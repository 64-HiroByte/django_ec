from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView

from shop.forms import AddToCartForm
from shop.models import Item


CART_SESSION_KEY = 'cart'

class ItemListView(ListView):
    model = Item
    template_name = "shop/item_list.html"
    context_object_name = 'items'
    ordering = 'created_at'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['quantities_in_cart']= Cart.get_quantities_in_cart(self.request.session, CART_SESSION_KEY)
    #     return context


class ItemDetailView(DetailView):
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

        # # カート内の商品数の取得
        # context['quantities_in_cart']= Cart.get_quantities_in_cart(self.request.session, CART_SESSION_KEY)
        # context['form'] = AddToCartForm()
        
        return context
    
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = AddToCartForm(request.POST)
    #     # 入力された数量のバリデーション
    #     if form.is_valid():
    #         quantity = form.cleaned_data['quantity']
            
    #         # カートに関する処理（カートの生成、商品追加、セッションに保存）
    #         cart = Cart.create_from_session(request.session, CART_SESSION_KEY)
    #         cart.add_item(item=self.object, quantity=quantity)
    #         cart.save_to_session(request.session, CART_SESSION_KEY)
            
    #         # 1. 商品詳細ページにリダイレクトする場合
    #         return redirect('shop:item-detail', pk=self.object.pk)
    #         # 2. 商品一覧ページにリダイレクトする場合
    #         # return redirect('shop:item-list')
    #     else:
    #         context = self.get_context_data(**kwargs)
    #         return self.render_to_response(context)


# class AddToCartView(RedirectView):
#     url = reverse_lazy('shop:item-list')

#     def get(self, request, *args, **kwargs):
#         # shop.models.Itemからpkで商品を指定、インスタンス化
#         item = get_object_or_404(Item, pk=kwargs['pk'])
        
#         # カートに関する処理（カートの生成、商品追加、セッションに保存）
#         cart = Cart.create_from_session(request.session, CART_SESSION_KEY)
#         cart.add_item(item)
#         cart.save_to_session(request.session, CART_SESSION_KEY)
        
#         return super().get(request, *args, **kwargs)