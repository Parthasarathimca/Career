from django.contrib import admin
from .models import *
from COS.core.utils import DisableDeleteAdmin

# Register your models here.

admin.site.register(EdgeType, DisableDeleteAdmin)
admin.site.register(BoardColor, DisableDeleteAdmin)
admin.site.register(MaterialType, DisableDeleteAdmin)
admin.site.register(InventoryExtra, DisableDeleteAdmin)
admin.site.register(HardwareCategory, DisableDeleteAdmin)
admin.site.register(HardwareInventory, DisableDeleteAdmin)
admin.site.register(MarketingInventory, DisableDeleteAdmin)
admin.site.register(Inventory)
