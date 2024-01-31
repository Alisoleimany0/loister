from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        post_migrate.connect(create_required_objects, sender=self)


def create_required_objects(sender, **kwargs):
    from customer.models import CustomerProfile
    from cart.models import Cart
    for customer in CustomerProfile.objects.all():
        cart = Cart.objects.filter(customer=customer)
        if not cart:
            Cart.objects.create(customer=customer)
