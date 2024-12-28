from django.contrib import admin

from purchase.models import Address
from purchase.models import CreditCard
from purchase.models import Prefecture
from purchase.models import User

# Register your models here.
admin.site.register(Address)
admin.site.register(CreditCard)
admin.site.register(Prefecture)
admin.site.register(User)