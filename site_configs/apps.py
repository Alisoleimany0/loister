from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SiteConfigsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_configs'
    verbose_name = '1. پیکربندی سایت'

    def ready(self):
        post_migrate.connect(create_required_objects, sender=self)


def create_required_objects(sender, **kwargs):
    from site_configs.models import ContactUs, SiteInfo, HomepageCoverGroup, Rules, AboutUs
    if not ContactUs.objects.all():
        ContactUs.objects.create()
    if not SiteInfo.objects.all():
        SiteInfo.objects.create()
    if not HomepageCoverGroup.objects.all():
        HomepageCoverGroup.objects.create()
    if not Rules.objects.all():
        Rules.objects.create()
    if not AboutUs.objects.all():
        AboutUs.objects.create()
