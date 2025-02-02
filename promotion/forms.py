from django import forms

from promotion.models import PromotionCode


class PromotionCodeForm(forms.ModelForm):
    """
    プロモーションコード入力フォーム
    """
    
    class Meta:
        model = PromotionCode
        fields = ['code']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'code',
                'placeholder': 'コードを入力してください',
                'required': False
            })
        }
    
    