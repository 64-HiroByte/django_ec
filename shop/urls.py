from django.urls import path

from shop.views import AddToCartView
from shop.views import ItemDetailView
from shop.views import ItemListView

app_name = 'shop'
urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('add_to_cart/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
]
