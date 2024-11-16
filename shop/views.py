from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView

from shop.cart import Cart
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
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 現在のアイテムを取得
        item = self.get_object()
        # 表示させる関連商品の数
        get_related_item_count = 4

        # 関連商品の取得（ただし、現在の商品は除く）
        context['related_items'] = Item.objects.exclude(id=item.id).order_by('-created_at')[:get_related_item_count] 
        return context


CART_SESSION_KEY = 'cart'

class AddToCartView(RedirectView):
    url = reverse_lazy('item_list')

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=kwargs['item_pk'])

        cart = Cart.create_from_session(request.session, CART_SESSION_KEY)
        cart.add_item(item)
        
        cart.save_to_session(request.session, CART_SESSION_KEY)
        return super().get(request, *args, **kwargs)