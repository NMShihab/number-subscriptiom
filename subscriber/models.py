from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phnNumber = models.CharField(max_length=14,unique=True,blank=False,null=False)
    planName = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=256)
    startDate = models.CharField(max_length =256)
    endDate = models.CharField(max_length=256)
    subscription_id = models.CharField(max_length=256,blank=True,null=True)
    isSubscribe = models.BooleanField(default=True)

    def __str__(self):
        return self.phnNumber