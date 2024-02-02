from ckeditor_uploader.fields import RichTextUploadingField
from denorm import denormalized
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django_jalali.db import models as jmodels

from customer.models import CustomerProfile


class Category(models.Model):
    name = models.CharField(verbose_name="نام", max_length=20)

    class Meta:
        verbose_name_plural = "3. دسته بندی ها"
        verbose_name = "دسته بندی"

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name="نام", max_length=20)

    class Meta:
        verbose_name_plural = "4. نوع های محصول"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="نام محصول", max_length=40)
    slug = models.SlugField(verbose_name="slug", unique=True, allow_unicode=True, max_length=255)
    type = models.ForeignKey(ProductType, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="نوع")
    display_description = models.CharField(verbose_name="توضیحات نمایشی", max_length=500, default='', blank=True, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name="دسته‌بندی")
    release_date = models.DateField(verbose_name="تاریخ انتشار", default=timezone.now)
    views = models.BigIntegerField(verbose_name="تعداد بازدید", default=0)
    star = models.IntegerField(verbose_name="امتیاز", default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    price = models.DecimalField(verbose_name="قیمت", default=0, decimal_places=0, max_digits=12)
    is_on_sale = models.BooleanField(verbose_name="موجود در جشنواره", default=False)
    sale_price = models.DecimalField(verbose_name="قیمت فروش", default=0, decimal_places=0, max_digits=12)

    class Meta:
        verbose_name_plural = "1. محصول ها"
        verbose_name = "محصول"

    @property
    def sell_price(self):
        if self.is_on_sale:
            return self.sale_price
        else:
            return self.price

    @denormalized(models.IntegerField, default=0)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    title = models.CharField(verbose_name="عنوان", max_length=50)
    details = models.CharField(verbose_name="جزئیات", max_length=200)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    image = models.ImageField(null=True, upload_to='upload/product/', verbose_name="تصویر")
    is_default = models.BooleanField(default=False, verbose_name="تصویر پیش‌فرض")

    def save(self, *args, **kwargs):
        images = ProductImage.objects.filter(product=self.product)
        if not images:
            self.is_default = True
        super().save(*args, **kwargs)


class ProductOffers(models.Model):
    products = models.ManyToManyField(Product, blank=True, verbose_name="محصولات")
    finish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان پایان")
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name="عنوان")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")

    def save(self, *args, **kwargs):
        # make sure we're not updating
        if not self.pk and ProductOffers.objects.exists():
            raise ValidationError("You can only create one instance of ProductOffers")
        return super(ProductOffers, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "پیشنهاد"
        verbose_name_plural = "پشنهاد ها"

    def __str__(self):
        return "Product Offers"


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("2payment", "در انتظار پرداخت"),
        ("1processing", "پرداخت شده"),
        ("3sent", "ارسال شده"),
    )
    customer = models.ForeignKey(CustomerProfile, null=True, on_delete=models.SET_NULL, verbose_name="مشتری")
    session = models.CharField(max_length=100, null=True, verbose_name="Session")
    checkout_date = jmodels.jDateTimeField(blank=True, default=timezone.now, verbose_name="تاریخ پرداخت")
    customer_full_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="نام و نام خانوادگی")
    invoice_date_time = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ و زمان صدور فاکتور")
    total_price = models.DecimalField(verbose_name="قیمت کل", max_digits=12, decimal_places=0)
    delivery_phone_number = models.CharField(verbose_name="شماره تلفن تحویل‌گیرنده", max_length=15)
    district = models.CharField(verbose_name="منطقه", max_length=20)
    city = models.CharField(verbose_name="شهر", max_length=20)
    address_text = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(verbose_name="کد پستی", default=0, null=False, max_length=10)
    additional_info = models.TextField(verbose_name="اطلاعات تکمیلی", blank=True)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20, verbose_name="وضعیت سفارش")

    class Meta:
        verbose_name_plural = "2. سفارش ها"
        verbose_name = "سفارش"
        ordering = ('-checkout_date',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.id}"


class BoughtProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="محصول")
    name = models.CharField(verbose_name="نام", max_length=50)
    price = models.DecimalField(verbose_name="قیمت", max_digits=12, decimal_places=0)
    total_price = models.DecimalField(verbose_name="قیمت کل", max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField(verbose_name="تعداد")


def pre_product_image_save(sender, instance, **kwargs):
    if not ProductImage.objects.all():
        instance.is_default = True


signals.pre_save.connect(pre_product_image_save, sender=ProductImage)
