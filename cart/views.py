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
        
        return redirect('shop:item-list')

class DeleteFromCartView(View):
    """
    カートから指定した商品を削除するビュー
    """
    def post(self, request, *args, **kwargs):
        cart = Cart.load_from_session(request.session)
        item_pk = kwargs.get('item_pk')
        
        CartItem.delete_item(cart=cart.pk, item=item_pk)
        
        return redirect('cart:checkout')

class CheckoutView(FormView):
    """
    カートの中身を表示させるためのビュー
    """
    template_name = "cart/checkout.html"

    form_class = PurchaserForm
    shipping_address_form_class = ShippingAddressForm
    credit_card_form_class = CreditCardForm
    
    
    # def initialize_form(self, context, form_key, form_class, form_instance=None):
    #     if form_key not in context:
    #     #     context[form_key] = kwargs.get(form_key)
    #     # if not context[form_key]:
    #     #     context[form_key] = form_class()
    #         if form_instance is not None:
    #             context[form_key] = form_instance
    #         else:
    #             context[form_key] = form_class
    
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
    
    def forms_valid(self, purchaser_form, shipping_address_form, credit_card_form):
        """
        すべてのフォームのバリデーションが通った場合の処理
        """
        print('this is OK!')
        # DB保存処理を記述する
        
        return redirect('shop:item-list')
    
    def forms_invalid(self, purchaser_form, shipping_address_form, credit_card_form):
        """
        バリデーションにエラーがあった場合の処理
        """
        context = self.get_context_data(
            purchaser_form=purchaser_form,
            shipping_address_form=shipping_address_form,
            credit_card_form=credit_card_form
        )
        print('#'*20 + ' validate error! ' + '#'*20)
        purchaser_errors = purchaser_form.errors.items()
        print(purchaser_errors)
        address_errors = shipping_address_form.errors.items()
        print(address_errors)
        cc_errors = credit_card_form.errors.items()
        print(cc_errors)
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        purchaser_form = PurchaserForm(request.POST)
        shipping_address_form = ShippingAddressForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)
        # purchaser_form = self.form_class(request.POST)
        # shipping_address_form = self.shipping_address_form_class(request.POST)
        # credit_card_form = self.credit_card_form_class(request.POST)
        
        if (
            purchaser_form.is_valid() and
            shipping_address_form.is_valid() and
            credit_card_form.is_valid()
        ):
            return self.forms_valid(purchaser_form, shipping_address_form, credit_card_form)
        else:
            return self.forms_invalid(purchaser_form, shipping_address_form, credit_card_form)
            

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     context['purchaser_form'] = PurchaserForm()
    #     context['shipping_address_form'] = ShippingAddressForm()
    #     context['credit_card_form'] = CreditCardForm()
    #     # return render(request, self.template_name, context)
    #     return self.render_to_response(context)