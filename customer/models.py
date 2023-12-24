from django.contrib.auth.models import User
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        null=False,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Address(models.Model):
    customer = models.ForeignKey(
        CustomerProfile,
        related_name='customer_address',
        null=False,
        on_delete=models.CASCADE)
    delivery_phone_number = models.IntegerField()
    postal_code = models.IntegerField(null=False, default=0)
