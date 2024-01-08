from django import template

from customer.models import CustomerProfile

register = template.Library()


@register.filter()
def is_favourite(user, product):
    if user.is_authenticated:
        customer = CustomerProfile.objects.filter(user=user)
        if customer:
            return product.is_favourite(customer=customer[0])
