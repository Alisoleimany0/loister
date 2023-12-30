from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.forms import RadioSelect
from django.utils.safestring import mark_safe

from .forms import ProductAdminForm
from .models import HomepageCover, HomepageCoverGroup, ProductProperty, Product, Category, Order, ProductImage

admin.site.register(Category)
admin.site.register(Order)


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty


class ProductImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150" style="object-fit: cover;"/></a> %s ' % \
                (image_url, image_url, file_name, ''))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['is_default']
    formfield_overrides = {
        models.ImageField: {'widget': ProductImageWidget}}


class HomepageCoverImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  '
                u'style="object-fit: cover;"/></a> %s ' % \
                (image_url, image_url, file_name, ''))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class HomepageCoverInline(admin.TabularInline):
    model = HomepageCover
    formfield_overrides = {models.ImageField: {'widget': ProductImageWidget}}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = ProductPropertyInline, ProductImageInline
    form = ProductAdminForm

    def save_related(self, request, form, formsets, change):
        super(ProductAdmin, self).save_related(request, form, formsets, change)
        if 'pictures' in formsets:
            for formset in formsets['pictures']:
                for form in formset:
                    if form.cleaned_data.get('is_default'):
                        # Unset previous default pictures
                        ProductImage.objects.filter(product=form.instance.product).exclude(pk=form.instance.pk).update(
                            is_default=False)


@admin.register(HomepageCoverGroup)
class HomepageCoverGroupAdmin(admin.ModelAdmin):
    inlines = HomepageCoverInline,
