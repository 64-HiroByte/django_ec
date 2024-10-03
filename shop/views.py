from django.shortcuts import render
from django.views.generic import ListView

from shop.models import Item


# Create your views here.
class ItemListView(ListView):
    model = Item
    template_name = "shop/index.html"
