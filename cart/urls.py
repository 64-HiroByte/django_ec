from django.urls import path

from cart.views import CheckoutListView

app_name = 'cart'
urlpatterns = [
    path('', CheckoutListView.as_view(), name='checkout'),
]