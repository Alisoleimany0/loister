from django import template

from cart.models import CartProductQuantity
from customer.models import CustomerProfile, Review
from shop.models import Product
register = template.Library()


@register.filter()
def is_favourite(user, product):
    if user.is_authenticated:
        customer = CustomerProfile.objects.filter(user=user)
        if customer:
            return product.is_favourite(customer=customer[0])
    return False


@register.inclusion_tag("shop/review_reply_widget.html")
def review_reply_widget(parent: Review, product: Product):
    replies = Review.objects.filter(parent=parent, approved=True)
    return {'replies': replies, 'product': product}


@register.inclusion_tag("shop/product_card_widget.html")
def product_card_widget(product: Product, user, request, *args):
    context = {'product': product, 'user': user, 'request': request}
    try:
        cpq = CartProductQuantity.objects.filter(cart__customer__user=request.user, product=product).first()
        if cpq:
            context['number_in_cart'] = cpq.quantity
        else:
            context['number_in_cart'] = 0
        if args[0]:
            context['remove_div'] = args[0]
    except IndexError:
        pass
    return context
