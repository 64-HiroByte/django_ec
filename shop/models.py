from django.db import models

# Create your models here.
class item(models.Model):
    name = models.CharField(verbose_name='商品名', max_length=100)
    price = models.IntegerField(verbose_name='価格')
    description = models.TextField(verbose_name='説明')
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    # rating は現状で設定しない

    def __str__(self):
        return self.name