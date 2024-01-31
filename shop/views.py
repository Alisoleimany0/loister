# -*- coding: utf-8 -*-
import sys

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError, SuspiciousOperation, ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from site_configs.models import SocialLink, ContactUs, SiteInfo
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods

from customer.models import CustomerProfile, CustomerAddress, Review
from site_configs.models import HomepageCover
from .forms import SignupForm
from .models import Category, Product, ProductImage, ProductOffers, ProductDetail, Order, BoughtProduct, ProductType
from cart.models import Cart, CartProductQuantity


def expire_session(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session.set_expiry(86400)
        return func(request, *args, **kwargs)

    return wrapper


@expire_session
def index_view(request):
    all_products = Product.objects.all()
    order_by_date = all_products.order_by("release_date")[0:7]
    order_by_units_sold = all_products.order_by("units_sold")[0:7]
    order_by_views = all_products.order_by("views")[0:7]
    all_categories = Category.objects.all()
    covers = HomepageCover.objects.all()
    product_offers = ProductOffers.objects.first()
    description = Product.objects.all()
    offer_seconds_remaining = offer_days_remaining = None
    if product_offers:
        offer_remaining = (product_offers.finish_time - timezone.now())
        offer_seconds_remaining = offer_remaining.seconds
        offer_days_remaining = offer_remaining.days
        if offer_days_remaining < 0:
            offer_seconds_remaining = 0
            offer_days_remaining = 0

    context = {'products_by_date': order_by_date,
               'products_by_sold': order_by_units_sold,
               'products_by_views': order_by_views,
               'covers': covers,
               "all_categories": all_categories,
               'product_offers': product_offers,
               'offered_products': product_offers.products.all() if product_offers else (),
               'description': description,
               #    'description': description_value,
               'offer_seconds_remaining': offer_seconds_remaining,
               'offer_days_remaining': offer_days_remaining,
               'index': True}

    return render(request, "shop/index.html", context)


@expire_session
def product_single(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = ProductImage.objects.filter(product=product)
    category = Product.category
    properties = ProductDetail.objects.filter(product=product)
    reviews = Review.objects.filter(product=product, approved=True, parent=None)

    context = {'in_cart': 0, 'reviews': reviews}

    if request.user.is_authenticated:
        cart = Cart.objects.filter(customer__user=request.user)
    else:
        cart = Cart.objects.filter(session=request.session.session_key, customer=None)

    try:
        product_quantity = CartProductQuantity.objects.get(product=product, cart=cart.first())
        number_in_cart = product_quantity.quantity
        context['in_cart'] = number_in_cart
    except ObjectDoesNotExist:
        pass

    context['product'] = product
    context['product_images'] = images
    context['category'] = category
    context['product_properties'] = properties
    context['user'] = request.user
    return render(request, "shop/product_single.html", context)


@expire_session
def about(request):
    return render(request, 'shop/about.html')


@expire_session
def logout_user(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
    return redirect("home")


@expire_session
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


@expire_session
def category_view(request, cat):
    cat = cat.replace("-", " ")
    category = get_object_or_404(Category, name=cat)
    products = Product.objects.filter(category=category)
    all_categories = Category.objects.all()
    return render(request, "shop/category.html",
                  {'products': products, "category": category, "all_categories": all_categories})


@expire_session
def cart_view(request):
    if request.user.is_authenticated:
        items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
        sub_total = 0
        for item in items:
            sub_total += item.total_price
        context = {'items': items, 'sub_total': sub_total}
        return render(request, "shop/cart.html", context)
    else:
        if not request.session.session_key:
            request.session.save()
        if Cart.objects.filter(session=request.session.session_key, customer=None):
            cart = Cart.objects.get(session=request.session.session_key, customer=None)
        else:
            cart = Cart.objects.create(session=request.session.session_key)
        items = CartProductQuantity.objects.filter(cart=cart)
        sub_total = 0
        for item in items:
            sub_total += item.total_price
        context = {'items': items, 'sub_total': sub_total}
        return render(request, "shop/cart.html", context)


@expire_session
def add_cart_view(request):
    if request.user.is_authenticated:
        if request.GET.get("id", None) and request.GET.get("quantity", None):
            product = get_object_or_404(Product, id=request.GET['id'])
            cart = Cart.objects.filter(customer__user=request.user)
            if not cart:
                raise SuspiciousOperation()

            cart_product = CartProductQuantity.objects.get_or_create(product=product, cart=cart.first())[0]
            cart_product.quantity += int(request.GET['quantity'])
            cart_product.save()
            return redirect("product", product.slug)
    else:
        if not request.session.session_key:
            request.session.save()
        if request.GET.get("id", None) and request.GET.get("quantity", None):
            product = get_object_or_404(Product, id=request.GET['id'])
            anonymous_cart = Cart.objects.get_or_create(session=request.session.session_key, customer=None)
            cart_product = CartProductQuantity.objects.get_or_create(product=product, cart=anonymous_cart[0])[0]
            cart_product.quantity += int(request.GET['quantity'])
            cart_product.save()
            return redirect("product", product.slug)


@expire_session
def remove_cart_item_view(request):
    if request.POST.get("item_id", None):
        get_object_or_404(CartProductQuantity, id=request.POST.get("item_id")).delete()

    return redirect("cart")


@expire_session
def new_order_view(request):
    addresses = None
    customer = None
    if request.user.is_authenticated:
        items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
        addresses = CustomerAddress.objects.filter(customer__user=request.user)
        customer = CustomerProfile.objects.filter(user=request.user).first()
    else:
        items = CartProductQuantity.objects.filter(cart__session=request.session.session_key)
    sub_total = 0
    for item in items:
        sub_total += item.total_price
    context = {'addresses': addresses, 'items': items, 'sub_total': sub_total, 'customer': customer}
    return render(request, 'shop/purchase.html', context)


@expire_session
def coming_soon_view(request):
    return render(request, 'under_development.html')


@expire_session
def payment_redirect_view(request):
    if request.method == 'POST':
        if request.POST.get("state", None):
            customer = None
            session = None
            if request.user.is_authenticated:
                customer = CustomerProfile.objects.get(user=request.user)
                items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
            else:
                session = request.session.session_key
                items = CartProductQuantity.objects.filter(cart__session=session)
            sub_total = 0
            for item in items:
                sub_total += item.total_price
            order = Order.objects.create(customer=customer,
                                         session=session,
                                         total_price=sub_total,
                                         order_status=Order.ORDER_STATUS_CHOICES[0][0],
                                         customer_full_name=request.POST['full_name'],
                                         delivery_phone_number=request.POST['mobile'],
                                         district=request.POST['state'],
                                         city=request.POST['city'],
                                         postal_code=request.POST['postal_code'],
                                         address_text=request.POST['address'],
                                         additional_info=request.POST.get("additional_info"))

            for item in items:
                BoughtProduct.objects.create(order=order, product=item.product, quantity=item.quantity,
                                             name=item.product.name, price=item.sell_price,
                                             total_price=item.total_price)
            post_copy = request.POST.copy()
            post_copy["order_id"] = order.id
            # TODO this is for testing. Remove after implementing payment
            post_copy['code'] = "200"
            request.session['_post_data'] = post_copy
            return redirect("payment_confirmation")


@expire_session
def payment_confirmation_view(request):
    """method that handle bank's API callback"""
    # TODO properly handle api callback
    if request.session['_post_data']['code'] == "200" and request.session['_post_data']['order_id']:
        order = Order.objects.get(id=int(request.session['_post_data']["order_id"]))
        order.order_status = Order.ORDER_STATUS_CHOICES[1][0]
        order.save()
        if request.user.is_authenticated:
            CartProductQuantity.objects.filter(cart__customer__user=request.user).delete()
        else:
            CartProductQuantity.objects.filter(cart__session=request.session.session_key, cart__customer=None).delete()

        return redirect("home")


@expire_session
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


@expire_session
def remove_address_view(request, pk):
    if request.user.is_authenticated:
        get_object_or_404(CustomerAddress, id=pk).delete()
        return HttpResponse("""
                            <script>
                            sessionStorage.setItem('reload', 'true');
                            history.back();
                            </script>
                            """)
    return redirect("logup")


@expire_session
def profile_info_view(request):
    if request.user.is_authenticated:
        customer = CustomerProfile.objects.get(user=request.user)
        context = {'user': request.user, 'customer': customer}
        return render(request, 'user_profile/profile_info.html', context)
    return redirect("logup")


@expire_session
def profile_purchase_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer__user=request.user)
        context = {'orders': orders}
        return render(request, 'user_profile/purchase-history.html', context)
    return redirect("logup")


@expire_session
def browse_view(request, ):
    products = Product.objects.all().order_by("release_date")
    all_categories = Category.objects.all()
    category = None
    search = None
    if request.GET.get("cat", None):
        category = Category.objects.get(id=request.GET['cat'])
        products = products.filter(category=category)
    if request.GET.get("search", None):
        products = products.filter(name__iregex=request.GET['search'])
        search = request.GET['search']
    paginator = Paginator(products, 10)
    try:
        page_num = request.GET.get('page')
        page_object = paginator.page(page_num)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(1)
    products = page_object
    ptypes = ProductType.objects.all()

    last_query = request.GET.dict()
    last_query['ptype'] = request.GET.getlist('ptype')

    context = {"categories": all_categories, 'products': products, 'category': category, 'search': search,
               'last_query': last_query, 'ptypes': ptypes}

    return render(request, "shop/browse.html", context)


@expire_session
def wishlist_view(request):
    if request.user.is_authenticated:
        favourites = CustomerProfile.objects.get(user=request.user).favourites
        products = favourites.all()
        if request.GET.get("remove_favourite", None):
            favourites.remove(request.GET.get("remove_favourite"))
        context = {'products': products}
        return render(request, "shop/wishlist.html", context)
    return HttpResponse("<script>history.back();</script>")


@expire_session
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


@expire_session
def new_review(request, slug):
    if request.POST and request.user.is_authenticated:
        try:
            author = CustomerProfile.objects.get(user=request.user)
            rating = request.POST.get("rating", None)
            content = request.POST['content']

            Review.objects.create(product=get_object_or_404(Product, slug=slug), author=author, rating=rating,
                                  content=content)
            return redirect('product', slug)
        except MultiValueDictKeyError:
            pass
    raise SuspiciousOperation()


@expire_session
def toggle_wishlist(request, is_favourite, pk, next):
    if request.user.is_authenticated:
        if eval(is_favourite):
            CustomerProfile.objects.get(user=request.user).favourites.remove(Product.objects.get(id=pk))
        else:
            CustomerProfile.objects.get(user=request.user).favourites.add(Product.objects.get(id=pk))

    # url = reverse(next)
    # # Append the fragment
    # url_with_fragment = f'{url}#product{pk}'
    # # Redirect to the URL with the fragment
    # return redirect(url_with_fragment)
    return HttpResponse("""
                        <script>
                        sessionStorage.setItem('reload', 'true');
                        history.back();
                        </script>
                        """)
