from django.contrib import admin
from system.models import *
# Register your models here.

admin.site.register(Vendor)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BankAccount)