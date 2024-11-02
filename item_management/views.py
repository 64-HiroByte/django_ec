from django.shortcuts import render
from django.views.generic import ListView

from shop.models import Item
# Create your views here.
class ManagementListView(ListView):
    model = Item
    template_name = "item_management/management_list.html"
    context_object_name = 'items'
    ordering = 'created_at'