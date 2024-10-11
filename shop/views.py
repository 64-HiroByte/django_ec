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
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 現在のアイテムを取得
        item = self.get_object()
        # 表示させる関連商品の数
        get_related_item_count = 1

        # 関連商品の取得（ただし、現在の商品は除く）
        context['related_items'] = Item.objects.exclude(id=item.id).order_by('-created_at')[:get_related_item_count]  # 登録日が最新のもの1点
        return contex）