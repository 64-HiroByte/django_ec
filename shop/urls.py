from django.urls import path

from shop.views import ItemDetailView
from shop.views import ItemListView


urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]
