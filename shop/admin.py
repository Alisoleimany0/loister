from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.urls import reverse
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django_jalali.admin.filters import JDateFieldListFilter

from .models import ProductDetail, Product, Category, Order, ProductImage, \
    ProductOffers, ProductType, ProductWeight

admin.site.register(Category)


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


class ProductAdminForm(forms.ModelForm):
    default_image_choice = CustomChoiceField(
        queryset=ProductImage.objects.none(),
        widget=forms.RadioSelect,
        required=False,
        label='تصویر اصلی'
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # self.fields[default_image_choice]
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
    list_display = ['id', 'name', 'type', 'is_available']
    prepopulated_fields = {'slug': ('name',), }
    filter_horizontal = ['category']
    readonly_fields = ['release_date']
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
    list_display = ['id', 'customer_full_name', 'delivery_phone_number', 'formatted_date', 'total_price',
                    'set_to_complete', 'payment_track_id']
    search_fields = ['customer_full_name', 'delivery_phone_number', 'id', 'checkout_date', 'payment_track_id']

    list_filter = (
        ('checkout_date', JDateFieldListFilter),
    )
    readonly_fields = ['customer', 'session', 'invoice_date_time']

    def set_to_complete(self, obj):
        if obj.is_payment_successful:
            return format_html('<a class="button" href="{}">{}</a>', reverse('order_set_complete', args=[obj.pk]),
                               'نهایی کردن')
        elif obj.is_payment_pending:
            return "در انتظار پرداخت"
        elif obj.is_canceled:
            return "لغو شده"
        else:
            return "تکمیل شده"

    set_to_complete.short_description = 'وضعیت سفارش'

    def formatted_date(self, obj):
        if obj.checkout_date:
            return obj.checkout_date.strftime('%Y-%m-%d, ساعت %H:%M')  # Format the date as you like
        else:
            return "-"

    formatted_date.short_description = 'تاریخ پرداخت'  # Column header

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request).order_by('order_status', '-checkout_date')
        return qs


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductWeight)
class ProductWeightAdmin(admin.ModelAdmin):
    pass
