import requests
import json
import re
from datetime import timedelta, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist, SuspiciousOperation, MultipleObjectsReturned, \
    PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from zibal.zibal import zibal

import loister.settings
from cart.models import Cart, CartProductQuantity
from customer.models import CustomerProfile, CustomerAddress, Review
from loister import utils
from site_configs.models import HomepageCover, SiteInfo, HomepageVideo, HomepageCoverGroup
from .models import Category, Product, ProductImage, ProductOffers, ProductDetail, Order, BoughtProduct, ProductType, \
    ProductWeight


@utils.expire_session
def index_view(request):
    all_products = Product.objects.all()
    order_by_date = all_products.order_by("release_date")[0:8]
    order_by_units_sold = all_products.order_by("units_sold")[0:8]
    order_by_views = all_products.order_by("-views")[0:8]
    all_categories = Category.objects.all()
    videos = None
    covers = None
    if HomepageCoverGroup.objects.first().show_video:
        videos = HomepageVideo.objects.all()
    else:
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
               'videos': videos,
               "all_categories": all_categories,
               'product_offers': product_offers,
               'offered_products': product_offers.products.all() if product_offers else (),
               'description': description,
               #    'description': description_value,
               'offer_seconds_remaining': offer_seconds_remaining,
               'offer_days_remaining': offer_days_remaining,
               'index': True}

    return render(request, "shop/index.html", context)


