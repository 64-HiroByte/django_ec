from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View

from cart.models import Cart
from cart.models import CartItem
from purchase.models import Order
from purchase.models import OrderDetail
from purchase.models import Purchaser


class PurchaseView(View):
    """
    購入処理（注文履歴・注文明細の登録）を行うビュー
    """
    def get(self, request, *args, **kwargs):
        cart = Cart.load_from_session(request.session)
        
        # カートがない、または、数量が０の場合、トップページへリダイレクト
        if cart is None or cart.quantities == 0:
            return redirect('shop:item-list')
        
        purchaser_pk = request.session.get('purchaser')
        # セッションに購入者情報がない場合、トップページへリダイレクト
        if purchaser_pk is None:
            return redirect('shop:item-list')
        else:
            purchaser = Purchaser.objects.get(pk=purchaser_pk)
        
        try:
            with transaction.atomic():
                # OrderテーブルにCartテーブルの情報を保存
                order = Order.objects.create(
                    purchaser=purchaser,
                    total_price=cart.get_total_price(),
                )
                
                # OrderDetailテーブルにCartItemテーブルの情報を保存
                cart_items = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart.pk)
                
                for cart_item in cart_items:
                    OrderDetail.objects.create(
                        order=order,
                        item=cart_item.item,
                        quantity=cart_item.quantity,
                        sub_total=cart_item.sub_total,
                    )
                # カートの中身を削除
                cart.delete()
            
                # セッションから購入者情報を削除
                del request.session['cart']
                del request.session['purchaser']
                
                messages.success(request, '購入ありがとうございます')
                return redirect('shop:item-list')
            
        except Exception as err:
            messages.error(request, f'エラーが発生しました（{err}）')
            return redirect('shop:item-list')
        

class OrderListView(ListView):
    """
    注文履歴を表示するビュー
    """
    model = Order
    template_name = 'purchase/order_list.html'
    context_object_name = 'orders'
    ordering = '-created_at'
    
    def get_queryset(self):
        return Order.objects.select_related('purchaser')
    
    # 現状でcontext_dataをオーバーライドする必要はないが、今後の拡張を見据えて記述しておく
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 今後contextに追加するデータがあれば、ここに記述する
        
        return context


class OrderDetailView(DetailView):
    ""
    model = Order
    template_name = 'purchase/order_detail.html'
    context_object_name = 'orders'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 今後contextに追加するデータがあれば、ここに記述する
        # print(context['orders'])
        print(context)
        return context