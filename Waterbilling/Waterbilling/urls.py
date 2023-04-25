"""Waterbilling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('signin/', signin, name="signin"),
    path('signup/', signup, name="signup"),
    path('home/', home, name="home"),
    path('chart_data/', chart_data, name="chart_data"),
    path('payment/<str:pk>/', payment, name="payment"),
    path('report_problem/', report_problem, name="report_problem"),
    path('client_reports/', client_reports, name="client_reports"),
    path('client_profile/', client_profile, name="client_profile"),
    path('oauth_success/', oauth_success, name="oauth_success"),
    path('stk_push_success/', stk_push_success, name="stk_push_success"),
    path('client_bills/', client_bills, name="client_bills"),
    path('update_bill/<str:pk>/', update_bill, name="update_bill"),
    path('claim_payment/', claim_payment, name="claim_payment"),
    path('bills/', bills, name="bills"),
    path('consumption_data/', consumption_data, name="consumption_data"),

    # --------------------------------admin-----------------------------------
    path('admin_home/', admin_home, name="admin_home"),
    path('view_reports/', view_reports, name="view_reports"),
    path('download_report/', download_report, name="download_report"),
    path('problems/', problems, name="problems"),
    path('respond_problems/', respond_problems, name="respond_problems"),
    path('contact_clients/', contact_clients, name="contact_clients"),
    path('admin_profile/', admin_profile, name="admin_profile"),
    path('from_to_query/', from_to_query, name="from_to_query"),
    path('today_query/', today_query, name="today_query"),
    path('payment_data/', payment_data, name="payment_data"),
    path('download_invoice/', download_invoice, name="download_invoice"),


#   ------------------------------general------------------------------------------------
    path('logout/', logout_view, name="logout"),
]
