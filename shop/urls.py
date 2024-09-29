from django.urls import path

from shop.views import ItemListView


urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
]
