from __future__ import absolute_import, unicode_literals
import random
# from celery.decorators import task
from celery import shared_task
from subscriber.models import Customer
from django.contrib.auth.models import User

@shared_task
def updateSubscription():
    customers = Customer.objects.filter(planName="Globalnet Silver")
    for customer in customers:
        customer.isSubscribe = False
        customer.save() 
        user = User.objects.get(email= customer.user)
        user.is_active = False
        user.save()
        print("user is deactivated")


    
    
    

