from django.urls import path
from .views import customerRegistration

urlpatterns = [
    path('register/',customerRegistration,name="register"),
]