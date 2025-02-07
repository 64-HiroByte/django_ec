from django.urls import path

from cart.views import ApplyPromotionToCartView
from cart.views import CancelPromotionFromCartView


app_name = 'promotion'
urlpatterns = [
    path('apply/', ApplyPromotionToCartView.as_view(), name='apply'),
    path('cancel/', CancelPromotionFromCartView.as_view(), name='cancel'),
]