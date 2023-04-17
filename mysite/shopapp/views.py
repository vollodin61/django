from timeit import default_timer

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

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
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(UserPassesTestMixin, CreateView, PermissionRequiredMixin):
    def form_valid(self, form):
        form.instance.created_by = self.request.user.id
        return super().form_valid(form)

    def test_func(self):
        # return self.request.user.groups.filter('secret-group').exists()
        return self.request.user.user_permissions

    permission_required = 'add_product'
    model = Product
    fields = 'name', 'price', 'discount', 'description', 'created_by'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UserPassesTestMixin, UpdateView, PermissionRequiredMixin):
    model = Product
    fields = 'name', 'price', 'discount', 'description'
    template_name_suffix = '_update_form'
    permission_required = 'product_update'

    def test_func(self):
        return self.request.user.user_permissions

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))


class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'view_order'
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))


class CreateOrderView(CreateView):
    template_name = 'shopapp/order_form.html'
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))
    fields = 'delivery_address', 'promocode', 'user', 'products'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    template_name = 'shopapp/order_update_form.html'
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))
    fields = 'delivery_address', 'promocode', 'user', 'products'
    # success_url = reverse_lazy('shopapp:order_details')

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )


class OrderDeleteView(DeleteView):
    template_name = 'shopapp/order_confirm_delete.html'
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))
    success_url = reverse_lazy('shopapp:orders_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            for product in products
        ]
        return JsonResponse({'products': products_data})



# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse('shopapp:orders_list')
#             return redirect(url)
#     else:
#         form = OrderForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'shopapp/create-order.html', context)
