# Generated by Django 3.2.9 on 2021-11-10 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import subscriber.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber', models.CharField(max_length=14)),
                ('subscription', models.CharField(max_length=100)),
                ('subscription_start', models.CharField(blank=True, max_length=100, null=True)),
                ('subscription_end', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_plan_name', models.CharField(max_length=100)),
                ('subscription_plan_type', models.CharField(max_length=100)),
                ('subscription_plan_amount', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_number', models.CharField(max_length=14, unique=True)),
                ('phone_number1', models.CharField(blank=True, max_length=14, null=True)),
                ('phone_number2', models.CharField(blank=True, max_length=14, null=True)),
                ('subscription_plan', models.CharField(max_length=100, verbose_name=subscriber.models.SubscriptionPlan)),
                ('stripe_id', models.CharField(max_length=256)),
                ('subscription_id', models.CharField(blank=True, max_length=256, null=True)),
                ('start_date', models.CharField(max_length=256)),
                ('end_date', models.CharField(max_length=256)),
                ('is_subscribe', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
