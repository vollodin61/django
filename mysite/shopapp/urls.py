from django.urls import path
from .views import (
    ShopIngexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    OrdersListView,
    OrdersDetailView,
    CreateProductView,
    create_order,
)

app_name = 'shopapp'

urlpatterns = [
    path('', ShopIngexView.as_view(), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/create/', CreateProductView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>', OrdersDetailView.as_view(), name='order_details'),
    path('orders/create/', create_order, name='order_create'),
]
