from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import View

# from cart.cart import Cart
from cart.models import Cart
from cart.models import CartItem
from shop.models import Item


# CART_SESSION_KEY = 'cart'


class AddToCartView(View):
    def get_cart(self):
        cart = Cart.load_from_session(self.request.session)
        if cart is None:
            cart = Cart.create_cart(self.request.session)
        return cart
    
    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        # item_pk = request.POST.get('item_pk')  # 商品一覧ページの数量もフォームを使う
        item_pk = kwargs.get('item_pk')
        item = get_object_or_404(Item, pk=item_pk)
        
        quantity = int(request.POST.get('quantity'))
        CartItem.add_item(cart, item, quantity)
        
        return redirect('shop:item-list')  # リダイレクト先は後で決める


class CheckoutListView(TemplateView):
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
        
        # cart_pk = self.request.session.get(CART_SESSION_KEY)

        # if cart is None:
        #     context['cartitems'] = None
            
        # else:
        #     cart = Cart.objects.get(pk=cart_pk)
        #     context['cartitems'] = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart_pk)
        #     context['total_price'] = cart.get_total_price()
        #     context['quantities_in_cart'] = cart.quantities
        # print(context)
        
        return context
    
"""
    def post(self, request, *args, **kwargs):
        item_pk = request.POST.get('item_pk')
        if item_pk:
            item_pk = int(item_pk)
            # カートから選択した商品を削除する処理（カートの生成、商品の削除、セッションに保存）
            cart = Cart.create_from_session(request.session, CART_SESSION_KEY)
            cart.delete_item(item_pk)
            cart.save_to_session(request.session, CART_SESSION_KEY)
        
        return redirect('cart:checkout')
"""
