from django.db import models
from django.contrib.auth.models import User
import datetime
import string, secrets


class AccessToken(models.Model):
	token = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		get_latest_by = 'created_at'

	def __str__(self):
		return self.token

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30) 
    contact_number = models.CharField(null=True, unique=True, max_length=10)
    email = models.EmailField()
    def __str__(self):       
        return f"{self.last_name}, {self.first_name}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    meter_number = models.CharField(max_length=15, default=None)
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30) 
    contact_number = models.CharField(null=True, unique=True, max_length=10)
    location = models.CharField(max_length=50, default=None,null=True,blank=True)
    address = models.CharField(max_length=250)
    appartment_name = models.CharField(max_length=250,default=None,null=True,blank=True)
    appartment_number = models.CharField(max_length=30,default=None,null=True,blank=True)
    status = models.TextField(choices=(('Connected', 'Connected'), ('Disconnected', 'Disconnected'), ('Pending', 'Pending')))
    usage = models.TextField(choices=(('Household', 'Household'), ('Commercial', 'Commercial')), default='Household')

    def __str__(self):       
        return f"{self.last_name}, {self.first_name}"

class Payment(models.Model):
     client = models.ForeignKey(Client, on_delete=models.CASCADE)
     amount = models.DecimalField(max_digits=20, decimal_places=2)
     date_payed = models.DateTimeField(auto_now=True)
     security_key = models.CharField(max_length=10)

     def __str__(self):
          return f"{self.client.first_name}, {self.client.last_name}, {self.amount}"

class ReportProblem(models.Model):
     client = models.ForeignKey(Client, on_delete=models.CASCADE)
     problem = models.TextField()
     date = models.DateTimeField(auto_now=True)

class ResponseProblem(models.Model):
     admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)
     problem = models.ForeignKey(ReportProblem, on_delete=models.CASCADE)
     response = models.TextField()
     date = models.DateTimeField(auto_now=True)

class WaterBill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name="bill")
    meter_consumption = models.IntegerField(default=0)
    status = models.TextField(choices=(('Paid','Paid'),('pending', 'pending')), null=True)
    cost = models.IntegerField(default=1)
    duedate = models.DateField(null=True)
    penaltydate = models.DateField(null=True)


    def __str__(self):
        return f'{self.meter_consumption}'


class Metric(models.Model):
    consump_amount = models.FloatField(default=1, null=True)
    penalty_amount = models.FloatField(default=1, null=True)