from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import View

# from cart.cart import Cart
from cart.models import Cart
from cart.models import CartItem
from shop.models import Item


CART_SESSION_KEY = 'cart'


# class CartCreateview(CreateView):
#     model = Cart
#     fields = []
#     template_name = ''  # のちほど決める

#     def form_valid(self, form):
#         cart = form.save()
#         self.request.session[CART_SESSION_KEY] = cart.pk
#         return redirect('')  # 商品をカートに追加するページへリダイレクト


class AddToCartView(View):
    def get_cart(self):
        cart_pk = self.request.session.get(CART_SESSION_KEY)

        if cart_pk is None:
            cart = Cart.objects.create()
            self.request.session[CART_SESSION_KEY] = cart.pk
            return cart
        else:
            return Cart.objects.get(pk=cart_pk)
    
    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        item_pk = request.POST.get('item_pk')  # 商品一覧ページの数量もフォームを使う
        item = get_object_or_404(Item, pk=item_pk)
        
        quantity = int(request.POST.get('quantity'))
        CartItem.add_item(cart, item, quantity)
        
        return redirect('')  # リダイレクト先は後で決める


"""
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
"""
