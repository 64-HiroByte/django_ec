from basicauth.decorators import basic_auth_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from shop.models import Item


@method_decorator(basic_auth_required, name='dispatch')
class ManagementListView(ListView):
    """
    商品管理をするためのビュー
    """
    model = Item
    template_name = "item_management/management_list.html"
    context_object_name = 'items'
    ordering = 'created_at'


@method_decorator(basic_auth_required, name='dispatch')
class ItemCreateView(CreateView):
    """
    商品を新規登録するためのビュー
    """
    model = Item
    template_name = "item_management/item_form.html"
    fields = '__all__'
    success_url = reverse_lazy('item_management:management-item-list')


@method_decorator(basic_auth_required, name='dispatch')
class ItemDeleteView(DeleteView):
    """
    商品を削除するためのビュー
    """
    model = Item
    template_name = "item_management/item_delete.html"
    success_url = reverse_lazy('item_management:management-item-list')


@method_decorator(basic_auth_required, name='dispatch')
class ItemUpdateView(UpdateView):
    """
    商品の情報を更新するためのビュー
    """
    model = Item
    template_name = "item_management/item_form.html"
    fields = '__all__'
    success_url = reverse_lazy('item_management:management-item-list')
