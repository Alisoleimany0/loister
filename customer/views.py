from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from customer.models import Review, CustomerProfile
from loister import utils


def toggle_is_approved(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.approved = not review.approved
    review.save()

    return redirect(reverse('admin:customer_review_changelist'))


def update_profile_view(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    request.user.first_name = request.POST.get("first_name")
    request.user.last_name = request.POST.get("last_name")
    customer.user_phone_number = request.POST.get("phone_number")
    request.user.email = request.POST.get("email")
    if request.POST.get("password", None):
        request.user.set_password(request.POST['password'])
    request.user.save()
    customer.save()
    return utils.get_back_reload_response(request)
