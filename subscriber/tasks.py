from __future__ import absolute_import, unicode_literals
import random
# from celery.decorators import task
from celery import shared_task
from subscriber.models import Customer

@shared_task
def updateSubscription():
    customers = Customer.objects.all()
    for customer in customers:
        customer.isSubscribe = False
        customer.save()

    
    
    

