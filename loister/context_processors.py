from django.middleware.csrf import get_token

from site_configs.models import ContactUs, SiteInfo


def my_context_processor(request):
    contact_us = ContactUs.objects.first()
    site_info = SiteInfo.objects.first()
    csrf_token = get_token(request)
    print(csrf_token)
    return {'contact_us': contact_us, 'site_info': site_info, 'csrf_token': csrf_token}
