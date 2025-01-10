from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from cart.models import Cart
from cart.models import CartItem
from shop.models import Item
from purchase.forms import CreditCardForm
from purchase.forms import PurchaserForm
from purchase.forms import ShippingAddressForm
from purchase.utils import save_purchase_related_data


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
        messages.success(request, f'{item.name} x {quantity}点 をカートに追加しました')
        return redirect('shop:item-list')

class DeleteFromCartView(View):
    """
    カートから指定した商品を削除するビュー
    """
    def post(self, request, *args, **kwargs):
        cart = Cart.load_from_session(request.session)
        item_pk = kwargs.get('item_pk')
        
        CartItem.delete_item(cart=cart.pk, item=item_pk)
        messages.success(request, 'カートから商品を削除しました')
        return redirect('cart:checkout')

class CheckoutView(FormView):
    """
    カートの中身を表示させるためのビュー
    """
    template_name = "cart/checkout.html"

    form_class = PurchaserForm
    shipping_address_form_class = ShippingAddressForm
    credit_card_form_class = CreditCardForm
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.load_from_session(self.request.session)
        
        if cart is None:
            context['quantities_in_cart'] = 0
        else:
            context['cartitems'] = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart.pk)
            context['total_price'] = cart.get_total_price()
            context['quantities_in_cart'] = cart.quantities
        
        context['purchaser_form'] = kwargs.get('purchaser_form' , self.form_class())
        context['shipping_address_form'] = kwargs.get('shipping_address_form', self.shipping_address_form_class())
        context['credit_card_form'] = kwargs.get('credit_card_form', self.credit_card_form_class())
        
        return context
    
    def forms_valid(self, request, purchaser_form, related_data_forms):
        """
        すべてのフォームのバリデーションが通った場合の処理
        """
        # DB保存処理を記述する
        try:
            with transaction.atomic():
                # Puchaserの保存
                purchaser = purchaser_form.save()
                # Purchase関連データの保存
                save_purchase_related_data(
                    purchaser=purchaser, 
                    related_data_forms=related_data_forms
                )
                request.session['purchaser'] = purchaser.pk

                return redirect('purchase:processing')
        except Exception as err:
            # エラーが発生した場合、エラーメッセージを表示し、チェックアウトページにリダイレクト
            messages.error(request, f'購入処理中にエラーが発生しました（{err}）')
            return redirect('cart:checkout')
    
    def forms_invalid(self, purchaser_form, shipping_address_form, credit_card_form):
        """
        バリデーションにエラーがあった場合の処理
        """
        context = self.get_context_data(
            purchaser_form=purchaser_form,
            shipping_address_form=shipping_address_form,
            credit_card_form=credit_card_form
        )
        messages.info(self.request, '入力内容に誤りがあります')
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        purchaser_form = PurchaserForm(request.POST)
        shipping_address_form = ShippingAddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)
        
        related_data_forms = (shipping_address_form, credit_card_form)
        
        if (
            purchaser_form.is_valid() and
            shipping_address_form.is_valid() and
            credit_card_form.is_valid()
        ):
            return self.forms_valid(request, purchaser_form, related_data_forms)
        
        else:
            return self.forms_invalid(purchaser_form, shipping_address_form, credit_card_form)
            
