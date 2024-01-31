from django.urls import path

from site_configs import views

urlpatterns = [
    path('contact/', views.contact_us, name='contact'),
]
