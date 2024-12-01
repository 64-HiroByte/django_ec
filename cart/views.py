from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import TemplateView

from cart.cart import Cart
from shop.models import Item


CART_SESSION_KEY = 'cart'
# Create your views here.
class CheckoutListView(TemplateView):
    # model = Item
    template_name = "cart/checkout.html"
    # context_object_name = 'items'
    # ordering = 'created_at'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['quantities_in_cart']= Cart.get_quantities_in_cart(self.request.session, CART_SESSION_KEY)
        cart = Cart.create_from_session(self.request.session, CART_SESSION_KEY)
        context['items_in_cart'] = cart.items_in_cart
        context['total_price'] = cart.total_price
        return context

