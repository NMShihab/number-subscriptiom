from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phnNumber = models.CharField(max_length=14,unique=True,blank=False,null=False)
    isSubscribe = models.BooleanField(default=True)

    def __str__(self):
        return self.phnNumber