import dataclasses
from dataclasses import dataclass


@dataclass
class CartItem:
    '''カートに追加する商品'''

    id: int
    name: str
    price: int


@dataclass
class Cart:
    items_in_cart: list[CartItem]= dataclasses.field(default_factory=list)
    
    def add_item(self, item):
        '''
        カートに商品を追加
        '''
        cart_item = CartItem(id=item.pk, name=item.name, price=item.price)
        self.items_in_cart.append(cart_item)

    def clear(self):
        '''
        カート内の商品を一括削除
        '''
        self.items_in_cart.clear()
    
    def to_dict(self):
        '''
        カート内の商品を辞書型に変換
        '''
        return dataclasses.asdict(self)['items_in_cart']
    
    @classmethod
    def create_from_data(cls, items_data):
        '''
        保存されているデータからカートのインスタンスを生成するファクトリーメソッド
        '''
        cart = cls()
        for item_data in items_data:
            cart_item = CartItem(**item_data)
            cart.add_item(cart_item)
        return cart
    
    @classmethod
    def create_from_session(cls, session_data, key):
        '''
        セッションデータからカートのインスタンスを生成するファクトリーメソッド
        '''
        cart_data = session_data.get(key)
        if cart_data:
            cart = cls.create_from_data(cart_data)
        else:
            cart = cls()
        return cart
    
    def save_to_session(self, session_data, key):
        '''
        カートの情報をセッションに保存
        '''
        session_data[key] = self.to_dict()
    
    def __str__(self):
        return f'Cart:{self.items_in_cart}'
