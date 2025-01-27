from django.db import models

from purchase.utils import convert_expiration_string_to_date
from purchase.utils import create_information_dict
from purchase.varidators import ValidateDigitsNumber
from purchase.varidators import validate_expiration_date
from shop.models import Item


class Prefecture(models.Model):
    """
    都道府県名のモデル、住所を入力する際の選択肢として使用する

    Fields:
        pref_name(str): 都道府県名
    """
    pref_name = models.CharField(verbose_name='都道府県名', max_length=10)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    class Meta:
        db_table = 'prefectures'
        ordering = ['id']
    
    def __str__(self):
        return self.pref_name


class Purchaser(models.Model):
    """
    購入者を管理するモデル
    
    Fields:
        user_name(str): ユーザーネーム
        family_name(str): 氏名の姓の部分（first_nameと同じ）
        given_name(str): 氏名の名の部分（last_nameと同じ）
        email(str): メールアドレス
    """
    SESSION_KEY = 'purchaser'
    
    user_name = models.CharField(verbose_name='ユーザーネーム', max_length=255)
    family_name = models.CharField(verbose_name='姓', max_length=255)
    given_name = models.CharField(verbose_name='名', max_length=255)
    email = models.EmailField(verbose_name='メールアドレス')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        db_table = 'purchasers'
    
    @classmethod
    def save_to_session(cls, session, purchaser_id, session_key=SESSION_KEY):
        """
        セッションに購入者情報を保存する
        
        Args:
            session(SessionBase): リクエストのセッション情報
            purchaser_id(int): 購入者ID
            session_key(str, optional): セッション内で購入者IDを保持するキー（初期値: SESSION_KEY）
        """
        session[session_key] = purchaser_id
    
    @classmethod
    def load_from_session(cls, session, session_key=SESSION_KEY):
        """
        セッションから購入者情報を取得する
        
        Args:
            session(SessionBase): リクエストのセッション情報
            session_key(str, optional): セッション内で購入者IDを保持するキー（初期値: SESSION_KEY）
        
        Returns:
            Purchaser: セッション内に保存されている購入者情報
        """
        purchaser_id = session.get(session_key)
        if purchaser_id is None:
            return None
        return cls.objects.get(pk=purchaser_id)

    @property
    def full_name(self):
        """
        購入者の氏名を返す

        Returns:
            str: 購入者の氏名（姓と名の間に半角スペースあり）
        """
        return f'{self.family_name} {self.given_name}'
    
    @property
    def informations(self):
        html_template_keys = ('氏名', 'ユーザーネーム', 'メールアドレス')
        mail_template_keys = ('full_name', 'user_name', 'email')
        values = (self.full_name, self.user_name, self.email)
        return create_information_dict(html_template_keys, mail_template_keys, values)

    def __str__(self):
        return f'{self.full_name}@{self.user_name}'


