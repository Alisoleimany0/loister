from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="home"),
    path('about/', views.about, name="about"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.signup_user, name="signup"),
    path('customer/login/', views.logup_view, name="logup"),
    path('product/<int:pk>/', views.product_single, name="product"),
    path('product/<int:pk>/review/', views.new_review, name="product_review"),
    path('cart/', views.cart_view, name="cart"),
    path('cart/remove_item/', views.remove_cart_item_view, name="remove_cart_item"),
    path('order/new/', views.new_order_view, name="new_order"),
    path('customer/addresses/', views.profile_addresses_view, name="profile_addresses"),
    path('customer/info/', views.profile_info_view, name="profile_info"),
    path('customer/purchase_history/', views.profile_purchase_history, name="profile_purchase_history"),
    path('soon/', views.coming_soon_view, name="coming_soon"),
    path('payment_redirect/', views.payment_redirect_view, name="payment_redirect"),
    path('payment_confirmation/', views.payment_confirmation_view, name="payment_confirmation"),
    # path('browse/<int:page>', views.browse_view, name="browse_page"),
    path('browse/', views.browse_view, name="browse"),
    # path('browse/<int:cat>/<int:page>/', views.category_view, name="category_page"),
    # path('browse/<int:cat>/', views.browse_view, name="category"),
    path('wishlist/', views.wishlist_view, name="wishlist"),
    path('wishlist/<str:is_favourite>/<int:pk>/<str:next>/', views.toggle_wishlist, name="toggle_wishlist")
]
