from django.urls import path

from cart.views import AddToCartView
from cart.views import CheckoutView
from cart.views import DeleteFromCartView


app_name = 'cart'
urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('add_item/<int:item_pk>/', AddToCartView.as_view(), name='add-item'),
    path('delete_item/<int:item_pk>/', DeleteFromCartView.as_view(), name='delete-item'),
]