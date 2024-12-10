from django.db import models

from shop.models import Item
# Create your models here.
class Cart(models.Model):
    class Meta:
        db_table = 'carts'
    
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def get_total_price(self):
        return sum(item.get_sub_total() for item in self.items.all())
        
    # def __str__(self):
    #     return self.name


class CartItem(models.Model):
    class Meta:
        db_table = 'cart_items'
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    def get_sub_total(self):
        return self.item.price * self.quantity
    
    # def __str__(self):
    #     return self.name
    