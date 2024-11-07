from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from shop.models import Item


class ManagementListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "item_management/management_list.html"
    context_object_name = 'items'
    ordering = 'created_at'



class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = "item_management/item_form.html"
    fields = '__all__'
    success_url = reverse_lazy('management-item-list')



class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "item_management/item_delete.html"
    success_url = reverse_lazy('management-item-list')


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = "item_management/item_form.html"
    fields = '__all__'
    success_url = reverse_lazy('management-item-list')
