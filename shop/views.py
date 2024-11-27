from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView

from shop.cart import Cart
from shop.forms import AddToCartForm
from shop.models import Item


CART_SESSION_KEY = 'cart'
# Create your views here.
class ItemListView(ListView):
    model = Item
    template_name = "shop/item_list.html"
    context_object_name = 'items'
    ordering = 'created_at'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantities_in_cart']= Cart.get_quantities_in_cart(self.request.session, CART_SESSION_KEY)
        print(context)
        return context


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
        
        context['form'] = AddToCartForm()
        # print(context)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # カートに商品を追加する処理
            
            return redirect('shop:add-to-cart')


class AddToCartView(RedirectView):
    url = reverse_lazy('shop:item-list')

    def get(self, request, *args, **kwargs):
        # shop.models.Itemからpkで商品を指定、インスタンス化
        item = get_object_or_404(Item, pk=kwargs['pk'])
        # item = Item.objects.get(pk=kwargs['pk'])
        
        # ここからカートに関する処理
        cart = Cart.create_from_session(request.session, CART_SESSION_KEY)
        cart.add_item(item)
        cart.save_to_session(request.session, CART_SESSION_KEY)
        
        return super().get(request, *args, **kwargs)