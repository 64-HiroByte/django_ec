from django.urls import path

from purchase.views import PurchaseView
from purchase.views import OrderDetailView
from purchase.views import OrderListView


app_name = 'purchase'
urlpatterns = [
    path('', PurchaseView.as_view(), name='processing'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
]