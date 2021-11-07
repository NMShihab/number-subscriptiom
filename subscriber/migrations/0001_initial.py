# Generated by Django 3.2.9 on 2021-11-07 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phnNumber', models.CharField(max_length=14, unique=True)),
                ('planName', models.CharField(max_length=100)),
                ('stripe_id', models.CharField(max_length=256)),
                ('startDate', models.CharField(max_length=256)),
                ('endDate', models.CharField(max_length=256)),
                ('subscription_id', models.CharField(blank=True, max_length=256, null=True)),
                ('isSubscribe', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
