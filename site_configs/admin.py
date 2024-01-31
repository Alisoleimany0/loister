from django.contrib import admin
from django.db import models

from shop.admin import ImageWidget
from site_configs.models import ContactUs, SocialLink, SiteInfo, HomepageCoverGroup, HomepageCover, Rules


class HomepageCoverInline(admin.TabularInline):
    model = HomepageCover
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}


@admin.register(HomepageCoverGroup)
class HomepageCoverGroupAdmin(admin.ModelAdmin):
    inlines = HomepageCoverInline,


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialLink)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'link_address']


@admin.register(SiteInfo)
class SiteFaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    pass
