from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from cart.cart import Cart
from shop.models import Item


CART_SESSION_KEY = 'cart'
# Create your views here.
class CheckoutListView(ListView):
    model = Item
    template_name = "shop/item_list.html"
    context_object_name = 'items'
    ordering = 'created_at'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['quantities_in_cart']= Cart.get_quantities_in_cart(self.request.session, CART_SESSION_KEY)
        return context

