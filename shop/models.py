from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models

from django.db.models import signals
from customer.models import CustomerProfile


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=40)
    display_description = models.CharField(max_length=500, default='', blank=True, null=True)
    details = models.TextField()
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    category = models.ManyToManyField(Category, blank=True)
    star = models.CharField(max_length=5, default='0', validators=[MaxLengthValidator(5), MinValueValidator('0')])
    # star = models.IntegerField(default=0 , validators=[MaxLengthValidator(5), MinValueValidator(0)])
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    def __str__(self):
        return self.name


class ProductProperty(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=200)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, upload_to='upload/product/')
    is_default = models.BooleanField(default=False)


class ProductOffers(models.Model):
    pass


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=400, default='', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.user.first_name} {self.customer.user.last_name}'


class HomepageCoverGroup(models.Model):
    def save(self, *args, **kwargs):
        if not self.pk and HomepageCoverGroup.objects.exists():
            raise ValidationError("You can only create one instance of HomepageCovers")
        return super(HomepageCoverGroup, self).save(*args, **kwargs)

    def __str__(self):
        return "Homepage Covers"


class HomepageCover(models.Model):
    group = models.ForeignKey(
        HomepageCoverGroup,
        on_delete=models.CASCADE
    )
    title = models.CharField(blank=True, max_length=30)
    description = models.CharField(blank=True, max_length=100)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title


def pre_product_image_save(sender, instance, **kwargs):
    if not ProductImage.objects.all():
        instance.is_default = True


signals.pre_save.connect(pre_product_image_save, sender=ProductImage)
