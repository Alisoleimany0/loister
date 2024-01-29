from django.contrib import admin

from site_configs.models import ContactUs, SocialLink, SiteFace


# Register your models here.

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialLink)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteFace)
class ContactUsAdmin(admin.ModelAdmin):
    pass
