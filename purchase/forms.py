from django import forms

from .models import CreditCard
from .models import Prefecture
from .models import Purchaser
from .models import ShippingAddress


class PurchaserForm(forms.ModelForm):
    """
    ユーザー情報登録フォーム
    """
    class Meta:
        model = Purchaser
        fields = ['user_name', 'family_name', 'given_name', 'email']


class ShippingAddressForm(forms.ModelForm):
    """
    住所入力フォーム
    """
    class Meta:
        model = ShippingAddress
        fields = ['zip_code', 'prefecture', 'address', 'building']
    
    prefecture = forms.ModelChoiceField(queryset=Prefecture.objects.all())


class CreditCardForm(forms.ModelForm):
    """
    クレジットカード情報入力フォーム
    """
    class Meta:
        model = CreditCard
        fields = ['cardholder', 'card_number', 'card_expiration', 'cvv']