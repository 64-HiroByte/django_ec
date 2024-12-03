import dataclasses
from dataclasses import dataclass


@dataclass
class CartItem:
    """カートに追加する商品
    
    Attribute:
        sub_total(int): カートに追加した商品の小計
    """
    pk: int
    name: str
    price: int
    quantity: int = 0
    
    @property
    def sub_total(self):
        return self.price * self.quantity


@dataclass
class Cart:
    """CartItemをリスト内に格納するデータクラス

    Attribute:
        total_price(int): カートに入っている商品の合計金額
    Methods:
        add_item: カートに商品を追加する（カート内に同一商品がある場合は数量を更新する）
        delete_item: カートから商品を削除する
        load_session_data: セッションデータからカートオブジェクトを復元する
        create_from_session: セッションデータの有無を元にカートオブジェクトを生成する
        save_to_session: カートの情報をセッションに保存する
        get_quantities_in_cart: カートに入っている商品点数を取得する
    """
    items_in_cart: list[CartItem]= dataclasses.field(default_factory=list)
    
    @property
    def total_price(self):
        """
        以下のリスト内包表記でも同じ結果が得られる
        return sum(item_in_cart.sub_total for item_in_cart in self.items_in_cart)

        今回はコードの可読性を優先し、一般的なループ処理とした
        """ 
        total_price = 0
        for item_in_cart in self.items_in_cart:
            total_price += item_in_cart.sub_total
        return total_price
    
    def add_item(self, item, quantity=1):
        """商品をカートに追加または数量を更新する

        Args:
            item (object): 商品オブジェクト
            quantity (int, optional): カートに追加する商品の数量（初期値: 1）
        """
        # カート内に選択した商品がある場合は数量を更新する
        for item_in_cart in self.items_in_cart:
            if item_in_cart.pk == item.pk:
                item_in_cart.quantity += quantity
                return
        # カート内に選択した商品がない場合は追加する
        cart_item = CartItem(
            pk=item.pk, name=item.name, price=item.price, quantity=quantity
            )
        self.items_in_cart.append(cart_item)
    
    def delete_item(self, item_pk):
        """カートから選択した商品を削除する

        Args:
            item_pk (int): 選択した商品のpk(primary key)
        """
        for item_in_cart in self.items_in_cart:
            if item_in_cart.pk == item_pk:
                self.items_in_cart.remove(item_in_cart)
                return

    @classmethod
    def load_session_data(cls, items_in_session):
        """セッションデータからカートオブジェクトを復元する

        Args:
            items_in_session (list): セッションに保存されている商品情報（dict）を格納したリスト

        Returns:
            object: カートオブジェクト
        """
        cart = cls()
        for item_data in items_in_session:
            cart_item = CartItem(**item_data)
            cart.items_in_cart.append(cart_item)
        return cart
    
    @classmethod
    def create_from_session(cls, session_data, session_key):
        """セッションデータの有無を元にカートオブジェクトを生成する

        Args:
            session_data (dict): セッションデータの辞書オブジェクト
            session_key (str): セッションキー

        Returns:
            object: カートオブジェクト
        """
        items_in_session = session_data.get(session_key)
        if items_in_session:
            cart = cls.load_session_data(items_in_session)
        else:
            cart = cls()
        return cart
    
    def save_to_session(self, session_data, session_key):
        """カートの情報をセッションに保存する

        Args:
            session_data (dict): セッションデータの辞書オブジェクト
            session_key (str): セッションキー
        """
        session_data[session_key] = dataclasses.asdict(self)['items_in_cart']
    
    @classmethod
    def get_quantities_in_cart(cls, session_data, session_key):
        """カートに入っている商品点数を取得する

        Args:
            session_data (dict): セッションデータの辞書オブジェクト
            session_key (str): セッションキー

        Returns:
            int: カート内に入っている商品点数
        """
        cart = cls.create_from_session(session_data, session_key)
        quantities_in_cart = 0
        for item_in_cart in cart.items_in_cart:
            quantities_in_cart += item_in_cart.quantity
        return quantities_in_cart
