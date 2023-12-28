from django.contrib import admin
from .models import HomepageCover, HomepageCoverGroup, ProductProperty, Product, Category, Order

admin.site.register(Category)
admin.site.register(Order)


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty


class HomepageCoverInline(admin.TabularInline):
    model = HomepageCover


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = ProductPropertyInline,


@admin.register(HomepageCoverGroup)
class HomepageCoverGroupAdmin(admin.ModelAdmin):
    inlines = HomepageCoverInline,
