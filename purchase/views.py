from basicauth.decorators import basic_auth_required
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View

from cart.models import Cart
from cart.models import CartItem
from purchase.models import Order
from purchase.models import OrderDetail
from purchase.models import Purchaser
from purchase.utils import delete_from_session
from purchase.utils import get_template_dict
from purchase.utils import redirect_if_invalid


class PurchaseView(View):
    """
    購入処理（注文履歴・注文明細の登録）を行うビュー
    """
    def get(self, request, *args, **kwargs):
        cart = Cart.load_from_session(request.session)
        purchaser = Purchaser.load_from_session(request.session)
        
        redirect_if_invalid(cart=cart, purchaser=purchaser, redirect_url='shop:item-list')
        
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

                # セッションからカートと購入者情報を削除
                delete_from_session(request.session, Cart, Purchaser)
                # セッションに注文情報を保存
                Order.save_to_session(request.session, order.pk)
                
                return redirect('purchase:mail')
            
        except Exception as err:
            messages.error(request, f'エラーが発生しました（{err}）')
            return redirect('shop:item-list')
        

@method_decorator(basic_auth_required, name='dispatch')
class OrderListView(ListView):
    """
    購入履歴を表示するビュー
    """
    model = Order
    template_name = 'purchase/order_list.html'
    context_object_name = 'orders'
    ordering = '-created_at'
    
    def get_queryset(self):
        return Order.objects.select_related('purchaser')


@method_decorator(basic_auth_required, name='dispatch')
class OrderDetailView(DetailView):
    """
    購入明細を表示するビュー
    """
    model = Order
    template_name = 'purchase/order_detail.html'
    # context_object_name = 'orders'  # orderとordersの混在は紛らわしいので設定しない
    
    def get_queryset(self):
        return Order.get_order_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object  # orders --> orderでもいいのではないか？
        purchaser = order.purchaser
        shipping_address = order.purchaser.shipping_address
        credit_card = order.purchaser.credit_card
        
        template_dict = get_template_dict(
            purchaser, shipping_address, credit_card, 
            attr_name='informations', 
            template_key='html_template'
        )
        
        informations_list = [
            {'label': key, 'value': value} for key, value in template_dict.items()
        ]
        context['order'] = order
        context['purchaser_infos'] = informations_list
        context['order_details'] = order.order_detail.all()
        return context


class SendOrderMailView(View):
    """
    注文情報をメールで送信するビュー
    """
    SUBJECT = 'ご注文ありがとうございます'
    FROM_EMAIL_ADDRESS = 'hiorbyte@gmail.com'
    template_name = 'purchase/order_confirmation_mail.txt'
    
    def get(self, request, *args, **kwargs):
        order_id = Order.load_from_session(request.session)
        if order_id is None:
            messages.error(request, '注文情報が見つかりません')
            return redirect('shop:item-list')
        
        # クエリセット取得
        order_queryset = Order.get_order_queryset()
        order = get_object_or_404(order_queryset, id=order_id)
        
        # template_dict作成
        purchaser = order.purchaser
        shipping_address = order.purchaser.shipping_address
        credit_card = order.purchaser.credit_card
        
        template_dict = get_template_dict(
            purchaser, shipping_address, credit_card, 
            attr_name='informations', 
            template_key='mail_template'
        )
        template_dict['order'] = order
        template_dict['order_details'] = order.order_detail.all()
        
        # メールテンプレート呼び出し
        message_body = render_to_string(self.template_name, template_dict)
        # メールテンプレートに辞書を渡してメッセージ本文作成
        
        
        subject = self.SUBJECT
        message = message_body
        from_email = self.FROM_EMAIL_ADDRESS
        recipient_list = [
            purchaser.email, "hiorbyte@gmail.com"
        ]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, '購入ありがとうございます')
        return redirect('shop:item-list')