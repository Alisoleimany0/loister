from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django_jalali.db import models as jmodels

import customer
from customer.models import CustomerProfile, CustomerAddress


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=255)
    display_description = models.CharField(max_length=500, default='', blank=True, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    release_date = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0)
    star = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    @property
    def sell_price(self):
        if self.is_on_sale:
            return self.sale_price
        else:
            return self.price

    @property
    def units_sold(self):
        bought_products = BoughtProduct.objects.filter(product=self)
        total = 0
        for bought_product in bought_products:
            total += bought_product.quantity
        return total

    @property
    def default_image(self):
        image = ProductImage.objects.filter(product=self).filter(is_default=True)
        if image:
            return image.first()
        return None

    def is_favourite(self, customer: CustomerProfile):
        return self in customer.favourites.all()

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
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

    def save(self, *args, **kwargs):
        images = ProductImage.objects.filter(product=self.product)
        if not images:
            self.is_default = True
        super().save(*args, **kwargs)


class ProductOffers(models.Model):
    products = models.ManyToManyField(Product)
    finish_time = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # make sure we're not updating
        if not self.pk and ProductOffers.objects.exists():
            raise ValidationError("You can only create one instance of ProductOffers")
        return super(ProductOffers, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product Offers"
        verbose_name_plural = "Product Offers"

    def __str__(self):
        return "Product Offers"


# failed to put cart model in customer app due to circular import issues
class Cart(models.Model):
    customer = models.OneToOneField(
        CustomerProfile,
        null=True,
        on_delete=models.CASCADE
    )
    session = models.CharField(max_length=100, null=True, blank=True)
    products = models.ManyToManyField(Product, through='CartProductQuantity')


class CartProductQuantity(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'cart'], name='product_cart_constraint')
        ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)

    @property
    def total_price(self):
        if self.product.is_on_sale:
            price = self.product.sale_price
        else:
            price = self.product.price
        return price * self.quantity

    @property
    def sell_price(self):
        if self.product.is_on_sale:
            price = self.product.sale_price
        else:
            price = self.product.price
        return price

    def __str__(self):
        return f"{self.product} : {self.quantity}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("1processing", "پرداخت شده"),
        ("2payment", "در انتظار پرداخت"),
        ("3sent", "ارسال شده"),
    )
    customer = models.ForeignKey(
        CustomerProfile,
        null=True,
        on_delete=models.SET_NULL)
    session = models.CharField(max_length=100, null=True)
    # TODO handle dating :- after API implementation
    checkout_date = jmodels.jDateField(blank=True, default=timezone.now)
    customer_full_name = models.CharField(max_length=50, null=True, blank=True)
    invoice_date_time = jmodels.jDateField(default=timezone.now)
    total_price = models.IntegerField()
    delivery_phone_number = models.IntegerField()
    district = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address_text = models.TextField()
    postal_code = models.IntegerField(null=False, default=0)
    delivery_details = models.TextField(blank=True)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.id}"


class BoughtProduct(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    total_price = models.IntegerField()
    quantity = models.IntegerField()


def pre_product_image_save(sender, instance, **kwargs):
    if not ProductImage.objects.all():
        instance.is_default = True


signals.pre_save.connect(pre_product_image_save, sender=ProductImage)


def customer_post_save(instance: CustomerProfile, *args, **kwargs):
    try:
        cart = instance.cart
    except Cart.DoesNotExist as e:
        cart = Cart.objects.create(customer=instance)
        cart.save()


signals.post_save.connect(customer_post_save, sender=CustomerProfile)
