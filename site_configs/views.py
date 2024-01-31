from django.shortcuts import render

from site_configs.models import ContactUs, SocialLink


def contact_us(request):
    info = ContactUs.objects.first()
    links = SocialLink.objects.all()
    context = {'info': info, 'links': links}
    return render(request, "contact.html", context)
