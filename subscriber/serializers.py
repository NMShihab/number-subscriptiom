from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer,SecondaryNumber,SubscriptionData

class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Customer
        fields =["user","email","primary_number","stripe_id","subscription_plan","start_date","end_date","subscription_id","is_subscribe"]
    
    def get_email(self,obj):
        email = str(obj.user)
        return email



class SeconderyNumberSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SecondaryNumber
        fields =["user","email","phn_number","stripe_id","subscription_plan","start_date","end_date","subscription_id","is_subscribe"]
    
    def get_email(self,obj):
        email = str(obj.user)
        return email


class SubscriptionHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubscriptionData
        fields =["subscriber","subscription","subscription_start","subscription_end"]
    
    