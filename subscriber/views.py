from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth.models import User
from .tasks import updateSubscription
from rest_framework import status
from django.conf import settings
import stripe
import re
import datetime

from .models import Customer
from .serializers import CustomerSerializer


stripe.api_key = settings.STRIPE_API_KEY

def isValidNumber(num):
    if(num[0] == "0" and len(num) >11):
        return False
    
    if(num[0]== "8" and len(num)>13):
        return False
    pattern = re.compile('(0|880)?[-\s]?[1]\d{9}')
    return pattern.match(num) 
    

@api_view(['POST'])
def customerRegistration(request):
    data = request.data
    
    

    print(data)

    try:
        if isValidNumber(data['phnNumber']):
            try:
            
                user = User.objects.create(
                    email = data['email'],
                    password = make_password(data['password'] )    

                )

                start_date = datetime.datetime.now().strftime("%c")
                end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%c")

                customerData = Customer.objects.create(
                    user = user,
                    phnNumber = data['phnNumber'],
                    planName = data['planName'],
                    stripe_id = user.id,
                    starDate = start_date,
                    endDate = end_date
                

                )

                
                
                serializer= CustomerSerializer(customerData,many=False)
                return Response(serializer.data)
            except Exception as e:
                u = User.objects.get(username = data['email'])
                u.delete()
                raise Exception(e)
        else:
            print("Phone Number is not correct")
            raise Exception("Phone Number is not correct")

    except  Exception as e:
        message = {"detail":str(e)}
        print(e)
        return Response(message)


def cancelCustomerSubscription(request):
    pass 