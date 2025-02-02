from django.urls import path

from cart.views import ApplyPromotionToCart


app_name = 'promotion'
urlpatterns = [
    path('apply/', ApplyPromotionToCart.as_view(), name='apply'),
]