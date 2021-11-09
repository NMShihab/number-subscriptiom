from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    """ Customer Model """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    primary_number = models.CharField(max_length=14,unique=True,blank=False,null=False)
    phone_number1=models.CharField(max_length=14,blank=True,null=True)
    phone_number2 = models.CharField(max_length=14,blank=True, null=True)
    subscription_plan = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=256)
    subscription_id = models.CharField(max_length=256,blank=True,null=True)
    start_date = models.CharField(max_length =256)
    end_date = models.CharField(max_length=256) 
    is_subscribe = models.BooleanField(default=True)

    def __str__(self):
        return self.primary_number