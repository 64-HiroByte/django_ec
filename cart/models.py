from django.db import models

from shop.models import Item
# Create your models here.
class Cart(models.Model):
    class Meta:
        db_table = 'carts'
    
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def get_total_price(self):
        cart_items = self.items.select_related('item')
        total_price = sum(cart_item.sub_total for cart_item in cart_items)
        return total_price
    
    @property
    def quantities(self):
        cart_items = self.items.select_related('item')
        quantities = sum(cart_item.quantity for cart_item in cart_items)
        return quantities
        
    def __str__(self):
        return f'{self.pk}'


class CartItem(models.Model):
    class Meta:
        db_table = 'cart_items'
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    @classmethod
    def add_item(cls, cart, item, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item
    
    @property
    def sub_total(self):
        return self.item.price * self.quantity
    
    def __str__(self):
        return f'cart: {self.cart.pk} - item: {self.item.name} x {self.quantity}'
    