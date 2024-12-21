from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import ListView

from cart.models import Cart
from shop.models import Item


class ItemListView(ListView):
    """
    商品の一覧を表示するビュー
    """
    model = Item
    template_name = "shop/item_list.html"
    context_object_name = 'items'
    ordering = 'created_at'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.load_from_session(self.request.session)
        if cart is None:
            context['quantities_in_cart'] = 0
        else:
            context['quantities_in_cart']= cart.quantities
        return context


class ItemDetailView(DetailView):
    """
    商品の詳細を表示するビュー
    """
    model = Item
    template_name = "shop/item_detail.html"
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 現在のアイテムを取得
        item_pk = kwargs.get('item_pk')
        # 表示させる関連商品の数
        get_related_item_count = 4
        # 関連商品の取得（ただし、現在の商品は除く）
        context['related_items'] = Item.objects.exclude(pk=item_pk).order_by('-created_at')[:get_related_item_count]

        # カート内の商品数の取得
        cart = Cart.load_from_session(self.request.session)
        if cart is None:
            context['quantities_in_cart'] = 0
        else:
            context['quantities_in_cart']= cart.quantities 
        return context
