from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='数量',
    )