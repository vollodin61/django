from django.contrib.auth.models import Group
from django.forms import ModelForm, ImageField, ClearableFileInput

from .models import Product, Order


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'discount', 'description', 'preview'

    images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
    )




class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'user', 'products'
