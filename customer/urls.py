from django.contrib import admin
from django.urls import path, include

from customer import views

urlpatterns = [
    path('review/<int:pk>/toggle_approved/', views.toggle_is_approved, name='customer_review_approved'),
    path('info/update/', views.update_profile_view, name='customer_update_profile')
]
