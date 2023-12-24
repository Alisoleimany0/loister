from django.contrib import admin
from django.contrib.auth.models import User

from customer.models import CustomerProfile, Address

admin.site.unregister(User)


class CustomerProfileInline(admin.TabularInline):
    model = CustomerProfile


class AddressInline(admin.TabularInline):
    model = Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = CustomerProfileInline,


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'user_phone_number']
    inlines = AddressInline,
