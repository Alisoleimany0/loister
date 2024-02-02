from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = '3. فروشگاه'

    def ready(self):
        post_migrate.connect(create_required_objects, sender=self)


def create_required_objects(sender, **kwargs):
    from shop.models import ProductOffers
    if not ProductOffers.objects.all():
        ProductOffers.objects.create(title="", description="")
