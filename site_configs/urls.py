from django.urls import path

from site_configs import views

urlpatterns = [
    path('contact/', views.contact_us_view, name='contact'),
    path('about/', views.about_us_view, name='about'),
    path('contact/send', views.contact_message_view, name='contact_message')
]
