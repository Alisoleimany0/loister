from django.contrib import admin
from django.db import models

from shop.admin import ImageWidget
from site_configs.models import ContactUs, SocialLink, SiteInfo, HomepageCoverGroup, HomepageCover, Rules, \
    UserContactMessage


class HomepageCoverInline(admin.TabularInline):
    model = HomepageCover
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}


class SocialLinkInline(admin.TabularInline):
    model = SocialLink


@admin.register(HomepageCoverGroup)
class HomepageCoverGroupAdmin(admin.ModelAdmin):
    inlines = HomepageCoverInline,


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    inlines = SocialLinkInline,


@admin.register(SiteInfo)
class SiteFaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    pass


@admin.register(UserContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    pass
