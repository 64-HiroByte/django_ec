from django import forms

from .models import CreditCard
from .models import Purchaser
from .models import ShippingAddress


class UserFrom(forms.ModelForm):
    """
    ユーザー情報登録フォーム
    """
    class Meta:
        model = Purchaser
        fields = ['user_name', 'family_name', 'given_name', 'email']


class AddressForm(forms.ModelForm):
    """
    住所入力フォーム
    """
    class Meta:
        model = ShippingAddress
        fields = ['zip_code', 'prefecture', 'address', 'building']


class CreditCardForm(forms.ModelForm):
    """
    クレジットカード情報入力フォーム
    """
    class Meta:
        model = CreditCard
        fields = ['cardholder', 'card_number', 'card_expiration', 'cvv']