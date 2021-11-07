from __future__ import absolute_import, unicode_literals
import random
# from celery.decorators import task
from celery import shared_task
from subscriber.models import Customer
from django.contrib.auth.models import User
import datetime

@shared_task
def updateSubscription():
    """ This task will unsubsscribe after the subscription period end"""
    today_date = datetime.datetime.now().strftime("%x")
    customers = Customer.objects.filter(planName=today_date)
    for customer in customers:
        customer.isSubscribe = False
        customer.save() 
        user = User.objects.get(email= customer.user)
        user.is_active = False
        user.save()
        print("user is deactivated")


    
    
    

