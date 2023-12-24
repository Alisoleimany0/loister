from django.contrib import admin
from . import models
from .models import HomepageCover, HomepageCoverGroup

admin.site.register(models.Category)
admin.site.register(models.CustomerProfile)
admin.site.register(models.Product)
admin.site.register(models.Order)


class HomepageCoverInline(admin.TabularInline):
    model = HomepageCover


@admin.register(HomepageCoverGroup)
class HomepageCoverGroupAdmin(admin.ModelAdmin):
    inlines = HomepageCoverInline,
