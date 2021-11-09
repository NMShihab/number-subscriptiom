from django.urls import path
from .views import customer_registration,cancel_customer_subscription,change_plan

urlpatterns = [
    path('register/',customer_registration,name="register"),
    path("cancel-subscription/",cancel_customer_subscription,name="cancel-plan"),
    path("change-subscription/",change_plan,name="change-plan")
]