@utils.expire_session
def product_single(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # weights = product.weights.all()
    images = ProductImage.objects.filter(product=product)
    category = Product.category
    properties = ProductDetail.objects.filter(product=product)
    reviews = Review.objects.filter(product=product, approved=True, parent=None, content__iregex="^(?!\s*$).+")

    # context = {'in_cart': 0, 'reviews': reviews, 'weights': weights}
    context = {'in_cart': 0, 'reviews': reviews}

    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(product)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        product.views = hits
        product.save()
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    # ##
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
    except MultipleObjectsReturned:
        raise ValidationError("Error occurred contact server admin")
    related_products = Product.objects.filter(category__in=product.category.all()).distinct()
    context['product'] = product
    context['product_images'] = images
    context['category'] = category
    context['product_properties'] = properties
    context['user'] = request.user
    context['related_products'] = related_products

    return render(request, "shop/product_single.html", context)


@utils.expire_session
def logout_user(request):
    logout(request)
    return utils.get_toast_response(request, "با موفقیت خارج شدید", "success")


@utils.expire_session
def signup_user(request):
    if request.POST:
        if not User.objects.filter(username=request.POST['username']).exists():
            if not re.match(r"^[a-zA-z\d@_\-.]+$", request.POST['username']) or \
                    (request.POST['username']).__contains__("\\"):
                return utils.get_toast_response(request,
                                                "نام کاربری فقط میتواند ترکیبی از اعداد و حروف انگلیسی و _ @ . باشد",
                                                "danger")
            try:
                validate_password(request.POST['password'])
            except ValidationError as error:
                import sys
                error_str = ""
                for err in error.error_list:
                    error_str += err.message % err.params
                return utils.get_toast_response(request, error_str, "danger")
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            user.first_name = "کاربر"
            user.save()
            # note: CustomerProfile object will be created by django signal inside shop.models
            login(request, user)
            return utils.get_toast_response(request, "ثبت نام شما با موفقیت انجام شد", "success")

        return utils.get_toast_response(request, "این نام کاربری در سیستم وجود دارد. نام کاربری دیگری انتخاب کنید",
                                        "danger")
    raise Http404


@utils.expire_session
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
        # if Cart.objects.filter(session=request.session.session_key, customer=None):
        #     anonymous_cart = Cart.objects.get(session=request.session.session_key, customer=None)
        # else:
        #     anonymous_cart = Cart.objects.create(session=request.session.session_key)
        anonymous_cart = Cart.objects.get_or_create(session=request.session.session_key, customer=None)[0]

        items = CartProductQuantity.objects.filter(cart=anonymous_cart)
        sub_total = 0
        for item in items:
            sub_total += item.total_price
        context = {'items': items, 'sub_total': sub_total}
        return render(request, "shop/cart.html", context)


@utils.expire_session
def add_cart_view(request):
    if request.GET.get("id", None) and request.GET.get("quantity", None):
        product = get_object_or_404(Product, id=request.GET['id'])
        if not product.is_available:
            return utils.get_toast_response(request, "این کالا ناموجود است", "danger")
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(customer=get_object_or_404(CustomerProfile, user=request.user))
            cart = cart[0]
            cart_product = \
                CartProductQuantity.objects.get_or_create(product=product, cart=cart,
                                                          weight=request.GET.get('weight', None))[0]
            cart_product.quantity += int(request.GET['quantity'])
            if cart_product.quantity > cart_product.product.max_in_cart:
                return utils.get_toast_response(request,
                                                f"سقف سبد خرید این محصول {cart_product.product.max_in_cart} عدد است",
                                                "warning")
            cart_product.save()
        else:
            if not request.session.session_key:
                request.session.save()
            anonymous_cart = Cart.objects.get_or_create(session=request.session.session_key, customer=None)
            cart_product = CartProductQuantity.objects.get_or_create(product=product, cart=anonymous_cart[0],
                                                                     weight=request.GET.get('weight', None))[0]
            cart_product.quantity += int(request.GET['quantity'])
            if cart_product.quantity > cart_product.product.max_in_cart:
                return utils.get_toast_response(request,
                                                f"سقف سبد خرید این محصول {cart_product.product.max_in_cart} عدد است",
                                                "warning")
            cart_product.save()

        return utils.get_toast_response(request, f"{product.name} به سبد خرید اضافه شد", "success")
    return utils.get_toast_response(request, "درخواست نامتعارف!", "danger")


@utils.expire_session
def remove_cart_item_view(request):
    if request.POST.get("item_id", None):
        get_object_or_404(CartProductQuantity, id=request.POST.get("item_id")).delete()

    return redirect("cart")


def delete_all_cart(request):
    if request.user.is_authenticated:
        CartProductQuantity.objects.filter(cart__customer__user=request.user).delete()
    else:
        CartProductQuantity.objects.filter(cart__session=request.session.session_key).delete()
    return redirect('cart')


@utils.expire_session
def new_order_view(request):
    addresses = None
    customer = None
    if request.user.is_authenticated:
        items = CartProductQuantity.objects.filter(cart__customer__user=request.user)
        addresses = CustomerAddress.objects.filter(customer__user=request.user)
        customer = CustomerProfile.objects.filter(user=request.user).first()
    #     if Order.objects.filter(order_status=Order.ORDER_STATUS_CHOICES[0][0], customer=customer).exists():
    #         return utils.get_toast_response(request,
    #                                         "شما سفارش پرداخت نشده دارید. لطفا ابتدا از طریق پنل کاربری سفارش خود را پرداخت یا لغو کنید.",
    #                                         "warning")
    else:
    #     if Order.objects.filter(order_status=Order.ORDER_STATUS_CHOICES[0][0],
    #                             session=request.session.session_key).exists():
    #         return utils.get_toast_response(request,
    #                                         "شما سفارش پرداخت نشده دارید. لطفا ابتدا از طریق پنل کاربری سفارش خود را پرداخت یا لغو کنید.",
    #                                         "warning")
        items = CartProductQuantity.objects.filter(cart__session=request.session.session_key)
    if not items:
        return redirect("home")
    sub_total = 0

    for item in items:
        sub_total += item.total_price
    print("FUCK")
    # calculate freight cost
    freight_cost = SiteInfo.objects.first().freight_cost if sub_total < 1000000 else 0
    sub_total += freight_cost

    context = {'addresses': addresses, 'items': items, 'sub_total': sub_total, 'customer': customer,
               'freight_cost': freight_cost}
    return render(request, 'shop/purchase.html', context)



@utils.expire_session
def cancel_order_view(request, pk):
    order = get_object_or_404(Order, id=pk)
    if not order.is_payment_pending:
        return utils.get_toast_response(request, "شما نمیتوانید این سفارش را لغو کنید", "danger")
    order.set_canceled()
    order.save()
    return utils.get_toast_response(request, "سفارش لغو شد", "success")


@utils.expire_session
def coming_soon_view(request):
    return render(request, 'under_development.html')


@utils.expire_session
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

            # calculate freight cost
            freight_cost = SiteInfo.objects.first().freight_cost if sub_total < 10000000 else 0
            sub_total += freight_cost

            if request.POST.get("order_id", None):
                order = get_object_or_404(Order, id=request.POST['order_id'])
            else:
                order = Order.objects.create(customer=customer,
                                             session=session,
                                             freight_cost=freight_cost,
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
                                                 name=item.product.name, price=item.sell_price, weight=item.weight,
                                                 total_price=item.total_price)
            callback_url = \
                ('http://' if loister.settings.DEBUG else 'https://') + SiteInfo.objects.first().site_domain + reverse(
                    'payment_confirmation')
            zb = zibal(loister.settings.MERCHANT, callback_url)
            # send payment request
            response_dict = zb.request(amount=str(order.total_price * 10), mobile=order.delivery_phone_number,
                                       order_id=order.id)
            try:
                if response_dict['result'] == 100:
                    track_id = response_dict['trackId']
                    order.payment_track_id = track_id
                    order.save()
                    return redirect(f'https://gateway.zibal.ir/start/{track_id}')
                else:
                    return HttpResponse(
                        f"""<h1 dir="rtl">درخواست شما با خطا مواجه شد<h1>""" +
                        f"""<h1 dir="rtl">{zb.request_result(response_dict['result'])}<h1>""" +
                        f"""<h1 dir="rtl">در صورت داشتن حساب کاربری میتوانید خرید همین سفارش از صفحه کاربری خود ادامه دهید</h1>"""
                    )
            except:
                raise SuspiciousOperation(response_dict['result'])
    raise Http404


@utils.expire_session
def payment_confirmation_view(request):
    """method that handles bank's API callback"""
    context = {'order_id': request.GET['orderId'], 'track_id': request.GET['trackId']}
    if request.GET['success'] == "1":
        zb = zibal(loister.settings.MERCHANT, '')
        response = zb.verify(trackId=request.GET['trackId'])
        if response['result'] == 100:
            if response['status'] == 1:
                order = Order.objects.get(id=int(request.GET["orderId"]))

                if order.payment_track_id != request.GET['trackId']:
                    raise ValidationError("trackId is invalid")
                if order.total_price * 10 != response['amount']:
                    raise ValidationError("payment amount is invalid")

                order.set_payment_successful()
                order.checkout_date = datetime.fromisoformat(response['paidAt'])
                order.save()
                context['successful'] = True
                if request.user.is_authenticated:
                    CartProductQuantity.objects.filter(cart__customer__user=request.user).delete()
                else:
                    CartProductQuantity.objects.filter(cart__session=request.session.session_key,
                                                       cart__customer=None).delete()
            else:
                return HttpResponse(
                    """<h1 dir="rtl">پرداخت شما از سمت زیبال تایید نشده است لطفا با پشتیبانی تماس بگیرید.</h1>""" +
                    "<br>" + f"{zb.verify_result(response['result'])}")
        elif response['result'] == 201:
            context['already_successful'] = True
        else:
            return HttpResponse("""<h1 dir="rtl">پرداخت با خطا مواجه شده است</h1>""")
    else:
        context['successful'] = False
    return render(request, "payment_result.html", context=context)


@utils.expire_session
def profile_addresses_view(request):
    if request.user.is_authenticated:
        addresses = CustomerAddress.objects.filter(customer__user=request.user)
        context = {'addresses': addresses}
        return render(request, 'user_profile/addresses.html', context)
    return redirect("logup")


@utils.expire_session
def add_address_view(request):
    if request.POST:
        CustomerAddress.objects.create(customer=CustomerProfile.objects.get(user=request.user),
                                       delivery_phone_number=request.POST.get("mobile", 0),
                                       district=request.POST.get("state"),
                                       city=request.POST.get("city"),
                                       address=request.POST.get("address"),
                                       postal_code=request.POST.get("postal_code"))
        return utils.get_back_reload_response(request)
    return Http404


@utils.expire_session
def remove_address_view(request, pk):
    if request.user.is_authenticated:
        get_object_or_404(CustomerAddress, id=pk).delete()
        return utils.get_back_reload_response(request)
    return redirect("logup")


@utils.expire_session
def profile_info_view(request):
    if request.user.is_authenticated:
        customer = CustomerProfile.objects.get(user=request.user)
        context = {'user': request.user, 'customer': customer}
        return render(request, 'user_profile/profile_info.html', context)
    return redirect("logup")


@utils.expire_session
def profile_purchase_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer__user=request.user).order_by('-invoice_date_time')
        context = {'orders': orders}
        return render(request, 'user_profile/purchase-history.html', context)
    return redirect("logup")


