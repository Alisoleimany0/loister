from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from customer.models import CustomerProfile, CustomerAddress, Review


class AddressInline(admin.TabularInline):
    model = CustomerAddress


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    inlines = AddressInline,

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user']
        else:
            return []


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'toggle_is_approved']

    def toggle_is_approved(self, obj):
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('customer_review_approved', args=[obj.pk]),
            'Disapprove' if obj.approved else 'Approve'
        )

    toggle_is_approved.short_description = 'Is Approved'
