from site_configs.models import ContactUs, SiteFace


def my_context_processor(request):
    contact_us = ContactUs.objects.first()
    site_face = SiteFace.objects.first()
    return {'contact_us': contact_us, 'site_face': site_face}
