from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from customer.models import Review


def toggle_is_approved(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.approved = not review.approved
    review.save()

    return redirect(reverse('admin:customer_review_changelist'))
