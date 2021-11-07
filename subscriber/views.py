from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password 
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
    """ This Function will validate phn number"""
    if(num[0] == "0" and len(num) >11):
        return False
    
    if(num[0]== "8" and len(num)>13):
        return False
    pattern = re.compile('(0|880)?[-\s]?[1]\d{9}')
    return pattern.match(num) 


def IsAuthenticated(data):
    """This function will aythenticate user"""
    user_ =  User.objects.get(email=data["username"])
    return check_password(data["password"],user_.password)
   
    
def IsActive(data):
    """ This funtion for check active customer"""
    user_ =  User.objects.get(email=data["username"])
    return user_.is_active





@api_view(['POST'])
def customerRegistration(request):
    """ This view will Register user and subscribe fo a plan"""

    data = request.data
    
    try:
        if isValidNumber(data['phnNumber']):
            try:
            
                user = User.objects.create(
                    email = data['email'],
                    password = make_password(data['password'] )    

                )

                start_date = datetime.datetime.now().strftime("%c")
                end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")

                if(data["planName"] == "Globalnet Gold"):
                    end_date = (datetime.datetime.now() + datetime.timedelta(365)).strftime("%x")

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




@api_view(['PUT'])
def cancelCustomerSubscription(request):

    """This view will cancle subscription plan"""
    
    data = request.data


    if IsAuthenticated(data) == False :
        return Response({"message":"Please give us right email and password"})

    if IsActive(data) == False :
        return Response({"message":"Your phone number is deactivated"})

    
    
    try: 
        user =  User.objects.get(email=data["username"])  

        customer = Customer.objects.get(user=user.id)

        if(customer.planName == "Globalnet Bronze" or customer.planName == "Globalnet Silver"):
            return Response({"message":"You Can not Cancel your plan"})

        customer.isSubscribe = False
        customer.save()

        user.is_active = False
        user.save()
        serializer= CustomerSerializer(customer,many=False)
        return Response(serializer.data)
    except  Exception as e:
        message = {"detail":str(e)}
        print(e)
        return Response(message)
    
   
    

@api_view(['PUT'])
def changePlan(request):
    """ This view will change plan for customer"""

    data = request.data
    if IsAuthenticated(data) == False :
        return Response({"message":"Please give us right email and password"})
    # if IsActive(data) == False :
    #     return Response({"message":"Your phone number is deactivated."})

    start_date = datetime.datetime.now().strftime("%c")
    end_date = end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")
    

    if data["planName"] == "Globalnet Gold":
        end_date = (datetime.datetime.now() + datetime.timedelta(365)).strftime("%x")
    
        
    print(data["planName"])
    
    try: 
        user =  User.objects.get(email=data["username"])  
        

        customer = Customer.objects.get(user=user.id)

        

        customer.planName = data["planName"]
        customer.starDate = start_date
        customer.endDate = end_date
        customer.isSubscribe = True
        customer.save()

        user.is_active = True
        user.save()
        serializer= CustomerSerializer(customer,many=False)
        return Response(serializer.data)
    except  Exception as e:
        message = {"detail":str(e)}
        print(e)
        return Response(message)

    



    
 