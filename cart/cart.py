import dataclasses
from dataclasses import dataclass


@dataclass
class CartItem:
    '''カートに追加する商品'''
    pk: int
    name: str
    price: int
    quantity: int = 0
    
    @property
    def sub_total(self):
        return self.price * self.quantity


@dataclass
class Cart:
    items_in_cart: list[CartItem]= dataclasses.field(default_factory=list)
    
    @property
    def total_price(self):
        total_price = 0
        for item_in_cart in self.items_in_cart:
            total_price += item_in_cart.sub_total
        return total_price
        # 上記内容は以下のリスト内包表記でもいいが、可読性を向上させるためにループ処理とした
        # return sum(item_in_cart.sub_total for item_in_cart in self.items_in_cart)
    
    def add_item(self, item, quantity=1):
        '''
        カートに商品を追加
        '''
        # update処理
        for item_in_cart in self.items_in_cart:
            if item_in_cart.pk == item.pk:
                item_in_cart.quantity += quantity
                return
            
        cart_item = CartItem(
            pk=item.pk, name=item.name, price=item.price, quantity=quantity
            )
        self.items_in_cart.append(cart_item)
    
    def delete_item(self, item_pk):
        for item_in_cart in self.items_in_cart:
            if item_in_cart.pk == item_pk:
                self.items_in_cart.remove(item_in_cart)
                return

    def clear(self):
        '''
        カート内の商品を一括削除
        '''
        self.items_in_cart.clear()
    
    # save_to_sessionに直接記述した
    # def to_dict(self):
    #     '''
    #     カート内の商品を辞書型に変換
    #     '''
    #     return dataclasses.asdict(self)['items_in_cart']
    
    @classmethod
    def load_session_data(cls, items_in_session):
        '''
        保存されているデータからカートのインスタンスを復元するファクトリーメソッド
        '''
        cart = cls()
        for item_data in items_in_session:
            cart_item = CartItem(**item_data)
            cart.items_in_cart.append(cart_item)
        return cart
    
    @classmethod
    def create_from_session(cls, session_data, session_key):
        '''
        セッションデータからカートのインスタンスを生成するファクトリーメソッド
        '''
        items_in_session = session_data.get(session_key)
        if items_in_session:
            cart = cls.load_session_data(items_in_session)
        else:
            cart = cls()
        return cart
    
    def save_to_session(self, session_data, session_key):
        '''
        カートの情報をセッションに保存
        '''
        # session_data[session_key] = self.to_dict()
        session_data[session_key] = dataclasses.asdict(self)['items_in_cart']
    
    @classmethod
    def get_quantities_in_cart(cls, session_data, session_key):
        cart = cls.create_from_session(session_data, session_key)
        quantities_in_cart = 0
        for item_in_cart in cart.items_in_cart:
            quantities_in_cart += item_in_cart.quantity
        return quantities_in_cart
    
    def __str__(self):
        return f'Cart:{self.items_in_cart}'
