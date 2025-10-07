from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import * 
from news.models import News
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import EmailMessage


  



def home(request):

    Servicedata = ServiceModel.objects.all()
    Aboutdata = AboutModel.objects.all()
    Clientdata = ClientModel.objects.all()
    Featuresdata = Features.objects.all()
    Newsdata = News.objects.all()
    portfoliodata = Portfolio.objects.all()
    headerdata = Header.objects.all()
    herodata = Hero.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()
    
    
    data = {
        'Servicedata': Servicedata,
        'Aboutdata': Aboutdata,
        'Featuresdata':Featuresdata,
        'Newsdata': Newsdata,
        'portfoliodata': portfoliodata,
        'headerdata': headerdata,
        'herodata': herodata,
        'footerdata': footerdata,
        'socialdata': socialdata
    }
    return render(request, "blog/index.html", data)

def innerpage(request):
    return render(request, "blog/inner-page.html")


def port_data(request, pk):
    Servicedata = ServiceModel.objects.all()
    headerdata = Header.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()
    port_data=Portfolio_details.objects.get(pk=pk)
    
    data = {
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'port_data': port_data,
        'footerdata': footerdata,
        'socialdata': socialdata

    }
    return render(request, "blog/portfolio-details.html", data)


def port(request):
    portfoliodata = Portfolio.objects.all()
    Servicedata = ServiceModel.objects.all()
    headerdata = Header.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()
    data = {
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'portfoliodata': portfoliodata,
        'footerdata': footerdata,
        'socialdata': socialdata 
    }
    return render(request, "blog/portfolio.html",data)

def subscribe(request):
    if request.method == "POST":
        
        email = request.POST.get('email')
        if email:
            Subscribe.objects.create(
                email = email
            )
            
    return redirect('/')
    #return render(request, "blog/index.html")

