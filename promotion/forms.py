from django import forms
from django.shortcuts import redirect

from promotion.models import PromotionCode


class PromotionCodeForm(forms.Form):
    """
    プロモーションコード入力フォーム
    """
    code = forms.CharField(
        label='プロモーションコード',
        max_length=PromotionCode.MAX_CODE_LENGTH,
        required=False,
        widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'code',
                'placeholder': 'コードを入力してください',
                # 'required': 'required'
        })
    )
    
    def clean_code(self):
        code = self.cleaned_data['code']
        
        if not code:
            raise forms.ValidationError('プロモーションコードを入力してください')
        
        # プロモーションコードは存在するか
        try:
            promotion = PromotionCode.objects.get(code=code)
        except PromotionCode.DoesNotExist:
            raise forms.ValidationError(f'"{code}"は無効なコードです')
        
        # 使用済みプロモーションコードであるか
        if not promotion.is_active:
            raise forms.ValidationError(f'"{code}"は既に使われています')
        
        # PromotionCodeのインスタンスをcleaned_dataに保存
        self.cleaned_data['promotion'] = promotion
        return code