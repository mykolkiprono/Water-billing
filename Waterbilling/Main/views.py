from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from decouple import config


from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .mpesa.core import MpesaClient
from .mpesa import utils

import smtplib
import ssl
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from email.mime.image import MIMEImage

cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
# stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = 'https://api.darajambili.com/b2c/result'


def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)

def stk_push_success(request):
	phone_number = config('LNM_PHONE_NUMBER')
	amount = 1
	account_reference = 'ABC001'
	transaction_desc = 'STK Push Description'
	callback_url = stk_push_callback_url
	r = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
	return JsonResponse(r.response_description, safe=False)

def email( subject, body, emails=[]):
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = emails
    # subject = 'Website registration'
    # body = 'Activate your account.'
    message = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return 1

def is_client(user):
    return user.groups.filter(name='client').exists()

def is_admin(user):
    return user.groups.filter(name='administrator').exists()

def index(request):     
    return render(request, "index/eBusiness/index.html", {})

def signin(request):  
    loginForm=LoginForm()
    if request.method == "POST":
        username = request.POST['username']
        password =  request.POST['password']
        user = authenticate(
    		    request, 
    		    username=username, 
    		    password=password
        )
        if user:
            login(request, user)
            if is_client(user):
                return redirect(home)
            else:
                return redirect(admin_home)
                 
   
    return render(request, "auth/signin/colorlib-regform-2/colorlib-regform-2/index.html", {"loginForm":loginForm})

def signup(request):
    userForm=UserForm()
    clientForm=ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=UserForm(request.POST)
        clientForm=ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            raw_password = userForm.cleaned_data['password']
            user.set_password(user.password)
            user.save()
            
            client=clientForm.save(commit=False)
            client.user=user
            client.status = "Connected"
            client.save()
            # login(request, user)
            
            my_client_group = Group.objects.get_or_create(name='client')
            my_client_group[0].user_set.add(user)  
            subject = 'XYZ-Water registration Logins'
            body = 'Your Username : '+str(user.username)+' and Password : '+str(raw_password)
            email( subject, body, emails=[user.email])
            return redirect(signup)
    return render(request, "admin-home/argon/signup.html", {'userForm':userForm,'clientForm':clientForm})
    # return render(request, "auth/signup/colorlib-regform-2/colorlib-regform-2/index.html", {'userForm':userForm,'clientForm':clientForm})

def home(request):     
    user = request.user
    client = Client.objects.filter(user=user).first()
    plans = Payment.objects.filter(client=client)
    bills = client.bill.all()
    consumption=0
    
    for bill in bills:
        consumption+=int(bill.meter_consumption)

    total=consumption*2
    # chart_data(request)
    return render(request, "client-home/argon/index.html", {"user":user,"plans":plans,"total":total,"consumption":consumption,"client":client})


import random
from django.utils import timezone
def payment(request,pk):     
    user = request.user
    client=Client.objects.get(user=user)
    bill = WaterBill.objects.get(pk=pk)
    test = False
    msg=''
    if bill.status == "Paid":
        test = True
        msg="This bill has already been paid"
    
    
    amount=0
    account_reference = 'Water Bill Payment'
    # transaction_desc = ''
    transaction_desc = 'STK Push Description'
    if bill is not None:
        if (request.POST):
            data = request.POST.dict()
            phone_number = data.get("phone")
            if len(phone_number)<10:
                msg="invalid phone number"
                return render(request, "client-home/argon/payment.html", {"user":user,"bill":bill,"msg":msg,"test":test})          

            security_key = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            
            r=cl.stk_push(phone_number, bill.cost, account_reference, transaction_desc, stk_push_callback_url)
            p=Payment.objects.create(client=client,amount=bill.cost,date_payed=datetime.datetime.now(),security_key=security_key)
            bill.status="Paid"
            bill.save()
            
            # parse_stk_result(r)
            body = "you have successfully paid "+str(bill.cost)+"for "+"water Bill  "+"security key="+str(security_key)
            email( "water payment", body, emails=[user.email])
            redirect(payment,pk)
    return render(request, "client-home/argon/payment.html", {"user":user,"bill":bill,"msg":msg,"test":test})

