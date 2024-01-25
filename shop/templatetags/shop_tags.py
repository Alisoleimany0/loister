from django import template

from customer.models import CustomerProfile, Review

register = template.Library()


@register.filter()
def is_favourite(user, product):
    if user.is_authenticated:
        customer = CustomerProfile.objects.filter(user=user)
        if customer:
            return product.is_favourite(customer=customer[0])


@register.inclusion_tag("shop/review_reply_widget.html")
def review_reply_widget(parent: Review):
    replies = Review.objects.filter(parent=parent, approved=True)
    return {'replies': replies}
