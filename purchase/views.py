from django.db import transaction
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from .forms import CreditCardForm
from .forms import PurchaserForm
from .forms import ShippingAddressForm
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
        # 以下のelse文の内容は注文履歴の処理を行う際に有効化する
        # else:
        #     cart_items = CartItem.objects.select_related('item', 'cart').filter(cart_id=cart.pk)
        
        # form
        purchaser_form = PurchaserForm(request.POST)
        shipping_address_form = ShippingAddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)
        if (purchaser_form.is_valid() and 
            shipping_address_form.is_valid() and
            credit_card_form.is_valid()
            ):
            print('this is OK!')
            return redirect('cart:checkout')
        # try:
        #     with transaction.atomic():
        #         # Puchaserの保存
        #         purchaser = purchaser_form.save()
                
        #         # ShippingAdressの保存
        #         shipping_address = shipping_address_form.save(commit=False)
        #         shipping_address.purchaser = purchaser
        #         shipping_address.save()
                
        #         # CreditCardの保存
        #         credit_card = credit_card_form.save(commit=False)
        #         credit_card.purchaser = purchaser
        #         credit_card =credit_card_form.save()
        #     return 
        
        # except Exception as err:
        #     # Print文の内容をFlashメッセージで表示させる
        #     print(f'予期せぬエラーが発生しました: {err}')
        
        else:
            print('this is error!')
            address_errors = shipping_address_form.errors.items()
            print(address_errors)
            cc_errors = credit_card_form.errors.items()
            print(cc_errors)
            return redirect('cart:checkout')


