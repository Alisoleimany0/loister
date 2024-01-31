from site_configs.models import ContactUs, SiteInfo


def my_context_processor(request):
    contact_us = ContactUs.objects.first()
    site_info = SiteInfo.objects.first()
    return {'contact_us': contact_us, 'site_info': site_info}
