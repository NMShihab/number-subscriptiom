from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password 
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.conf import settings
import stripe
import re
import datetime
from random import randrange

from .models import Customer,SubscriptionData, SubscriptionPlan
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


def generate_phn_number(): 
    first_two_digit = "01"
    third_digit = str(randrange(3, 10))
    last_eight_digit = str(randrange(10000000, 100000000))
    return str(first_two_digit+third_digit+last_eight_digit)

   
    
def is_active_user(user):
    """ This funtion for check active customer"""
    user_ =  User.objects.get(email=user)
    return user_.is_active





@api_view(['POST'])
def customer_registration(request):
    """ This view will Register user and subscribe for a plan"""
    data = request.data
    
    phone_number = generate_phn_number()
    
    
 
    try:
        
            try:
                 
                # Create stripe account
                stripe_customer = stripe.Customer.create(
                    email = data['email']
                )

                # Set a default card for account
                s_card = stripe.Customer.create_source(
                    stripe_customer.id,
                    source="tok_amex",
                )
                
                plan_id = "price_1JsHMxSDkRo5FXlkOsq2QHSV"

                # if data["subscription_plan"]== "Globalnet Silver":
                #     plan_id = "price_1JsHOJSDkRo5FXlkQmfEQzhN"
                
                # if data["subscription_plan"]== "Globalnet Gold":
                #     plan_id = "price_1JsHPFSDkRo5FXlk9VSl41rV"

                # Create subscription for customer
                subscription = stripe.Subscription.create(
                    customer = stripe_customer.id,
                    items = [{'plan':plan_id}]
                )
                
                # Create User account
                user = User.objects.create(
                    email = data['email'],
                    password = make_password(data['password'] )    

                )

                start_date = datetime.datetime.now().strftime("%c")
                end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")

                subscription_plan = SubscriptionPlan.objects.get(subscription_plan_name="Globalnet Bronze")
               
                # Create customer data
                customer_data = Customer.objects.create(
                    user = user,
                    primary_number = phone_number,
                    subscription_plan = subscription_plan.subscription_plan_name,
                    stripe_id = stripe_customer.id,
                    start_date = start_date,
                    end_date = end_date,
                    subscription_id = subscription.id
    
                )
                
                # Entry Subscription data
                SubscriptionData.objects.create(
                    subscriber = data['email'],
                    subscription =  subscription_plan.subscription_plan_name,
                    subscription_start = start_date,
                    subscription_end = end_date                 
                    
                )
                    
                
                
               
                serializer= CustomerSerializer(customer_data,many=False)
                return Response(serializer.data)

            except Exception as e:
                # delete user if any functionality fails
                u = User.objects.get(username = data['email'])
                u.delete()
                raise Exception(e)
        

    except  Exception as e:
        message = {"detail":str(e)}
        print(e)
        return Response(message)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    
    """ Customer Details"""
    
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
        serializer = CustomerSerializer(customer, many=False)
    
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error":str(e)})
 
 
        
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_all_user_data(request):
    
    """ Get All Customer data. Only Admin acccess"""
      
    try:
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
    
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error":str(e)})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_customer_subscription(request):

    """This view will cancle subscription plan"""
    
    user = request.user 
    if is_active_user(user) == False :
        return Response({"message":"Your phone number is deactivated"})

    try: 
        user =  User.objects.get(email=user)  
        customer = Customer.objects.get(user=user)

        if customer.subscription_plan == SubscriptionPlan.objects.get(subscription_plan_name="Globalnet Gold"): 
            stripe.Subscription.delete(
                customer.subscription_id,
            )
            customer.subscription_id = ""
            customer.is_subscribe = False
            customer.save()

            user.is_active = False
            user.save()
        
            return Response({"message":"Your subscription cancel Successfully"})
        
        return Response({"message":"You Can not Cancel your plan"})
    
    except  Exception as e:    
        message = {"detail":str(e)}
        
        return Response(message)
    
   
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_plan(request):
    """ This view will change plan for customer """

    data = request.data
    
    if is_active_user(request.user) == False :
        return Response({"message":"Your phone number is deactivated."})

    start_date = datetime.datetime.now().strftime("%c")
    end_date = end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")
            
    # print(data["subscription_plan"])
    
    try: 
        user =  User.objects.get(email=request.user)  
        customer = Customer.objects.get(user=user)

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

    



    
 