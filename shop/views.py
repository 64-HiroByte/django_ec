from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

from shop.models import Item


# Create your views here.
class ItemListView(ListView):
    model = Item
    template_name = "shop/item_list.html"
    context_object_name = 'items'
    ordering = 'created_at'


class ItemDetailView(DetailView):
    model = Item
    template_name = "shop/item_detail.html"
