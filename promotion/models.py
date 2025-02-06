from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class PromotionCode(models.Model):
    """
    プロモーションコードのモデル

    Fields:
        code(str): 7桁の英数字で構成されたプロモーションコードで、ユニーク制約あり
        discount_amount(int): 割引額。MIN_DISCOUNT_AMOUNT〜MAX_DISCOUNT_AMOUNTの間の整数（バリデータ適用）
        is_active(bool): 使用可能であるかを示すフラグ
    """
    # プロモーションコードの長さの制約
    MIN_CODE_LENGTH = 4
    MAX_CODE_LENGTH = 32
    # 割引額の制約
    MIN_DISCOUNT_AMOUNT = 10
    MAX_DISCOUNT_AMOUNT = 10000
    # セッションキー
    SESSION_KEY = 'promotion'
    
    # Fields
    code = models.CharField(
        verbose_name='プロモーションコード', max_length=MAX_CODE_LENGTH, unique=True
    )
    discount_amount = models.IntegerField(
        verbose_name='割引額', 
        validators=[
            MinValueValidator(MIN_DISCOUNT_AMOUNT), 
            MaxValueValidator(MAX_DISCOUNT_AMOUNT),
        ]
    )
    is_active = models.BooleanField(verbose_name='使用可能', default=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        db_table = 'promotion_codes'
        ordering = ['id']
    
    @classmethod
    def save_to_session(cls, session, promotion_id, session_key=SESSION_KEY):
        """
        セッションに適用しているプロモーションコードのIDを保存する

        Args:
            session (SessionBase): リクエストのセッション情報
            promotion_id(int): プロモーションコードのID
            session_key(str, optional): セッション内でプロモーションコードのIDを保持するキー（初期値: SESSION_KEY）
        """
        session[session_key] = promotion_id
        
    def __str__(self):
        return f'{self.code}: {self.discount_amount}円'