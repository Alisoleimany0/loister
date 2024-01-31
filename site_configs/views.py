from django.http import HttpResponse
from django.shortcuts import render, redirect

from site_configs.models import ContactUs, SocialLink, UserContactMessage, AboutUs, Rules


def contact_us_view(request):
    info = ContactUs.objects.first()
    links = SocialLink.objects.all()
    context = {'info': info, 'links': links}
    return render(request, "contact.html", context)


def about_us_view(request):
    about = AboutUs.objects.first()
    context = {'about': about}
    return render(request, "about.html", context=context)


def contact_message_view(request):
    if request.POST:
        if request.POST.get("name") and request.POST.get("email") and request.POST.get("message"):
            UserContactMessage.objects.create(name=request.POST['name'], email=request.POST['email'],
                                              message=request.POST['message'])
        else:
            return HttpResponse("<script>history.back();</script>")

    # TODO: success
    return redirect("contact")


def rules_view(request):
    rules = Rules.objects.first()
    context = {'rules': rules}
    return render(request, "rules.html", context=context)
