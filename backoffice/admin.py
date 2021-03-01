from django.contrib import admin
from backoffice.models import ( 
    Buying, 
    BuyingEntry, 
    Dish, 
    PartitionFormulla, Portion, 
    Price, 
    Product,
    ProductType,
    Room)

admin.site.register(PartitionFormulla)
admin.site.register(Product)
admin.site.register(Room)
admin.site.register(Price)
admin.site.register(Dish)
admin.site.register(Buying)
admin.site.register(BuyingEntry)
admin.site.register(Portion)
admin.site.register(ProductType)
# Register your models here.
