from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.db.models import F, QuerySet
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .models import ProductDetail, Product, Category, Order, ProductImage, \
    ProductOffers, Cart, CartProductQuantity, BoughtProduct

admin.site.register(Category)
admin.site.register(Cart)


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail
    classes = ('collapse',)


class ImageWidget(AdminFileWidget):
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
        models.ImageField: {'widget': ImageWidget}}
    classes = ('collapse',)


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Shows an image with the label
        """
        image = conditional_escape(obj.image.url)
        title = conditional_escape(obj.product)

        label = """<img src="%s" alt="%s" width="150" height="150" style="object-fit: cover;"/>""" % (image, title)

        return mark_safe(label)


# class HorizontalRadioSelect(forms.RadioSelect):
#     user renderer template. the IDE won't be able to locate it
#     def render(self, name, value, attrs=None, renderer=None):
#         super().render(name, value, attrs, renderer=renderer)


class ProductAdminForm(forms.ModelForm):
    default_image_choice = CustomChoiceField(
        queryset=ProductImage.objects.none(),
        widget=forms.RadioSelect,
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            images = ProductImage.objects.filter(product=self.instance)
            if images:
                self.fields['default_image_choice'].queryset = images
                default_image = images.filter(is_default=True)
                if default_image:
                    self.fields['default_image_choice'].initial = default_image.first()

    def save(self, commit=True):
        images = ProductImage.objects.filter(product=self.instance)
        if images:
            images.update(is_default=False)
        chosen_image = self.cleaned_data['default_image_choice']
        if chosen_image:
            chosen_image.is_default = True
            chosen_image.save()
        return super().save(commit)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {'slug': ('name',), }
    inlines = ProductDetailInline, ProductImageInline
    form = ProductAdminForm

    def save_related(self, request, form, formsets, change):
        super(ProductAdmin, self).save_related(request, form, formsets, change)
        if 'pictures' in formsets:
            for formset in formsets['pictures']:
                for form in formset:
                    if form.cleaned_data.get('is_default'):
                        # Unset previous default pictures
                        ProductImage.objects.filter(product=form.instance.product_single).exclude(pk=form.instance.pk) \
                            .update(is_default=False)


@admin.register(ProductOffers)
class ProductOffersAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_full_name', 'delivery_phone_number', 'checkout_date', 'total_price', 'order_status']
    readonly_fields = ['customer', 'session']

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request).order_by('order_status')
        return qs
