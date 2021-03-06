from django.contrib import admin
from backoffice.models import ( 
    Buying, 
    BuyingEntry, 
    Dish, Drink, Invoice, InvoiceEntry, 
    PartitionFormulla, Portion, 
    Price, 
    Product,
    ProductType,
    Room, Transfert, Drink)

admin.site.register(PartitionFormulla)
admin.site.register(Product)
admin.site.register(Room)
admin.site.register(Price)
admin.site.register(Dish)
admin.site.register(Buying)
admin.site.register(BuyingEntry)
admin.site.register(Portion)
admin.site.register(Drink)
admin.site.register(Invoice)
admin.site.register(InvoiceEntry)
admin.site.register(ProductType)
admin.site.register(Transfert)
# Register your models here.
