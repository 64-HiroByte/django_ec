from django.db import models

# Create your models here.
class Item(models.Model):
    """
    商品を管理するモデル
    
    Fields:
        name(str): 商品名
        price(int): 価格
        image(image): 商品の画像
        description(str): 商品の説明文
    """
    name = models.CharField(verbose_name='商品名', max_length=100)
    price = models.IntegerField(verbose_name='価格')
    image = models.ImageField(verbose_name='商品画像', upload_to='images/', blank=True, null=True)
    description = models.TextField(verbose_name='説明')
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    # rating は現状で設定しない

    class Meta:
        db_table = 'items'
    
    def __str__(self):
        return self.name