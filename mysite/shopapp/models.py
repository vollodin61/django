from django.db import models
from django.contrib.auth.models import User
from myauth.models import Profile


class Product(models.Model):
    class Meta:
        ordering = ['name', 'price']

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(Profile, null=True, on_delete=models.PROTECT, to_field='user_id')
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Product(pk={self.pk}, name={self.name!r})'


class Order(models.Model):
    class Meta:
        ordering = ['user', 'delivery_address']

    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f'Order(products={self.pk}, delivery_address={self.delivery_address!r})'
