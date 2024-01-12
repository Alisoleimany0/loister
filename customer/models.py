from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        null=False,
        on_delete=models.CASCADE,
    )
    user_phone_number = models.CharField(max_length=20)
    favourites = models.ManyToManyField("shop.Product", blank=True)

    def __str__(self):
        return f'{self.user.username}'


class CustomerAddress(models.Model):
    customer = models.ForeignKey(
        CustomerProfile,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    delivery_phone_number = models.IntegerField()
    district = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.TextField()
    postal_code = models.IntegerField(null=False, default=0)



# def create_cart
#
#
# signals.pre_save.connect()
