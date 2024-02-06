from django.middleware.csrf import get_token

from customer.models import CustomerProfile
from site_configs.models import ContactUs, SiteInfo, ETrustSymbol


def my_context_processor(request):
    contact_us = ContactUs.objects.first()
    site_info: SiteInfo = SiteInfo.objects.first()
    symbols = ETrustSymbol.objects.all()
    csrf_token = get_token(request)
    context = {'contact_us': contact_us, 'site_info': site_info, 'symbols': symbols, 'csrf_token': csrf_token}
    if request.user.is_authenticated:
        customer = CustomerProfile.objects.filter(user=request.user).first()
        context['user_name'] = customer.full_name
    return context