def bills(request):
    user = request.user
    client = Client.objects.get(user=user)
    bills = client.bill.all()
    return render(request, "client-home/argon/client_bills.html", {"user":user,"client":client,"bills":bills})
def claim_payment(request):     
    user = request.user
    if (request.POST):
        data = request.POST.dict()
        security_code = data.get("security")

        payment=Payment.objects.filter(security_key=security_code)
        if payment.exists():
            pass
    return render(request, "client-home/argon/claim.html", {"user":user})
from dateutil.relativedelta import relativedelta
def client_bills(request):     
    user = request.user
    clients = Client.objects.all()
    if (request.POST):
        data = request.POST.dict()
        security_code = data.get("security")
        

        payment=Payment.objects.filter(security_key=security_code)
        if payment.exists():
            if payment.status!="Active":
                payment.status="Active"
                payment.save()
    return render(request, "admin-home/argon/bills.html", {"user":user,"clients":clients})

def update_bill(request,pk):
    user = request.user
    client = Client.objects.get(id=pk)
    bills = client.bill.filter(status="pending").order_by('duedate')
    total=0
    if bills is not None:
        for bill in bills:
            total+=int(bill.meter_consumption)*2
    if (request.POST):
        data = request.POST.dict()
        consuption = float(data.get("consuption"))
        due_date = data.get("due_date")
        date_str = "2023-04-30 14:30:00"  # Example date string
        date_format = "%Y-%m-%d %H:%M:%S"  # Example date format string
        due_date = datetime.datetime.strptime(date_str, date_format)
        now = datetime.datetime.now()  # Get the current date and time
        penalty_date = due_date + relativedelta(months=1)
        cost = consuption*2
        subject = 'New Water Bill: XYZ-Water'
        body = 'Your Consumption '+str(consuption)+' and cost Kshs, '+str(cost)+' due date '+str(due_date)
        email( subject, body, emails=[user.email])
        
        WaterBill.objects.create(client=client,meter_consumption=consuption,cost=cost, status="pending", duedate=due_date,penaltydate=penalty_date)
        return redirect(update_bill,pk)
    return render(request, "admin-home/argon/updatebill.html", {"client":client,"user":user,"bills":bills,"total":total})

def client_reports(request):     
    user = request.user
    client = Client.objects.filter(user=user).first()
    plans = Payment.objects.filter(client=client)
    complaints = ReportProblem.objects.filter(client=client)
    return render(request, "client-home/argon/tables.html", {"user":user,"plans":plans,"complaints":complaints})

def report_problem(request):     
    user = request.user
    client=Client.objects.get(user=user)
    if (request.POST):
        data = request.POST.dict()
        problem = data.get("problem")
        ReportProblem.objects.create(client=client,problem=problem,date=datetime.datetime.now())
    return render(request, "client-home/argon/problem.html", {"user":user})

def client_profile(request):
    user = request.user
    client = Client.objects.get(user=user)
    return render(request, "", {"user":user,"client":client})

# ----------------------------------------Admin---------------------------------------------------------
from django.db.models import Sum

def admin_home(request):
    user = request.user
    problems = ReportProblem.objects.all()
    clients = Client.objects.all()
    payments = Payment.objects.all()
    
    total = payments.aggregate(Sum('amount'))
    total = total.get('amount__sum') 
    
  
    return render(request, "admin-home/argon/index.html", {"user":user,"problems":problems,"clients":clients,"total":total,"payments":payments})

def contact_clients(request):
    user = request.user
    clients = User.objects.all()
    emails=[]
    for client in clients:
        emails.append(client.email)
    if (request.POST):
        data = request.POST.dict()
        subject = data.get("subject")
        body = data.get("body")
        email( subject, body, emails=emails)

    return render(request, "admin-home/argon/contact.html", {"user":user})

def problems(request):
    user = request.user
    prblms = ReportProblem.objects.all()
    return render(request, "admin-home/argon/respond.html", {"user":user, "prblms":prblms})

