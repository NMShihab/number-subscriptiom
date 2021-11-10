from django.urls import path
from .views import customer_registration,cancel_customer_subscription,change_plan,get_user_data,get_all_user_data
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',customer_registration,name="register"),
    path("user-details/",get_user_data,name="user-details"),
    path("users-lists/",get_all_user_data,name="user-details"),
    path("cancel-subscription/",cancel_customer_subscription,name="cancel-plan"),
    path("change-subscription/",change_plan,name="change-plan")
]