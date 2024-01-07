from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .forms import SignupForm
from .models import Category, Product, HomepageCover, ProductImage, ProductOffers, ProductProperty


def index_view(request):
    all_products = Product.objects.all()
    order_by_date = all_products.order_by("release_date")[0:7]
    # TODO: change to correct order by
    order_by_units_sold = all_products.order_by("release_date")[0:7]
    order_by_views = all_products.order_by("views")[0:7]
    all_categories = Category.objects.all()
    covers = HomepageCover.objects.all()
    product_offers = ProductOffers.objects.first()
    offer_seconds_remaining = (product_offers.finish_time - timezone.now()).seconds

    return render(request, "shop/index.html",
                  {'products_by_date': order_by_date, 'products_by_sold': order_by_units_sold,
                   'products_by_views': order_by_views, 'covers': covers,
                   "all_categories": all_categories,
                   'offered_products': product_offers.products.all() if product_offers else (),
                   'offer_seconds_remaining': offer_seconds_remaining,
                   'index': True})


def product_single(request, pk):
    product = Product.objects.get(id=pk)
    images = ProductImage.objects.filter(product=product)
    category = Product.category
    properties = ProductProperty.objects.filter(product=product)
    return render(request, "shop/product_single.html",
                  {'product': product, 'product_images': images, 'category': category,
                   'product_properties': properties})


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("home")
        else:
            messages.error(request, "اشکال در ورود")
            return redirect("login")
    else:
        return render(request, 'shop/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("با موفقیت خارج شدید!"))
    return redirect("home")


def signup_user(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "اکانت شما ساخته شد")
            return redirect("home")
        else:
            messages.error(request, "مشکلی در ثبت نام شما وجود دارد")
            return redirect("signup")
    else:
        return render(request, "signup.html", {'form': form})


def category_view(request, cat):
    cat = cat.replace("-", " ")
    category = get_object_or_404(Category, name=cat)
    products = Product.objects.filter(category=category)
    all_categories = Category.objects.all()
    return render(request, "category.html",
                  {'products': products, "category": category, "all_categories": all_categories})
