from django.db import transaction
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
        cart = Cart.load_from_session(request.session)
        if cart is None or cart.quantities == 0:
            # カートがないまたは、数量が０の場合のredirect先を考える
            return 
        
        purchaser_form = PurchaserForm(request.POST)
        shipping_address_form = ShippingAddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)

        if not (purchaser_form.is_valid() and 
            shipping_address_form.is_valid() and
            credit_card_form.is_valid()
            ):
            # redirect先を考える
            return
        
        try:
            with transaction.atomic():
                # Puchaserの保存
                purchaser = purchaser_form.save()
                
                # ShippingAdressの保存
                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.purchaser = purchaser
                shipping_address.save()
                
                # CreditCardの保存
                credit_card = credit_card_form.save(commit=False)
                credit_card.purchaser = purchaser
                credit_card =credit_card_form.save()
            return 
        
        except Exception as err:
            # Print文の内容をFlashメッセージで表示させる
            print(f'予期せぬエラーが発生しました: {err}')