@utils.expire_session
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
    if request.GET.get("ptype", None):
        regex = ""
        for ptype in request.GET.getlist("ptype"):
            regex += ptype + "|"
        products = products.filter(type__name__iregex=regex[:-1])
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


@utils.expire_session
def wishlist_view(request):
    if request.user.is_authenticated:
        favourites = CustomerProfile.objects.get(user=request.user).favourites
        products = favourites.all()
        if request.GET.get("remove_favourite", None):
            favourites.remove(request.GET.get("remove_favourite"))
        context = {'products': products}
        return render(request, "shop/wishlist.html", context)
    return HttpResponse("<script>history.back();</script>")


@utils.expire_session
def logup_view(request):
    if request.user.is_authenticated:
        return redirect("profile_info")
    if request.method == "POST":
        if request.POST.get("username", None) and request.POST.get("password", None):
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                return utils.get_toast_response(request, "با موفقیت وارد شدید", "success")
            else:
                raise ValidationError("wrong credentials")
        else:
            raise ValidationError("fill fields")
    context = {'login_page': True}
    return render(request, 'login.html', context)


@utils.expire_session
def new_review(request, slug):
    if request.POST and request.user.is_authenticated:
        if request.POST.get("rating", None) or request.POST.get("content", None):
            product = get_object_or_404(Product, slug=slug)
            if Review.objects.filter(parent__isnull=False, author__user=request.user,
                                     submit_time__gte=timezone.now() - timedelta(seconds=30)).exists():
                return utils.get_toast_response(request, "شما به تازگی نظر ثبت کرده اید لطفا چند ثانیه صبر کنید",
                                                "warning")
            elif Review.objects.filter(parent__isnull=True, author__user=request.user,
                                       product=product).exists() and not request.POST.get("parent", None):
                return utils.get_toast_response(request, "شما قبلا نظر ثبت کرده اید",
                                                "danger")
            try:
                Review.objects.create(product=product,
                                      author=get_object_or_404(CustomerProfile, user=request.user),
                                      parent_id=request.POST.get("parent", None),
                                      rating=request.POST.get("rating", None),
                                      content=request.POST.get('content', None))

                return utils.get_toast_response(request, "نظر شما ثبت شد و پس از تایید نمایش داده خواهد شد", "success")
            except MultiValueDictKeyError:
                pass
        else:
            return utils.get_toast_response(request, "حداقل یکی از فیلد های امتیاز یا نظر باید پر شود", "warning")

    return utils.get_toast_response(request, "برای نظر دادن وارد حساب کاربری شوید", "warning")


