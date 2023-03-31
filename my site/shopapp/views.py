from email.policy import HTTP, default
from timeit import default_timer
from django.http import HttpResponse, HttpResponse
from django.shortcuts import render


def shop_index(request: HttpResponse):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        'time_running': default_timer(),
        'products': products
    }
    return (render(request, 'shopapp/shop-index.html', context=context))
