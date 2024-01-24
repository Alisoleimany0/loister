from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from customer.models import CustomerProfile, CustomerAddress
from .forms import SignupForm
from .models import Category, Product, HomepageCover, ProductImage, ProductOffers, ProductDetail, Cart, \
    CartProductQuantity, Order, BoughtProduct


def index_view(request):
    all_products = Product.objects.all()
    order_by_date = all_products.order_by("release_date")[0:7]
    # TODO: change to correct order by
    order_by_units_sold = all_products.order_by("release_date")[0:7]
    order_by_views = all_products.order_by("views")[0:7]
    all_categories = Category.objects.all()
    covers = HomepageCover.objects.all()
    product_offers = ProductOffers.objects.first()
    offer_seconds_remaining = None
    if product_offers:
        offer_seconds_remaining = (product_offers.finish_time - timezone.now()).seconds

    context = {'products_by_date': order_by_date, 'products_by_sold': order_by_units_sold,
               'products_by_views': order_by_views, 'covers': covers,
               "all_categories": all_categories,
               'offered_products': product_offers.products.all() if product_offers else (),
               'offer_seconds_remaining': offer_seconds_remaining,
               'index': True}

    return render(request, "shop/index.html", context)


def product_single(request, pk):
    product = Product.objects.get(id=pk)
    images = ProductImage.objects.filter(product=product)
    category = Product.category
    properties = ProductDetail.objects.filter(product=product)

    context = {'in_cart': 0}

    if request.user.is_authenticated:
        cart = Cart.objects.filter(customer__user=request.user)
        if not cart:
            raise PermissionDenied()
        if request.POST.get("quantity", None):
            try:
                CartProductQuantity.objects.create(product_id=pk, cart=cart[0], quantity=request.POST.get("quantity"))
            except IntegrityError as exception:
                if "UNIQUE constraint failed" in exception.__str__():
                    cart_product = CartProductQuantity.objects.get(product_id=pk, cart=cart[0])
                    cart_product.quantity += int(request.POST.get("quantity"))
                    cart_product.save()
        if request.GET.get("add_favourite", None):
            CustomerProfile.objects.get(user=request.user).favourites.add(product)
        elif request.GET.get("remove_favourite", None):
            CustomerProfile.objects.get(user=request.user).favourites.remove(product)
        product_quantity = CartProductQuantity.objects.filter(product=product, cart=cart[0])
        if product_quantity:
            number_in_cart = product_quantity[0].quantity
            context['in_cart'] = number_in_cart
    context['product'] = product
    context['product_images'] = images
    context['category'] = category
    context['product_properties'] = properties
    context['user'] = request.user
    return render(request, "shop/product_single.html", context)


def about(request):
    return render(request, 'shop/about.html')


def logout_user(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
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
        return render(request, "shop/signup.html", {'form': form})


def category_view(request, cat):
    cat = cat.replace("-", " ")
    category = get_object_or_404(Category, name=cat)
    products = Product.objects.filter(category=category)
    all_categories = Category.objects.all()
    return render(request, "shop/category.html",
                  {'products': products, "category": category, "all_categories": all_categories})


def cart_view(request):
    if request.user.is_authenticated:
        items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
        sub_total = 0
        for item in items:
            sub_total += item.total_price
        context = {'items': items, 'sub_total': sub_total}
        return render(request, "shop/cart.html", context)
    # TODO properly handle this
    raise Http404


# TODO this is stupid. merge it with cart view
def remove_cart_item_view(request):
    if request.user.is_authenticated:
        items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
        if request.POST.get("item_id", None):
            items.get(id=request.POST.get("item_id")).delete()
        sub_total = 0
        for item in items:
            sub_total += item.total_price
        context = {'items': items, 'sub_total': sub_total}
        return render(request, "shop/cart.html", context)
    raise Http404


def new_order_view(request):
    if request.user.is_authenticated:
        items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
        addresses = CustomerAddress.objects.filter(customer__user=request.user)
        sub_total = 0
        for item in items:
            sub_total += item.total_price
        context = {'addresses': addresses, 'items': items, 'sub_total': sub_total}
        return render(request, 'shop/purchase.html', context)


def coming_soon_view(request):
    return render(request, 'under_development.html')


def payment_redirect_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.POST.get("address_id", None):
            address = CustomerAddress.objects.get(id=int(request.POST.get("address_id")))
            items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
            sub_total = 0
            for item in items:
                sub_total += item.total_price
            order = Order.objects.create(customer=CustomerProfile.objects.get(user=request.user),
                                         total_price=sub_total,
                                         order_status=Order.ORDER_STATUS_CHOICES[0][0],
                                         delivery_phone_number=address.delivery_phone_number,
                                         address=address,
                                         district=address.district,
                                         city=address.city,
                                         address_text=address.address,
                                         postal_code=address.postal_code)

            for item in items:
                BoughtProduct.objects.create(order=order, product=item.product, quantity=item.quantity,
                                             name=item.product.name, price=item.sell_price,
                                             total_price=item.total_price)
            post_copy = request.POST.copy()
            post_copy["order_id"] = order.id
            post_copy['code'] = "200"
            request.session['_post_data'] = post_copy
            return redirect("payment_confirmation")

    raise Http404


def payment_confirmation_view(request):
    if request.user.is_authenticated:
        # TODO properly handle api callback
        if request.session['_post_data']['code'] == "200" and request.session['_post_data']['order_id']:
            order = Order.objects.get(id=int(request.session['_post_data']["order_id"]))
            order.order_status = Order.ORDER_STATUS_CHOICES[1][0]
            order.save()
            CartProductQuantity.objects.filter(cart__customer__user=request.user).delete()
            return redirect("home")
    raise ValidationError("error")


def profile_addresses_view(request):
    if request.user.is_authenticated:
        if request.POST.get("state", None):
            CustomerAddress.objects.create(customer=CustomerProfile.objects.get(user=request.user),
                                           delivery_phone_number=request.POST.get("mobile", 0),
                                           district=request.POST.get("state"),
                                           city=request.POST.get("city"),
                                           address=request.POST.get("address"),
                                           postal_code=request.POST.get("postal_code"))

        addresses = CustomerAddress.objects.filter(customer__user=request.user)
        context = {'addresses': addresses}
        if request.POST.get("state", None):
            return redirect('profile_addresses')
        return render(request, 'user_profile/addresses.html', context)
    return redirect("logup")


def profile_info_view(request):
    if request.user.is_authenticated:
        customer = CustomerProfile.objects.get(user=request.user)
        context = {'user': request.user, 'customer': customer}
        return render(request, 'user_profile/profile_info.html', context)
    return redirect("logup")


def profile_purchase_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer__user=request.user)
        context = {'orders': orders}
        return render(request, 'user_profile/purchase-history.html', context)
    return redirect("logup")


def browse_view(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()

    context = {"all_categories": all_categories, 'products': all_products}

    return render(request, "shop/browse.html", context)


def wishlist_view(request):
    if request.user.is_authenticated:
        favourites = CustomerProfile.objects.get(user=request.user).favourites
        products = favourites.all()
        if request.GET.get("remove_favourite", None):
            favourites.remove(request.GET.get("remove_favourite"))
        context = {'products': products}
        return render(request, "shop/wishlist.html", context)
    raise Http404


def logup_view(request):
    if request.user.is_authenticated:
        return redirect("profile_info")
    if request.method == "POST":
        if request.POST.get("username", None) and request.POST.get("password", None):
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                return redirect("home")
            else:
                raise ValidationError("wrong credentials")
        else:
            raise ValidationError("fill fields")
    context = {'login_page': True}
    return render(request, 'login.html', context)
