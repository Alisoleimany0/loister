from django.db import models


class Cart(models.Model):
    customer = models.OneToOneField(
        'customer.CustomerProfile',
        null=True,
        on_delete=models.CASCADE
    )
    session = models.CharField(max_length=100, null=True, blank=True)
    products = models.ManyToManyField('shop.Product', through='CartProductQuantity')


class CartProductQuantity(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'cart', 'weight'], name='product_cart_constraint')
        ]

    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)
    weight = models.CharField(max_length=20, null=True)

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



