from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

from django.utils import timezone


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        null=False,
        on_delete=models.CASCADE,
    )
    user_phone_number = models.CharField(max_length=20)
    favourites = models.ManyToManyField("shop.Product", blank=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

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


class Review(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    author = models.ForeignKey('CustomerProfile', null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    date_time_field = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        if self.author:
            return self.author.full_name
        else:
            return "کاربر حذف شده"
