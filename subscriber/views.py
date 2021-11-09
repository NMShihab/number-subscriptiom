from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password 
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.conf import settings
import stripe
import re
import datetime

from .models import Customer
from .serializers import CustomerSerializer


stripe.api_key = settings.STRIPE_API_KEY


def is_valid_number(num):
    """ This Function will validate phn number"""
    
    if(num[0] == "0" and len(num) >11):
        return False
    
    if(num[0]== "8" and len(num)>13):
        return False
    pattern = re.compile('(0|880)?[-\s]?[1]\d{9}')
    return pattern.match(num) 


def is_authenticated(data):
    """This function will aythenticate user"""
    user_ =  User.objects.get(email=data["username"])
    return check_password(data["password"],user_.password)
   
    
def is_active_user(data):
    """ This funtion for check active customer"""
    user_ =  User.objects.get(email=data["username"])
    return user_.is_active





@api_view(['POST'])
def customer_registration(request):
    """ This view will Register user and subscribe fo a plan"""

    data = request.data


    
    try:
        if is_valid_number(data['primary_number']):
            try:

                stripe_customer = stripe.Customer.create(
                    email = data['email']
                )

                s_card = stripe.Customer.create_source(
                    stripe_customer.id,
                    source="tok_amex",
                )

                plan_id = "price_1JsHMxSDkRo5FXlkOsq2QHSV"

                if data["subscription_plan"]== "Globalnet Silver":
                    plan_id = "price_1JsHOJSDkRo5FXlkQmfEQzhN"
                
                if data["subscription_plan"]== "Globalnet Gold":
                    plan_id = "price_1JsHPFSDkRo5FXlk9VSl41rV"

                subscription = stripe.Subscription.create(
                    customer = stripe_customer.id,
                    items = [{'plan':plan_id}]
                )
            
                user = User.objects.create(
                    email = data['email'],
                    password = make_password(data['password'] )    

                )

                start_date = datetime.datetime.now().strftime("%c")
                end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")

               

                customer_data = Customer.objects.create(
                    user = user,
                    primary_number = data['primary_number'],
                    subscription_plan = data['subscription_plan'],
                    stripe_id = stripe_customer.id,
                    start_date = start_date,
                    end_date = end_date,
                    subscription_id = subscription.id
    
                )
               
                serializer= CustomerSerializer(customer_data,many=False)
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
def cancel_customer_subscription(request):

    """This view will cancle subscription plan"""
    
    data = request.data


    if is_authenticated(data) == False :
        return Response({"message":"Please give us right email and password"})

    if is_active_user(data) == False :
        return Response({"message":"Your phone number is deactivated"})

    
    
    try: 
        user =  User.objects.get(email=data["username"])  

        customer = Customer.objects.get(user=user.id)

        print(customer)

        if(customer.subscription_plan == "Globalnet Bronze" or customer.subscription_plan == "Globalnet Silver"):
            return Response({"message":"You Can not Cancel your plan"})
        stripe.Subscription.delete(
            customer.subscription_id,
        )
        customer.is_subscription = False
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
def change_plan(request):
    """ This view will change plan for customer"""

    data = request.data
    if is_authenticated(data) == False :
        return Response({"message":"Please give us right email and password"})

    if is_active_user(data) == False :
        return Response({"message":"Your phone number is deactivated."})

    start_date = datetime.datetime.now().strftime("%c")
    end_date = end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")
    

    if data["subscription_plan"] == "Globalnet Gold":
        end_date = (datetime.datetime.now() + datetime.timedelta(365)).strftime("%x")
    
        
    print(data["subscription_plan"])
    
    try: 
        user =  User.objects.get(email=data["username"])  
        

        customer = Customer.objects.get(user=user.id)

        if customer.is_subscribe:
            stripe.Subscription.delete(
            customer.subscription_id,
        )


        

        plan_id = "price_1JsHMxSDkRo5FXlkOsq2QHSV"

        if data["subscription_plan"]== "Globalnet Silver":
            plan_id = "price_1JsHOJSDkRo5FXlkQmfEQzhN"
                
        if data["subscription_plan"]== "Globalnet Gold":
            plan_id = "price_1JsHPFSDkRo5FXlk9VSl41rV"

        subscription = stripe.Subscription.create(
            customer = customer.stripe_id,
            items = [{'plan':plan_id}]
        )       


        customer.subscription_plan = data["subscription_plan"]
        customer.start_date = start_date
        customer.end_date = end_date
        customer.subscription_id = subscription.id
        customer.is_subscribe = True
        customer.save()

        user.is_active = True
        user.save()
        serializer= CustomerSerializer(customer,many=False)
        
        return Response(serializer.data)
    
    except  Exception as e:
        
        message = {"detail":str(e)}
        print(e)
        return Response(message)

    



    
 