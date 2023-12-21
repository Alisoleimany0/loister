from django.shortcuts import render

# Create your views here.


def cart(request):
    return render(request, 'cart.html'  , {})

def cart_add(request):
    pass

def cart_delete(request):
    pass

def cart_update(request):
    pass