import os
import environ
import google.generativeai as genai
import re

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Configure API
genai.configure(api_key=env("MY_API_KEY"))

def ask_gemini(prompt):
    try:
        # Update to the newer model version
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        # Get the response text
        raw_text = response.text
        
        # Check if the entire response is wrapped in asterisks (internal thought pattern)
        if raw_text.startswith('**') and raw_text.endswith('**'):
            # Extract just the content inside the outer asterisks
            clean_text = raw_text[2:-2]
        else:
            # Otherwise just remove all asterisks
            clean_text = re.sub(r'\*+', '', raw_text)
            
        # For a more conversational tone in incomplete query responses
        if "customer's question is incomplete" in clean_text:
            # Replace with a friendlier message
            clean_text = "Could you please specify which shoe you'd like to know the price of? We have Tassel loafers (Ksh 4000), Chelsea boots (Ksh 5500), and Wingtip shoes (Ksh 5000) available."
        
        return clean_text
    except Exception as e:
        # Error handling
        print(f"Gemini API error: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."