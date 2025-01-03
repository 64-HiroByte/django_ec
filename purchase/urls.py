from django.urls import path

from purchase.views import PurchaseView


app_name = 'purchase'
urlpatterns = [
    path('', PurchaseView.as_view(), name='processing'),
]