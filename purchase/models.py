from django.db import models

class Prefecture(models.Model):
    """
    都道府県名のモデル、住所を入力する際の選択肢として使用する

    Attributes:
        neme(str): 都道府県名
    """
    name = models.CharField(verbose_name='都道府県名', max_length=10)
    
    class Meta:
        db_table = 'prefectures'
    
    def __str__(self):
        return self.name


class User(models.Model):
    """
    ユーザー情報を管理するモデル
    
    Attributes:
        user_name(str): ユーザーネーム（ユニーク制約）
        family_name(str): 氏名の姓の部分（first_nameと同じ）
        given_name(str): 氏名の名の部分（last_nameと同じ）
        email(str): メールアドレス
    """
    user_name = models.CharField(verbose_name='ユーザーネーム', max_length=255, unique=True)
    family_name = models.CharField(verbose_name='姓', max_length=255)
    given_name = models.CharField(verbose_name='名', max_length=255)
    email = models.EmailField(verbose_name='メールアドレス')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.user_name

class Address(models.Model):
    """
    ユーザーの住所を管理するモデル
    
    Attributes:
        user(str): 関連するユーザーネーム（１対１リレーション）
        country(str): 国名（入力可能な選択肢は'日本'のみ）
        prefecture(ForeignKey): 都道府県名
        zip_code(str): 郵便番号（７桁の数字、ハイフンを含まない）
        address(str): 住所（都道府県名を含まない）
        building(str, optional): 住所に続く建物の名称等
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    # 住所
    country = models.CharField(verbose_name='国', max_length=255)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.PROTECT)
    zip_code = models.CharField(verbose_name='郵便番号', max_length=7)  # ハイフン除く
    address = models.CharField(verbose_name='住所', max_length=255)
    building = models.CharField(verbose_name='住所（建物名など）', max_length=255, blank=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    class Meta:
        db_table = 'addresses'
    
    def __str__(self):
        return f'{self.user} - address'


class CreditCard(models.Model):
    """
    ユーザーのクレジットカードを管理するモデル
    important: 
        課題の要件に基づき、クレジットカード番号を平文で保存している（本来はStripeなどの決済会社が発行するハッシュ値を保存する）。
    )
    
    Attributes:
        user(str): 関連するユーザーネーム（１対１リレーション）
        cardholder(str):カードの名義人
        card_number(str): カード番号（16桁の数字、ハイフンを含まない）
        card_expiration(date): カードの有効期限
        cvv(str): セキュリティコード（3桁の数字）
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credit_card')
    # クレジットカード
    cardholder = models.CharField(verbose_name='カード名義人', max_length=255)
    card_number = models.CharField(verbose_name='カード番号', max_length=16)  # 16桁
    card_expiration = models.DateField(verbose_name='有効期限',)
    cvv = models.CharField(verbose_name='セキュリティコード', max_length=3)  # ３桁
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    
    def __str__(self):
        return f'{self.user} - credit_card(****{self.card_number[-4:]})'

