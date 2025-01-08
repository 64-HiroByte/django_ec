from django.db import transaction
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from cart.models import Cart
from cart.models import CartItem


# Create your views here.
class PurchaseView(View):
    
    
    def post(self, request, *args, **kwargs):
        print('-' * 30 + ' post ' + '-'* 30)
        cart = Cart.load_from_session(request.session)
        
        # カートがない、または、数量が０の場合、トップページへリダイレクト
        if cart is None or cart.quantities == 0:
            print('カートが空です！')
            return redirect('shop:item-list')
        
        cart_items = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart.pk)
        print(cart_items)
