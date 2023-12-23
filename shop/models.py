from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.firstname} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='upload/product/')
    star = models.CharField(max_length=5, default='0', validators=[MaxLengthValidator(5), MinValueValidator('0')])
    # star = models.IntegerField(default=0 , validators=[MaxLengthValidator(5), MinValueValidator(0)])
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=400, default='', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name}'


class Background(models.Model):
    title = models.CharField(blank=True, max_length=30)
    description = models.CharField(blank=True, max_length=100)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title
