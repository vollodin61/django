from timeit import default_timer

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order


class ShopIngexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = 'products'


class CreateProductView(CreateView):
    model = Product
    fields = 'name', 'price', 'discount', 'description'
    success_url = reverse_lazy('shopapp:products_list')

# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse('shopapp:products_list')
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'shopapp/create-product.html', context=context)


class OrdersListView(ListView):
    queryset = (Order.objects.
                select_related('user')
                .prefetch_related('products'))


class OrdersDetailView(DetailView):
    queryset = (Order.objects.
                select_related('user')
                .prefetch_related('products'))


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        'form': form
    }
    return render(request, 'shopapp/create-order.html', context)
