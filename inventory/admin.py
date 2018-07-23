from django.contrib import admin
from .models import *


admin.site.register(Furniture)
admin.site.register(Property)
admin.site.register(Warehouse)
admin.site.register(Cart)
admin.site.register(CartFurniture)
admin.site.register(PropertyFurniture)
admin.site.register(WarehouseFurniture)
