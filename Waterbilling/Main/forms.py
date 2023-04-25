from .models import *
from django.contrib.auth.models import User
from django import forms
from . import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.validators import UnicodeUsernameValidator
from datetime import datetime

class UserForm(forms.ModelForm):

    class Meta:
        model = User 
        fields = ['username','password','email']

    def clean(self):
        super(UserForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username.isnumeric():
            self._errors['username'] = self.error_class(['username cannot be numbers'])
        if len(username) < 3:
            self._errors['username'] = self.error_class(['username must be more than 3 characters'])

        if len(password) < 5:
            self._errors['password'] = self.error_class(['password cannot be less than 5 characters'])
        # if password.isnumeric:
        #     self._errors['password'] = self.error_class(['password must be alphanumeric'])

        

        return self.cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Invalid credentials")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
    

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client 
        fields= ['first_name','last_name','contact_number','address','meter_number','appartment_name','appartment_number','usage']


    def clean(self):
        super(ClientForm, self).clean()

        phone_number = self.cleaned_data.get('contact_number')
        meter_number = self.cleaned_data.get('meter_number')
        address = self.cleaned_data.get('address')

        if len(str(phone_number))<10:
            self._errors['contact_number'] = self.error_class(['must be a minimum of 10 characters'])

        if len(str(meter_number))<15:
            self._errors['meter_number'] = self.error_class(['must be a minimum of 15 characters'])      

        if len(str(address))<8:
            self._errors['address'] = self.error_class(['must be a minimum of 8 characters'])                

        return self.cleaned_data