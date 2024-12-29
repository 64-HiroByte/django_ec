from django.contrib import admin

from purchase.models import CreditCard
from purchase.models import Prefecture
from purchase.models import Purchaser
from purchase.models import ShippingAddress

# Register your models here.
admin.site.register(CreditCard)
admin.site.register(Prefecture)
admin.site.register(Purchaser)
admin.site.register(ShippingAddress)