class ShippingAddress(models.Model):
    """
    配送先住所を管理するモデル
    
    Fields:
        purchaser(OneToOne): 関連する購入者（１対１リレーション）
        zip_code(str): 郵便番号（７桁の数字、ハイフンを含まない）
        prefecture(ForeignKey): 都道府県名
        address(str): 都道府県名より後ろの住所
        building(str, optional): 住所に続く建物の名称等
    """
    ZIP_CODE_LENGTH = 7
    
    purchaser = models.OneToOneField(Purchaser, on_delete=models.CASCADE, related_name='shipping_address')
    # 住所
    zip_code = models.CharField(
        verbose_name='郵便番号',
        max_length=ZIP_CODE_LENGTH,
        validators=[
            ValidateDigitsNumber(length=ZIP_CODE_LENGTH),
        ]
    )
    prefecture = models.ForeignKey(Prefecture, on_delete=models.PROTECT)
    address = models.CharField(verbose_name='住所', max_length=255)
    building = models.CharField(verbose_name='住所（建物名など）', max_length=255, blank=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    class Meta:
        db_table = 'shipping_addresses'
    
    @property
    def full_address(self):
        """
        配送先の住所を返す

        Returns:
            str: 登録された配送先住所（建物名等の登録がある場合は、\n で改行して表示）
        """
        full_address = f'{self.prefecture}{self.address}'
        if self.building:
            full_address += f'\n{self.building}'
        return full_address
    
    @property
    def informations(self):
        html_template_keys = ('郵便番号', '配送先住所')
        mail_template_keys = ('zip_code', 'full_address')
        values = (self.zip_code, self.full_address)
        return create_information_dict(html_template_keys, mail_template_keys, values)
    
    def __str__(self):
        return f'{self.purchaser.full_name} - {self.full_address}'


class CreditCard(models.Model):
    """
    クレジットカードを管理するモデル
    Important: 
        課題の要件に基づき、クレジットカード番号を平文で保存している（本来はStripeなどの決済会社が発行するハッシュ値を保存する）。
    
    Fields:
        purchaser(OneToOne): 関連する購入者（１対１リレーション）
        cardholder(str):カードの名義人
        card_number(str): カード番号（16桁の数字、ハイフンを含まない）
        card_expiration(str): カードの有効期限（MM/YY、/を含む）
        cvv(str): セキュリティコード（3桁の数字）
    """
    CARD_NUMBER_LENGTH = 16
    CVV_LENGTH = 3
    
    purchaser = models.OneToOneField(Purchaser, on_delete=models.CASCADE, related_name='credit_card')
    # クレジットカード
    cardholder = models.CharField(verbose_name='カード名義人', max_length=255)
    card_number = models.CharField(
        verbose_name='カード番号', 
        max_length=CARD_NUMBER_LENGTH,
        validators=[
            ValidateDigitsNumber(length=CARD_NUMBER_LENGTH),
        ]
    )
    card_expiration = models.CharField(
        verbose_name='有効期限',
        max_length=5,
        validators=[
            validate_expiration_date,
        ]
    )
    cvv = models.CharField(
        verbose_name='セキュリティコード',
        max_length=CVV_LENGTH,
        validators=[
            ValidateDigitsNumber(length=CVV_LENGTH),
        ]
    )
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    @property
    def last_four_digits(self):
        """
        クレジットカード番号の末尾4桁を返す

        Returns:
            str: 登録されたクレジットカードの末尾4桁
        """
        return f'**** **** **** {self.card_number[-4:]}'
    
    @property
    def expiration_date(self):
        """
        登録されたクレジットカードの有効期限を年月日（date型）で返す

        Returns:
            date: YYYY-MM-DD に変換された日付（DDは末日）
        """
        return convert_expiration_string_to_date(self.card_expiration)
    
    @property
    def informations(self):
        html_template_keys = ('カード名義人', 'カード番号', '有効期限')
        mail_template_keys = ('cardholder', 'card_number', 'expiration_date')
        values = (self.cardholder, self.last_four_digits, self.expiration_date)
        return create_information_dict(html_template_keys, mail_template_keys, values)
    
    def __str__(self):
        return f'{self.purchaser.full_name} - {self.last_four_digits}'


class Order(models.Model):
    """
    注文履歴を管理するモデル
    
    Fields:
        purchaser(ForeignKey): 関連する購入者（多対１リレーション）
        total_price(int): 注文の合計金額
    """
    SESSION_KEY = 'order'
    
    # Fields
    purchaser = models.ForeignKey(Purchaser, on_delete=models.PROTECT, related_name='purchaser')
    total_price = models.IntegerField(verbose_name='合計金額')
    created_at = models.DateTimeField(verbose_name='購入日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
    
    @classmethod
    def save_to_session(cls, session, order_id, session_key=SESSION_KEY):
        """
        セッションに注文情報を保存する
        
        Args:
            session(SessionBase): リクエストのセッション情報
            order_id(int): 注文ID
            session_key(str, optional): セッション内で注文IDを保持するキー（初期値: SESSION_KEY）
        """
        session[session_key] = order_id
    
    @classmethod
    def load_from_session(cls, session, session_key=SESSION_KEY):
        """
        セッションから注文情報を取得する
        
        Args:
            session(SessionBase): リクエストのセッション情報
            session_key(str, optional): セッション内で注文IDを保持するキー（初期値: SESSION_KEY）
        
        Returns:
            int: セッション情報（注文ID）、セッション内にない場合はNoneを返す
        """
        return session.get(session_key)
    
    @classmethod
    def get_order_queryset(cls):
        """
        Orderモデルのクエリセットを取得する

        Returns:
            Queryset: 購入者情報、注文明細を関連付けたクエリセット
        """
        return (
            cls.objects.select_related(
                'purchaser',
                'purchaser__shipping_address',
                'purchaser__shipping_address__prefecture',
                'purchaser__credit_card'
            )
            .prefetch_related('order_detail__item')
        )
    
    def __str__(self):
        return f'{self.created_at}: {self.purchaser.full_name}'


class OrderDetail(models.Model):
    """
    注文明細を管理するモデル
    
    Fields:
        order(ForeignKey): 関連する注文履歴
        item(ForeignKey): 注文した商品
        quantity(int): 商品の数量
        sub_total(int): 商品の小計
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_detail')
    item  = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField(verbose_name='数量')
    sub_total = models.IntegerField(verbose_name='小計')
    created_at = models.DateTimeField(verbose_name='購入日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        db_table = 'order_details'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.item.name}: {self.order.purchaser.full_name}'

