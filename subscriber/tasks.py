from __future__ import absolute_import, unicode_literals
import random
# from celery.decorators import task
from celery import shared_task
from subscriber.models import Customer,SecondaryNumber
from django.contrib.auth.models import User
import datetime

@shared_task
def update_subscription():
    """ This task will run every mid night to unsubsscribe plan
        after the subscription period end """
   
    today_date = datetime.datetime.now().strftime("%x")
    customers = Customer.objects.filter(end_date=today_date)
    secondary_numbers = SecondaryNumber.objects.filter(end_date=today_date)
    
    # Deactivate account
    for customer in customers:
        customer.is_subscribe = False
        customer.save() 
        
        user = User.objects.get(email= customer.user)
        user.is_active = False
        user.save()
    
    # Remove phone number
    for secondary_number in secondary_numbers:
        secondary_number.delete()
        


    
    
    

