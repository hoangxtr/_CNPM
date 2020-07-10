from django.contrib import admin
from system.models import *
# Register your models here.

admin.site.register(Vendor)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BankAccount)
admin.site.register(MyWallet)

admin.site.register(Chef)
admin.site.register(Admin)
admin.site.register(Customer)