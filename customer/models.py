from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

from django.utils import timezone

import loister.utils


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        null=False,
        on_delete=models.CASCADE,
    )
    user_phone_number = models.CharField(max_length=20, null=True, verbose_name='شماره تلفن کاربری')
    favourites = models.ManyToManyField("shop.Product", blank=True)
    remember_me = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

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
        on_delete=models.CASCADE,
        verbose_name='مشتری')
    delivery_phone_number = models.CharField(verbose_name='شماره تحویل گیرنده', max_length=15)
    district = models.CharField(max_length=20, verbose_name='استان')
    city = models.CharField(max_length=20, verbose_name='شهر')
    address = models.TextField(verbose_name='آدرس')
    postal_code = models.CharField(null=False, default=0, verbose_name='کد پستی', max_length=15)

    class Meta:
        verbose_name = 'آدرس کاربر'
        verbose_name_plural = 'آدرس کاربران'


class Review(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, verbose_name='محصول')
    author = models.ForeignKey('CustomerProfile', null=True, on_delete=models.SET_NULL, verbose_name='نویسنده')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    content = models.TextField(null=True, blank=True, verbose_name='محتوا')
    rating = models.IntegerField(default=0, null=True, blank=True, verbose_name='امتیاز')
    date_time_field = models.DateTimeField(default=timezone.now, verbose_name='زمان و تاریخ')
    approved = models.BooleanField(default=False, verbose_name='تایید شده')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظر ها'

    @property
    def author_name(self):
        if self.author:
            return self.author.full_name
        else:
            return "کاربر حذف شده"

    @property
    def content_text(self):
        return loister.utils.truncate_text(self.content, 50)
    content_text.fget.short_description = 'محتوا'

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        if self.author:
            return self.author.full_name
        else:
            return "کاربر حذف شده"


def customer_post_save(instance: CustomerProfile, *args, **kwargs):
    from cart.models import Cart
    try:
        cart = instance.cart
    except Cart.DoesNotExist as e:
        cart = Cart.objects.create(customer=instance)
        cart.save()


signals.post_save.connect(customer_post_save, sender=CustomerProfile)
