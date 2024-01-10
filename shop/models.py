from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxLengthValidator, MaxValueValidator
from django.db import models
from django.db.models import signals
from django.utils import timezone

from customer.models import CustomerAddress, CustomerProfile


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=40)
    display_description = models.CharField(max_length=500, default='', blank=True, null=True)
    description = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    release_date = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0)
    star = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    @property
    def units_sold(self):
        return 0

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

    def save(self, *args, **kwargs):
        # make sure we're not updating
        if not self.pk and HomepageCoverGroup.objects.exists():
            raise ValidationError("You can only create one instance of ProductOffers")
        return super(ProductOffers, self).save(*args, **kwargs)


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("payment", "در انتظار پرداخت"),
        ("processing", "در حال پردازش"),
        ("sent", "ارسال شده"),
    )
    products = models.ManyToManyField(Product)
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(default=timezone.now)
    address = models.ForeignKey(
        CustomerAddress,
        on_delete=models.CASCADE,
    )
    delivery_details = models.TextField(blank=True)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.id


# failed to put cart model in customer app due to circular import issues
class Cart(models.Model):
    customer = models.OneToOneField(
        CustomerProfile,
        on_delete=models.CASCADE
    )
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
    quantity = models.IntegerField(default=1)

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


def customer_post_save(instance: CustomerProfile, *args, **kwargs):
    if not instance.cart:
        cart = Cart.objects.create(customer=instance)
        cart.save()


signals.post_save.connect(customer_post_save, sender=CustomerProfile)
