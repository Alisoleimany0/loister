from django.contrib.auth.models import User
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        null=False,
        on_delete=models.CASCADE,
    )
    user_phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username}'


class Address(models.Model):
    customer = models.ForeignKey(
        CustomerProfile,
        null=False,
        on_delete=models.CASCADE)
    delivery_phone_number = models.IntegerField()
    address = models.TextField()
    postal_code = models.IntegerField(null=False, default=0)
