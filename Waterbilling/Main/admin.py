from django.contrib import admin
from .models import *


class AccessTokenAdmin(admin.ModelAdmin):
    customers = AccessToken.objects.all().count()
    list_display=['token','created_at']

admin.site.register(AccessToken,AccessTokenAdmin)

class AdministratorAdmin(admin.ModelAdmin):
    admins = Administrator.objects.all().count()
    list_display=['user','first_name','last_name','contact_number']

admin.site.register(Administrator,AdministratorAdmin)

class ClientAdmin(admin.ModelAdmin):
    admins = Client.objects.all().count()
    list_display=['user','first_name','last_name','contact_number','meter_number','address','status']

admin.site.register(Client,ClientAdmin)

class WaterBillAdmin(admin.ModelAdmin):
    bills = WaterBill.objects.all().count()
    list_display=['client','meter_consumption','status','duedate','penaltydate']

admin.site.register(WaterBill,WaterBillAdmin)

class PaymentAdmin(admin.ModelAdmin):
    payments = Payment.objects.all().count()
    list_display=['client','amount','date_payed','security_key']

admin.site.register(Payment,PaymentAdmin)

class ReportProblemAdmin(admin.ModelAdmin):
    problems = ReportProblem.objects.all().count()
    list_display=['problem','client','date']

admin.site.register(ReportProblem,ReportProblemAdmin)

class ResponseProblemAdmin(admin.ModelAdmin):
    problems = ResponseProblem.objects.all().count()
    list_display=['response','problem','admin','date']

admin.site.register(ResponseProblem,ResponseProblemAdmin)