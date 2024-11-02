from django.urls import path

from item_management.views import ItemCreateView
from item_management.views import ManagementListView


urlpatterns = [
    path('', ManagementListView.as_view(), name='management-item-list'),
    path('register', ItemCreateView.as_view(), name='item-register'),
]