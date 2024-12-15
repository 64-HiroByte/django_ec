from django.urls import path

from cart.views import AddToCartView
# from cart.views import CartCreateview
from cart.views import CheckoutListView

app_name = 'cart'
urlpatterns = [
    path('', CheckoutListView.as_view(), name='checkout'),
    # path('<int:cart_pk>/create/', CartCreateview().as_view(), name='cart-create'),
    path('add_item/<int:item_pk>/', AddToCartView.as_view(), name='add-item'),
    # path('<int:pk>/delete_item/<int:item_pk>/', DeleteFromCartView.as_view(), name='checkout'),
]