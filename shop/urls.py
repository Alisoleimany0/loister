from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="home"),
    path('about/', views.about, name="about"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.signup_user, name="signup"),
    path('product/<int:pk>', views.product_single, name="product"),
    path('category/<str:cat>', views.category_view, name="category"),
    path('cart/', views.cart_view, name="cart"),
    path('cart/remove_item', views.remove_cart_item_view, name="remove_cart_item"),
    path('order/new/', views.new_order_view, name="new_order"),
    path('customer/addresses', views.addresses_view, name="profile_addresses"),
    path('customer/info', views.profile_info_view, name="profile_info"),
    path('customer/purchase_history', views.profile_purchase_history, name="profile_purchase_history"),
    path('soon', views.coming_soon_view, name="coming_soon"),
    path('payment_redirect/', views.payment_redirect_view, name="payment_redirect"),
    path('payment_confirmation/', views.payment_confirmation_view, name="payment_confirmation"),
]