@utils.expire_session
def toggle_wishlist(request, is_favourite, pk):
    if request.user.is_authenticated:
        if eval(is_favourite):
            CustomerProfile.objects.get(user=request.user).favourites.remove(Product.objects.get(id=pk))
        else:
            CustomerProfile.objects.get(user=request.user).favourites.add(Product.objects.get(id=pk))

        return utils.get_back_reload_response(request)
    return utils.get_toast_response(request, "برای اضافه کردن به علاقه مندی وارد سایت شوید", 'danger')


def order_set_complete_view(request, pk):
    order = Order.objects.get(pk=pk)
    order.set_completed()
    order.save()
    # return redirect(reverse('admin:shop_order_changelist'))
    return HttpResponse("<script>history.back();</script>")


def order_details_view(request, pk):
    if request.user.is_authenticated:
        order: Order = get_object_or_404(Order, pk=pk)
        if order.customer.user == request.user:
            if order.is_payment_pending:
                items = BoughtProduct.objects.filter(order=order)
                addresses = CustomerAddress.objects.filter(customer__user=request.user)
                customer = CustomerProfile.objects.filter(user=request.user).first()
                sub_total = 0
                for item in items:
                    sub_total += item.total_price

                # calculate freight cost
                freight_cost = SiteInfo.objects.first().freight_cost if sub_total < 10000000 else 0
                sub_total += freight_cost

                context = {'order': order, 'addresses': addresses, 'items': items, 'sub_total': sub_total,
                           'freight_cost': freight_cost, 'customer': customer}
                return render(request, "shop/purchase.html", context=context)
            else:
                items = BoughtProduct.objects.filter(order=order)
                context = {'order': order, 'items': items}
                return render(request, "user_profile/order_details.html", context=context)
    raise SuspiciousOperation()

#
# def test_view(request, order_id=2):
#     amount = 1000000
#     mobile = '09915392053'
#     callback_url = \
#         ('http://' if loister.settings.DEBUG else 'https://') + SiteInfo.objects.first().site_domain + reverse(
#             'payment_confirmation')
#     zb = zibal(loister.settings.MERCHANT, callback_url)
#     order = get_object_or_404(Order, id=order_id)
#     response_dict = zb.request(amount=str(order.total_price * 10), mobile=order.delivery_phone_number,
#                                order_id=order.id)
#     try:
#         if response_dict['result'] == 100:
#             track_id = response_dict['trackId']
#             order.payment_track_id = track_id
#             order.save()
#             return redirect(f'https://gateway.zibal.ir/start/{track_id}')
#         else:
#             return HttpResponse(
#                 f"""<h1 dir="rtl">درخواست شما با خطا مواجه شد<h1>""" +
#                 f"""<h1 dir="rtl">{zb.request_result(response_dict['result'])}<h1>""" +
#                 f"""<h1 dir="rtl">لطفا برای حل مشکل با پشتیبانی تماس بگیرید</h1>"""
#             )
#
#     except:
#         raise SuspiciousOperation(response_dict['result'])
