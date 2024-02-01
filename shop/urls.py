from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="home"),
    path('about/', views.about, name="about"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.signup_user, name="signup"),
    path('customer/login/', views.logup_view, name="logup"),
    path('product/<str:slug>/', views.product_single, name="product"),
    path('product/<str:slug>/review/', views.new_review, name="product_review"),
    path('cart/', views.cart_view, name="cart"),
    path('cart/add_product/', views.add_cart_view, name="add_cart"),
    path('cart/remove_item/', views.remove_cart_item_view, name="remove_cart_item"),
    path('order/new/', views.new_order_view, name="new_order"),
    path('customer/addresses/', views.profile_addresses_view, name="profile_addresses"),
    path('customer/addresses/remove/<int:pk>', views.remove_address_view, name="remove_address"),
    path('customer/info/', views.profile_info_view, name="profile_info"),
    path('customer/purchase_history/', views.profile_purchase_history, name="profile_purchase_history"),
    path('soon/', views.coming_soon_view, name="coming_soon"),
    path('payment_redirect/', views.payment_redirect_view, name="payment_redirect"),
    path('payment_confirmation/', views.payment_confirmation_view, name="payment_confirmation"),
    path('browse/', views.browse_view, name="browse"),
    path('order/<int:pk>/set_complete/', views.order_set_complete_view, name="order_set_complete"),
    path('wishlist/', views.wishlist_view, name="wishlist"),
    path('wishlist/<str:is_favourite>/<int:pk>/<str:next>/', views.toggle_wishlist, name="toggle_wishlist")
]
