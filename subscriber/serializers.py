from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =["id","usename","email"]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields =["user","phnNumber","isSubscribe"]

    
    