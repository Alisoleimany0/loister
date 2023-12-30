from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import SignupForm
from .models import Category, Product, HomepageCoverGroup, HomepageCover, ProductImage


def helloworld(request):
    all_products = Product.objects.all()
    products_with_images = []
    for i in range(len(all_products)):
        default_image = ProductImage.objects.filter(product=all_products[i]).get(is_default=True)
        products_with_images.append({
            'product': all_products[i],
            'default_image': default_image
        })
    all_categories = Category.objects.all()
    covers = HomepageCover.objects.all()
    return render(request, "shop/index.html",
                  {'products': products_with_images, 'covers': covers, "all_categories": all_categories})


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


def product(request, pk):
    product = Product.objects.get(id=pk)
    category = Product.category
    print(category)     # error for showinh righ category
    return render(request, "shop/product.html",
                   {'product': product , 'category' : category})


def category(request, cat):
    cat = cat.replace("-", " ")
    category = get_object_or_404(Category, name=cat)
    products = Product.objects.filter(category=category)
    all_categories = Category.objects.all()
    return render(request, "category.html",
                  {'products': products, "category": category, "all_categories": all_categories})
