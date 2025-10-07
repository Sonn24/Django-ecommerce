from core.models import Item
from .gemini_client import ask_gemini

def get_response(user_input):
    items = Item.objects.all()
    print("Loaded Items:", items)  # Debug log

    # Format price with commas
    item_data = "\n".join(
        f"Title: {item.title}, Price: Ksh {'{:,.2f}'.format(item.price)}, "
        f"Discount Price: {'{:,.2f}'.format(item.discount_price) if item.discount_price else 'N/A'}, "
        f"Category: {item.get_category_display()}, "
        f"Description: {item.description}, Features: {item.features}"
        for item in items
    )

    # Prepare prompt
    prompt = f"""
You are a helpful assistant for the emmywlks online store. Answer questions based on the product data below.
Always format prices with commas as thousand separators (e.g., Ksh 1,000.00 instead of Ksh 1000.00).

Important instructions for your responses:
- Never use labels like "Features:", "Description:", or other formal category labels in your responses
- Blend product information naturally into conversational sentences
- Mention product qualities and characteristics in a flowing, natural way
- Use conversational language instead of listing specifications
- Use short sentences and natural conversational flow
- dont talk about mode of payment unless asked

Payment Information:
- We exclusively accept M-Pesa as our payment method.
- After placing an order, customers will receive M-Pesa payment instructions.
- The payment process is secure and transactions are processed immediately.
- For any payment issues, customers can contact our support team.

Product Data:
{item_data}

Customer Question:
{user_input}
"""
    print("Prompt:", prompt)  # Log the full prompt

    # Get intelligent response from Gemini
    return ask_gemini(prompt)