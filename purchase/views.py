from basicauth.decorators import basic_auth_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
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
        purchaser_pk = Purchaser.load_from_session(request.session)
        redirect_url = 'shop:item-list'
        
        redirect_if_invalid(cart=cart, purchaser_pk=purchaser_pk, redirect_url=redirect_url)
        
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
                delete_from_session(request.session, Cart, Purchaser)
                
                messages.success(request, '購入ありがとうございます')
                return redirect(redirect_url)
            
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
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.get_order_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.object
        purchaser = orders.purchaser
        shipping_address = orders.purchaser.shipping_address
        credit_card = orders.purchaser.credit_card
        
        template_dict = get_template_dict(
            purchaser, shipping_address, credit_card, 
            attr_name='informations', 
            template_key='html_template'
        )
        
        informations_list = [
            {'label': key, 'value': value} for key, value in template_dict.items()
        ]
        
        context['purchaser_infos'] = informations_list
        
        context['order_details'] = orders.order_detail.all()
        for ordered_item in context['order_details']:
            print(f'{ordered_item.item.name}: {ordered_item.item.price}円 x {ordered_item.quantity} = {ordered_item.sub_total}円')
        return context


class SendOrderMailView(View):
    """
    注文情報をメールで送信するビュー
    """
    SUBJECT = 'ご注文ありがとうございます'
    FROM_EMAIL_ADDRESS = 'hiorbyte@gmail.com'
    
    def get(self, request, *args, **kwargs):
        order = Order.load_from_session(request.session)
        if order is None:
            messages.error(request, '注文情報が見つかりません')
            return redirect('shop:item-list')
        
        subject = self.SUBJECT
        message = "本文"
        from_email = self.FROM_EMAIL_ADDRESS
        recipient_list = [
            "hiorbyte@gmail.com"
        ]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return redirect('cart:checkout')