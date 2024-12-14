from django.contrib import admin

from cart.models import Cart
from cart.models import CartItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)