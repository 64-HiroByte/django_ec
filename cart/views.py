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
from promotion.forms import PromotionCodeForm
from promotion.models import PromotionCode
from purchase.forms import CreditCardForm
from purchase.forms import PurchaserForm
from purchase.forms import ShippingAddressForm
from purchase.models import Purchaser
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

class ApplyPromotionToCart(View):
    def post(self, request, *args, **kwargs):
        form = PromotionCodeForm(request.POST)
        
        if form.is_valid():
            print(form)
            # PromotionCode.save_to_session(request.session, promotion_id=promotion.pk)
            messages.success(request, 'プロモーションコードを適用しました')
        else:
            print(f'エラーの内容: {form.errors["code"][0]}')
            messages.error(request, '無効なプロモーションコードが入力されました')
        return redirect('cart:checkout')

class CheckoutView(FormView):
    """
    カートの中身を表示させるためのビュー
    
    Attributes:
        form_class(Form): メインのフォームクラス
        shipping_address_form_class(Form): 配送先住所のフォームクラス
        credit_card_form_class(Form): クレジットカードのフォーム
        primary_form_key(str): メインのフォームのキー
        form_classes(dict): フォームの辞書

    Helper Methods:
        get_related_data_forms: 関連データのフォームを取得する
        forms_valid_failure: バリデーションエラーまたはトランザクションエラー時の処理
        forms_valid_successful: すべてのフォームのバリデーションが通った場合の処理
    """
    template_name = "cart/checkout.html"

    form_class = PurchaserForm
    shipping_address_form_class = ShippingAddressForm
    credit_card_form_class = CreditCardForm
    promotion_cord_form_class = PromotionCodeForm
    
    primary_form_key = 'purchaser_form'
    
    form_classes = {
        primary_form_key: form_class,
        'shipping_address_form': shipping_address_form_class,
        'credit_card_form': credit_card_form_class,
        'promotion_cord_form': promotion_cord_form_class,
    }
    
    def get_related_data_forms(self, forms):
        """
        関連データのフォームを取得する
        
        Args:
            forms(dict): フォームの辞書
        
        Returns:
            list: 関連データのフォームのリスト
        """
        related_data_forms = []
        for form_name, form_class in forms.items():
            if form_name != self.primary_form_key:
                related_data_forms.append(form_class)
            
        return related_data_forms
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.load_from_session(self.request.session)
        
        if cart is None:
            context['quantities_in_cart'] = 0
        else:
            context['cartitems'] = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart.pk)
            context['total_price'] = cart.get_total_price()
            context['quantities_in_cart'] = cart.quantities
        
        for form_name, form_class in self.form_classes.items():
            context[form_name] = kwargs.get(form_name, form_class())
        
        return context
    
    def forms_valid_failure(self, forms, messages_level=messages.info, message=''):
        """
        postメソッド実行時に使用
        バリデーションエラーまたはトランザクションエラー時の処理
        """
        context = self.get_context_data(**forms)
        messages_level(self.request, message)
        
        return self.render_to_response(context=context)
    
    def forms_valid_successful(self, request, forms):
        """
        postメソッド実行時に使用
        すべてのフォームのバリデーションが通った場合の処理
        """
        # DB保存処理を記述する
        try:
            with transaction.atomic():
                # Puchaserの保存
                purchaser = forms[self.primary_form_key].save()

                # Purchase関連データの保存
                related_data_forms = self.get_related_data_forms(forms)
                save_purchase_related_data(
                    purchaser=purchaser, 
                    related_data_forms=related_data_forms
                )
                # 購入者情報をセッションに保存
                Purchaser.save_to_session(request.session, purchaser.pk)

            return redirect('purchase:processing')
        except Exception as err:
            # エラーが発生した場合、エラーメッセージを表示し、チェックアウトページにリダイレクト
            messages_level = messages.error
            message = f'購入処理中にエラーが発生しました（{err}）'
            return self.forms_valid_failure(forms, messages_level=messages_level, message=message)
    
    def post(self, request, *args, **kwargs):
        # フォームのインスタンスを生成し、辞書に格納
        forms = {}
        for form_name, form_cls in self.form_classes.items():
            forms[form_name] = form_cls(request.POST)

        # バリデーションを実行
        if all(form.is_valid() for form in forms.values()):
            return self.forms_valid_successful(request, forms)
        else:
            message = '入力内容に誤りがあります'
            return self.forms_valid_failure(forms, message=message)
