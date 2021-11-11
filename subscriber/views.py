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

from .models import Customer,SubscriptionData, SubscriptionPlan,SecondaryNumber
from .serializers import CustomerSerializer,SeconderyNumberSerializer, SubscriptionHistorySerializer


stripe.api_key = settings.STRIPE_API_KEY


def generate_phn_number(): 
    """Generate Bangladeshi phn number"""
    first_two_digit = "01"
    third_digit = str(randrange(3, 10))
    last_eight_digit = str(randrange(10000000, 100000000))
    
    return str(first_two_digit+third_digit+last_eight_digit)
 

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
                subscription_plan = subscription_plan,
                stripe_id = stripe_customer.id,
                start_date = start_date,
                end_date = end_date,
                subscription_id = subscription.id
    
            )
                
            # Entry Subscription data
            SubscriptionData.objects.create(
                subscriber = phone_number,
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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_another_number(request):
    """ This function will generate new number and plan for subscriber """
    
    user = request.user   
    phone_number = generate_phn_number()
    
    user_email = user.username
       
    try:                      
        # Create stripe account
        stripe_customer = stripe.Customer.create(
            email = user_email
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

        # Create a default subscription for customer 
        subscription = stripe.Subscription.create(
            customer = stripe_customer.id,
            items = [{'plan':plan_id}]
        )
                
                
        start_date = datetime.datetime.now().strftime("%c")
        end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")

        subscription_plan = SubscriptionPlan.objects.get(subscription_plan_name="Globalnet Bronze")
               
        # Create customer data
        customer_data = SecondaryNumber.objects.create(
            user = user,
            phn_number = phone_number,
            subscription_plan = subscription_plan,
            stripe_id = stripe_customer.id,
            start_date = start_date,
            end_date = end_date,
            subscription_id = subscription.id
    
        )
                
        # Entry Subscription data
        SubscriptionData.objects.create(
            subscriber = phone_number,
            subscription =  subscription_plan.subscription_plan_name,
            subscription_start = start_date,
            subscription_end = end_date                 
                    
        )
                    
                           
        serializer= SeconderyNumberSerializer(customer_data,many=False)
        return Response(serializer.data)

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
        
            return Response({"message":"Your subscription cancel Successfully. Your Number is deactivated.Company has own your Number"})
        
        return Response({"message":"You Can not Cancel your plan"})
    
    except  Exception as e:    
        message = {"Error":str(e)}
        
        return Response(message)
    
   
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_plan(request):
    """ This view will change plan for customer """

    data = request.data

    start_date = datetime.datetime.now().strftime("%c")
    end_date = end_date = (datetime.datetime.now() + datetime.timedelta(30)).strftime("%x")
            
    # print(data["subscription_plan"])
    
    try: 
        user =  User.objects.get(email=request.user)  
        customer = Customer.objects.get(user=user)
        subscription_plan = SubscriptionPlan.objects.get(subscription_plan_name=data["subscription_plan"])

        if customer.is_subscribe:
            stripe.Subscription.delete(
            customer.subscription_id,
        )       

        plan_id = "price_1JsHMxSDkRo5FXlkOsq2QHSV"

        if data["subscription_plan"]== "Globalnet Silver":
            plan_id = "price_1JsHOJSDkRo5FXlkQmfEQzhN"
                
        if data["subscription_plan"]== "Globalnet Gold":
            plan_id = "price_1JsHPFSDkRo5FXlk9VSl41rV"

        # Create new stripe subscription
        subscription = stripe.Subscription.create(
            customer = customer.stripe_id,
            items = [{'plan':plan_id}]
        )   
        
        # Update SubscriptionData      
        subscription_user_data = SubscriptionData.objects.filter(subscriber=customer.primary_number)  
        for data_subscriber in subscription_user_data:
            if(data_subscriber.subscription_start == customer.start_date):
                data_subscriber.subscription_end = start_date  
                data_subscriber.save()          
                break   
              
               
        # Change subscription plan info
        customer.subscription_plan = subscription_plan
        customer.start_date = start_date
        customer.end_date = end_date
        customer.subscription_id = subscription.id
        customer.is_subscribe = True
        customer.save()
                
        # Create new subscription data 
        SubscriptionData.objects.create(
            subscriber = customer.primary_number,
            subscription =  subscription_plan.subscription_plan_name,
            subscription_start = start_date,
            subscription_end = end_date                 
                    
        )
        
        serializer= CustomerSerializer(customer,many=False)
        
        return Response(serializer.data)
    
    except  Exception as e:   
        message = {"Error":str(e)}
        return Response(message)

    

@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_all_subscription_history(request):
    try:
        all_data = SubscriptionData.objects.all()
        serializer =  SubscriptionHistorySerializer(all_data,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"message":str(e)})
    

    
 