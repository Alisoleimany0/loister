from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from customer.models import Review


# Create your views here.
def toggle_is_approved(request, pk):
    obj = get_object_or_404(Review, pk=pk)
    obj.approved = not obj.approved
    obj.save()

    return redirect(reverse('admin:customer_review_changelist'))