def respond_problems(request,pk):
    user = request.user
    return render(request, "admin-home/argon/respond.html", {"user":user})



def view_reports(request):
    user = request.user
    clients = Client.objects.all()
    payments = Payment.objects.all()
    bills = WaterBill.objects.all()
    total = payments.aggregate(Sum('amount'))
    total = total.get('amount__sum')
    return render(request, "admin-home/argon/tables.html", {"user":user,"payments":payments,"clients":clients,"total":total,"bills":bills})

def download_report(request):
    user = request.user
    return render(request, "admin-home/argon/upgrade.html", {"user":user})

def admin_profile(request):
    user = request.user
    admin = Administrator.objects.get(user=user)
    return render(request, "admin-home/argon/profile.html", {"user":user,"admin":admin})

def today_query(request):
    user = request.user
    last = user.last_login
    now = datetime.datetime.now()
    user = request.user
    
    payments = Payment.objects.filter(date_payed__date=datetime.date.today())
    
    total = payments.aggregate(Sum('amount'))
    total = total.get('amount__sum')    
    # bills = WaterBill.objects.filter(date_payed__date=datetime.date.today())
    return render(request, "admin-home/argon/tables.html", {"user":user, "payments":payments,"total":total})

def from_to_query(request):   
    
    if (request.POST):
        user = request.user
        data = request.POST.dict()
        from_date = data.get("from")
        to_date = data.get("to")       
       
        payments = Payment.objects.filter(date_payed__range=[from_date, to_date])

        total = payments.aggregate(Sum('amount'))
        total = total.get('amount__sum')      
        return render(request, "admin-home/argon/tables.html", {"user":user, "payments":payments,"total":total})
    
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
import calendar
from django.db.models.functions import ExtractDay

def payment_data(request):
    current_year = timezone.now().year
    # payments = Payment.objects.filter(date_payed__year=current_year)
    # payments_by_month = payments.annotate(month=ExtractMonth('date_payed')).values('month').annotate(total=Sum('amount'))
    # data = {
    #     'months': [calendar.month_name[payment['month']] for payment in payments_by_month],
    #     'totals': [payment['total'] for payment in payments_by_month]
    # }
    # return JsonResponse(data)
    payments = Payment.objects.filter(date_payed__year=current_year)
    payments_by_day = payments.annotate(day=ExtractDay('date_payed')).values('day').annotate(total=Sum('amount'))
    data = {
        'days': [payment['day'] for payment in payments_by_day],
        # 'days': [calendar.day_name[payment['day']-1] if payment['day'] else '' for payment in payments_by_day],
        'totals': [payment['total'] for payment in payments_by_day]
    }
    # print(data)
    return JsonResponse(data)
def chart_data(request):
    user = request.user
    current_year = timezone.now().year
    return JsonResponse()

def consumption_data(request):
    user=request.user
    client = Client.objects.get(user=user)
    # Retrieve the consumption data for the specified user and group it by month
    consumption_by_month = WaterBill.objects.filter(client=client).annotate(month=ExtractMonth('duedate')).values('month').annotate(total_consumption=Sum('meter_consumption'))
    # Create a dictionary with the month names and the corresponding total consumption
    data = {
        'months': [calendar.month_name[consumption['month']] for consumption in consumption_by_month],
        'totals': [consumption['total_consumption'] for consumption in consumption_by_month]
    }
    # Return the data as a JSON response
    return JsonResponse(data)

from django.shortcuts import render
from django.utils import timezone
from .models import Payment
from datetime import timedelta

def notify_clients(request):
      
    return 1

def logout_view(request):
    logout(request)
    return redirect(index)


from xhtml2pdf import pisa
import io
from django.template.loader import get_template

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return pdf



def download_invoice(request):
    user = request.user
    payments = Payment.objects.all() 
    
    total = payments.aggregate(Sum('amount'))
    total = total.get('amount__sum')    
    
    pdf = render_to_pdf("admin-home/argon/downlod_invoice.html", {'payments':payments, 'user':user,"total":total})
    return render_to_pdf("admin-home/argon/downlod_invoice.html", {'payments':payments,'user':user,"total":total})
