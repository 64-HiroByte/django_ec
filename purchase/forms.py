import re

from django import forms

from .models import CreditCard
from .models import Prefecture
from .models import Purchaser
from .models import ShippingAddress


class PurchaserForm(forms.ModelForm):
    """
    ユーザー情報登録フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} is-invalid'

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
        error_messages = {
            'user_name': {
                'required': 'ユーザーネームを入力してください',
            },
            'family_name': {
                'required': '姓を入力してください',
            },
            'given_name': {
                'required': '名を入力してください',
            },
            'email': {
                'required': 'メールアドレスを入力してください',
            },
        }


class ShippingAddressForm(forms.ModelForm):
    """
    住所入力フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} is-invalid'
    
    class Meta:
        model = ShippingAddress
        fields = ['zip_code', 'prefecture', 'address', 'building']
        widgets = {
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'zip-code',
                'placeholder': '数字7桁',
                'required': True,
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address',
                'placeholder': '千代田区千代田１−１',
                'required': True,
            }),
            'building': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'building',
                'placeholder': 'ビル名、マンション名など',
                'required': False,
            }),
        }
        error_messages = {
            'zip_code': {
                'required': '郵便番号を入力してください',
            },
            'address': {
                'required': '住所を入力してください',
            },
        }
    
    prefecture = forms.ModelChoiceField(
        queryset=Prefecture.objects.all(),
        empty_label='選択してください',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'prefecture',
            'required': True,
        }),
        error_messages={
            'required': '都道府県を選択してください'
        }
    )


class CreditCardForm(forms.ModelForm):
    """
    クレジットカード情報入力フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} is-invalid'
    
    class Meta:
        model = CreditCard
        fields = ['cardholder', 'card_number', 'card_expiration', 'cvv']
        widgets = {
            'cardholder': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'cardholder',
                'placeholder': 'TARO YAMADA',
                'required': True,
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'card-number',
                'placeholder': '数字16桁',
                'required': True,
            }),
            'card_expiration': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'card-expiration',
                'placeholder': '月/年',
                'required': True,
            }),
            'cvv': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'cvv',
                'placeholder': '数字3桁',
                'required': True,
            }),
        }
        error_messages = {
            'cardholder': {
                'required': 'カード名義人を入力してください',
            },
            'card_number': {
                'required': 'カード番号を入力してください',
            },
            'card_expiration': {
                'required': '有効期限を入力してください',
            },
            'cvv': {
                'required': 'セキュリティコードを入力してください',
            },
        }
    
    def clean_card_expiration(self):
        expiration = self.cleaned_data['card_expiration']
        
        # MM/YY形式のチェック
        if not re.match(r'^\d{2}/\d{2}$', expiration):
            raise forms.ValidationError('MM/YYの形式で入力してください（例: 01/26）')

        # MM（月）の範囲のチェック
        if not re.match(r'^(0[1-9]|1[0-2])/\d{2}$', expiration):
            raise forms.ValidationError('"MM"の部分は01から12の範囲で入力してください')
        return expiration
    