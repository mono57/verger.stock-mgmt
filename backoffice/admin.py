from django.contrib import admin
from backoffice.models import Dish, PartitionFormulla, Price, Product, Room

admin.site.register(PartitionFormulla)
admin.site.register(Product)
admin.site.register(Room)
admin.site.register(Price)
admin.site.register(Dish)
# Register your models here.
