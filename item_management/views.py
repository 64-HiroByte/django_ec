from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from shop.models import Item


class ManagementListView(ListView):
    model = Item
    template_name = "item_management/management_list.html"
    context_object_name = 'items'
    ordering = 'created_at'



class ItemCreateView(CreateView):
    model = Item
    template_name = "item_management/item_form.html"
    fields = '__all__'
    success_url = reverse_lazy('management-item-list')



class ItemDeleteView(DeleteView):
    model = Item
    template_name = "item_management/item_delete.html"
    success_url = reverse_lazy('management-item-list')
