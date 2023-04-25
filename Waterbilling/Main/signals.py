from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone

from .models import Payment
today = timezone.now().date()




# @receiver(post_save, sender=Payment)
# def update_payment_status(sender, instance, **kwargs):
#     if instance.plan == "Weekly" and instance.status != "Expired":
#         if instance.date_payed < datetime.datetime.now() - datetime.timedelta(weeks=1):
#             instance.status = "Expired"
#             instance.save()
