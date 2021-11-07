from django.urls import path
from .views import customerRegistration,cancelCustomerSubscription,changePlan

urlpatterns = [
    path('register/',customerRegistration,name="register"),
    path("cancel-subscription/",cancelCustomerSubscription,name="cancel"),
    path("change-subscription/",changePlan,name="change-plan")
]