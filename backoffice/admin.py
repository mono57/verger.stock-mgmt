from django.contrib import admin
from backoffice.models import ( 
    Buying, 
    BuyingEntry, 
    Dish, 
    PartitionFormulla, Portion, 
    Price, 
    Product, 
    Room)

admin.site.register(PartitionFormulla)
admin.site.register(Product)
admin.site.register(Room)
admin.site.register(Price)
admin.site.register(Dish)
admin.site.register(Buying)
admin.site.register(BuyingEntry)
admin.site.register(Portion)
# Register your models here.
