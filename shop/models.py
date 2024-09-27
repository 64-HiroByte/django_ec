from django.db import models

# Create your models here.
class item(models.Model):
    item_name = models.CharField(max_length=100)
    item_image = models.ImageField()
    item_price = models.IntegerField()
    # item_rating
    