import calendar
import datetime

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
        widgets ={
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'user-name',
                'placeholder': 'username',
                'required': True,
            }),
            'family_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'family-name',
                'placeholder': '山田',
                'required': True,
            }),
            'given_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'given-name',
                'placeholder': '太郎',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'your-email-address@example.com',
                'required': True,
            }),
        }


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
    
    def clean_card_expiration(self):
        expiration = self.cleand_data['card_expiration']
        expiration_m, expiration_y = expiration.split('/')
        
        expiration_y = 2000 + int(expiration_y)
        expiration_m = int(expiration_m)
        expiration_d = calendar.monthrange(2000 + int(expiration_y), int(expiration_m))[1]
        expiration_date = datetime.date(expiration_y, expiration_m, expiration_d)
        if expiration_date < datetime.date.today():
            raise forms.ValidationError('有効期限が切れています')
        return expiration
    