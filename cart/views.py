from django.shortcuts import redirect
from django.views.generic import TemplateView

from cart.cart import Cart


CART_SESSION_KEY = 'cart'

class CheckoutListView(TemplateView):
    template_name = "cart/checkout.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # カート内の商品点数の取得
        context['quantities_in_cart']= Cart.get_quantities_in_cart(self.request.session, CART_SESSION_KEY)
        # セッションデータからカートを生成
        cart = Cart.create_from_session(self.request.session, CART_SESSION_KEY)
        # contextにカートに関する情報を追加
        context['items_in_cart'] = cart.items_in_cart
        context['total_price'] = cart.total_price
        return context
    
    def post(self, request, *args, **kwargs):
        item_pk = request.POST.get('item_pk')
        if item_pk:
            item_pk = int(item_pk)
            # カートから選択した商品を削除する処理（カートの生成、商品の削除、セッションに保存）
            cart = Cart.create_from_session(request.session, CART_SESSION_KEY)
            cart.delete_item(item_pk)
            cart.save_to_session(request.session, CART_SESSION_KEY)
        
        return redirect('cart:checkout')

