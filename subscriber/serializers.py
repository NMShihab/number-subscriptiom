from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Customer
        fields =["user","email","phnNumber","isSubscribe"]
    
    def get_email(self,obj):
        email = str(obj.user)
        return email

    
    