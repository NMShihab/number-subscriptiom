from django.contrib import admin
from .models import Customer,SubscriptionPlan,SubscriptionData,SecondaryNumber
# Register your models here.

admin.site.register(Customer)
admin.site.register(SubscriptionData)
admin.site.register(SubscriptionPlan)
admin.site.register(SecondaryNumber)