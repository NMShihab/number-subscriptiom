from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

from .models import Customer
from .serializers import CustomerSerializer, UserSerializer

# Create your views here.


@api_view(['POST'])
def customerRegistration(request):
    data = request.data

    print(data)

    try:
        user = User.objects.create(
            username = data["username"],
            email = data['email'],
            password = make_password(data['password'] )    

        )

        customerData = Customer.objects.create(
            user = user,
            phnNumber = data['phnNumber'],
            isSubscribe = data['isSubscribe']

        )
        userData = UserSerializer(user,many=False)
        customerData = CustomerSerializer(customerData,many=False)
        # serializer = userData.data + customerData.data
        return Response(customerData.data)

    except  Exception as e:
        message = e
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


def cancelCustomerSubscription(request):
    pass