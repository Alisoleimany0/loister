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
    path('cart/remove_item', views.remove_cart_item_view, name="remove_cart_item")
]
