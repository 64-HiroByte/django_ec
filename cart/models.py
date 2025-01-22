from django.db import models
from django.shortcuts import get_object_or_404

from shop.models import Item
# Create your models here.
class Cart(models.Model):
    """
    カートを管理するモデル
    
    Attributes:
        quantities(int): カート内の商品点数
    
    Methods:
        load_from_session: リクエストのセッション情報からカートインスタンスを返す（classmethod）
        create_cart: カートインスタンスの新規作成（classmethod）
        get_total_price: カート内の商品の合計金額
    """
    SESSION_KEY = 'cart'
    
    # fields
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    class Meta:
        db_table = 'carts'
    
    @classmethod
    def load_from_session(cls, session, session_key=SESSION_KEY):
        """
        セッションからカートIDを取得し、カートインスタンスを返す。
        カートIDが存在しない場合は、Noneを返す。

        Args:
            session (SessionBase): リクエストのセッション情報
            session_key (str, optional): セッション内でカートIDを保持するキー（初期値: SESSION_KEY）

        Returns:
            Optional[Cart]: カートのインスタンス、カートが存在しない場合 None
        """
        cart_pk = session.get(session_key)
        if cart_pk is not None:
            try: 
                return cls.objects.get(pk=cart_pk)
            except cls.DoesNotExist:
                return None
        return None
    
    @classmethod
    def create_cart(cls, session, session_key=SESSION_KEY):
        """
        カートを新規作成し、DBとセッションに登録する。

        Args:
            session (SessionBase): リクエストのセッション情報
            session_key (str, optional): セッション内でカートIDを保持するキー（初期値: SESSION_KEY）

        Returns:
            Cart: カートのインスタンス
        """
        cart = cls.objects.create()
        session[session_key] = cart.pk
        return cart

    def get_total_price(self):
        """
        カート内の商品の小計を合算し、カート内の合計金額を返す。

        Returns:
            int: カート内の商品の合計金額
        """
        cart_items = self.items.select_related('item')
        total_price = sum(cart_item.sub_total for cart_item in cart_items)
        return total_price
    
    @property
    def quantities(self):
        """
        カート内の商品点数を返す。

        Returns:
            int: カート内の商品点数
        """
        cart_items = self.items.select_related('item')
        quantities = sum(cart_item.quantity for cart_item in cart_items)
        return quantities
        
    def __str__(self):
        return f'{self.pk}'


class CartItem(models.Model):
    """
    カート内の商品を管理するモデル

    Fields:
        cart(ForeignKey): 関連するカート
        item(ForeignKey): カートに入っている商品
        quantity(int): 商品の数量
    
    Attributes:
        sub_total(int): 商品の小計

    Methods:
        add_item: カートに商品を追加する（classmethod）
        delete_item: カートから指定の商品を削除する（classmethod）
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        ordering = ['created_at']
    
    @classmethod
    def add_item(cls, cart, item, quantity=1):
        """
        カートに商品を追加する。既に同じ商品が存在する場合は、数量を加算する。

        Args:
            cart (Cart): 関連するカート
            item (Item): 追加する商品
            quantity (int, optional): カートに追加する商品の数量（初期値: 1）

        Returns:
            CartItem: 新規作成または更新されたカートアイテム
        """
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item
    
    @classmethod
    def delete_item(cls, cart, item):
        """
        カートから指定の商品を削除する。

        Args:
            cart (Cart): 関連するカート
            item (Item): 追加する商品
        Raises:
            Http404: 指定のカートアイテムが存在しない場合
        """
        cart_item = get_object_or_404(cls, cart_id=cart, item_id=item)
        cart_item.delete()
    
    @property
    def sub_total(self):
        """
        商品の小計を計算する。

        Returns:
            int: 商品単価 x 数量
        """
        return self.item.price * self.quantity
    
    def __str__(self):
        return f'cart: {self.cart.pk} - item: {self.item.name} x {self.quantity}'
    