def contact(request):
    Servicedata = ServiceModel.objects.all()
    headerdata = Header.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        msg = request.POST.get('message')

        if name and email and subject and msg:
            # Save to database
            ContactModel.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=msg,
            )

            # HTML email message with user data
            email_message = f"""
            <html>
                <head>
                    <title>Contact</title>
                    <style>
                        .mailer-main {{
                            border: 1px solid green;
                            width: 80%;
                            margin: auto;
                            padding: 20px;
                            height: auto;
                            font-family: Arial, sans-serif;
                        }}
                        .hr {{
                            width: 100%;
                        }}
                    </style>
                </head>
                <body>
                    <div class="mailer-main">
                        <h1>Raymedia</h1>
                        <hr class="hr">
                        <div>
                            <h3>Inquiry Confirmed!</h3>
                            <h4>Thank You, {name}</h4>
                            <p>We are pleased to have you on our site. Your query will be looked after soon by us.</p>
                            <h4>Summary of your message:</h4>
                            <p><strong>Name:</strong> {name}</p>
                            <p><strong>Email:</strong> {email}</p>
                            <p><strong>Subject:</strong> {subject}</p>
                            <p><strong>Message:</strong><br>{msg}</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            # Send the email
            email_subject = 'Inquiry Mail Confirmation - Raymedia Graphix'
            from_email = 'muthonijuliet828@gmail.com'
            recipient_list = [email]

            email_obj = EmailMessage(
                email_subject,
                email_message,
                from_email,
                recipient_list,
            )
            email_obj.content_subtype = "html" 
            email_obj.send()

            messages.success(request, 'Your inquiry has been sent successfully!')

        else:
            messages.error(request, 'All fields are required!')

    data = {
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'footerdata': footerdata,
        'socialdata': socialdata
    }

    return render(request, "blog/contact.html", data)

def calculator(request):
    result = ''
    if request.method == "POST":
        try:
            val1 = float(request.POST.get('val1'))
            operator = request.POST.get('operator')
            val2 = float(request.POST.get('val2'))

            if operator == '+':
                result = val1 + val2
            elif operator == '-':
                result = val1 - val2
            elif operator == '*':
                result = val1 * val2
            elif operator == '/':
                result = val1 / val2
            elif operator == '%':
                result = val1 % val2
            else:
                result = 'Invalid operator'
        except ValueError:
            result = 'Invalid input'

    return render(request, "blog/calculator.html", {'c': result})


def even(request):
    c = ''
    if request.method== "POST":
        num = eval(request.POST.get('num'))
        if num % 2 == 0:
            c = "Even Number"
        else:
            c = "Odd Number"
    return render(request,"blog/even.html", {'c' : c})


#def mark(request):
    # t=''
    # p=''
    # c=''
   # data={}
    #if request.method == "POST":
     #   s1 = eval(request.POST.get('s1'))
      #  s2 = eval(request.POST.get('s2'))
       # s3 = eval(request.POST.get('s3'))
        #s4 = eval(request.POST.get('s4'))
        #s5 = eval(request.POST.get('s5'))

        #t = s1+s2+s3+s4+s5
        #p = t*100/500
        #if p >= 90:
         #   c = "Distinction"
        #elif p <90 and p >= 80 :
         #   c = "Fist Class"
        #elif p< 80 and p <=70 :
         #   c = "Second Class"
        #elif p< 70 and p <=45 :
         #   c = "Third Class"
        #elif p< 45 and p <=33 :
         #   c = "Pass"
        #else:
         #   c = "Fail"
        #data = {
         #   't': t,
          #  'p': p,
           # 'c': c
        #}

        
    #return render(request, "blog/marksheet.html",data)

def services(request):
     Servicedata = ServiceModel.objects.all()
     headerdata = Header.objects.all()
     footerdata = Footer.objects.all()
     socialdata = Social.objects.all()

     paginator = Paginator(Servicedata,2)
     page_num = request.GET.get('page')
     Servicedatafinal = paginator.get_page(page_num)
     last_page = Servicedatafinal.paginator.num_pages
     data = {
         'Servicedata': Servicedatafinal,
         'last_page': last_page,
         'total_page': [n+1 for n in range(last_page)],
         'headerdata': headerdata,
         'footerdata': footerdata,
         'socialdata': socialdata 
     }
     return render(request, "blog/services.html",data)

def news(request,slug):
    Newsdata = News.objects.get(slug = slug)
    Servicedata = ServiceModel.objects.all()
    headerdata = Header.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()
    data = {
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'footerdata': footerdata,
        'socialdata': socialdata,
        'Newsdata': Newsdata,
    }


    return render(request, "blog/news.html",data)


def about(request):
     Aboutdata = AboutModel.objects.all()
     Servicedata = ServiceModel.objects.all()
     headerdata = Header.objects.all()
     footerdata = Footer.objects.all()
     socialdata = Social.objects.all()
     data = {
        'Aboutdata': Aboutdata,
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'footerdata': footerdata,
        'socialdata': socialdata
     }
     return render(request, "blog/about.html",data)

#def team(request):
    #Teamdata = Team.objects.all()
   # Servicedata = ServiceModel.objects.all()
   # headerdata = Header.objects.all()
   # footerdata = Footer.objects.all()
    #socialdata = Social.objects.all()
    #data = {
      #  'Teamdata': Teamdata,
       # 'Servicedata': Servicedata,
      #  'headerdata': headerdata,
       # 'footerdata': footerdata,
       # 'socialdata': socialdata
  #  }
    #return render(request, "blog/team.html",data)

def footer(request):
    Servicedata = ServiceModel.objects.all()
    headerdata = Header.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()

    data = {
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'footerdata': footerdata,
        'socialdata': socialdata
    }

    return render(request, "blog/footer.html",data)

def service_detail(request, slug):
    service = ServiceModel.objects.get(slug = slug)
    Servicedata = ServiceModel.objects.all()
    headerdata = Header.objects.all()
    footerdata = Footer.objects.all()
    socialdata = Social.objects.all()

    data = {
        'service': service,
        'Servicedata': Servicedata,
        'headerdata': headerdata,
        'footerdata': footerdata,
        'socialdata': socialdata

    }
    return render(request, 'blog/service_detail.html', data)
