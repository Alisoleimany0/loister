from django.contrib import admin
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
    list_display = ['author', 'action_checkbox', 'approved']
