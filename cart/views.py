from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View

from cart.models import Cart
from cart.models import CartItem
from shop.models import Item
from purchase.forms import CreditCardForm
from purchase.forms import PurchaserForm
from purchase.forms import ShippingAddressForm


class AddToCartView(View):
    """
    カートに商品を追加するためのビュー
    """
    def get_cart(self):
        cart = Cart.load_from_session(self.request.session)
        if cart is None:
            cart = Cart.create_cart(self.request.session)
        return cart
    
    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        item_pk = kwargs.get('item_pk')
        item = get_object_or_404(Item, pk=item_pk)
        
        quantity = int(request.POST.get('quantity'))
        CartItem.add_item(cart, item, quantity)
        
        return redirect('shop:item-list')

class DeleteFromCartView(View):
    """
    カートから指定した商品を削除するビュー
    """
    def post(self, request, *args, **kwargs):
        cart = Cart.load_from_session(request.session)
        item_pk = kwargs.get('item_pk')
        
        CartItem.delete_item(cart=cart.pk, item=item_pk)
        
        return redirect('cart:checkout')

class CheckoutListView(TemplateView):
    """
    カートの中身を表示させるためのビュー
    """
    template_name = "cart/checkout.html"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cart = Cart.load_from_session(self.request.session)
        
        if cart is None:
            context['quantities_in_cart'] = 0
        else:
            context['cartitems'] = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart.pk)
            context['total_price'] = cart.get_total_price()
            context['quantities_in_cart'] = cart.quantities
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['purchaser_form'] = PurchaserForm()
        context['shipping_address_form'] = ShippingAddressForm()
        context['credit_card_form'] = CreditCardForm()
        return render(request, self.template_name, context)