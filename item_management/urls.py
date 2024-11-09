from django.urls import path

from item_management.views import ItemCreateView
from item_management.views import ItemDeleteView
from item_management.views import ManagementListView
from item_management.views import ItemUpdateView


urlpatterns = [
    path('', ManagementListView.as_view(), name='management-item-list'),
    path('register/', ItemCreateView.as_view(), name='item-register'),
    path('<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('<int:pk>/edit/', ItemUpdateView.as_view(), name='item-edit'),
]