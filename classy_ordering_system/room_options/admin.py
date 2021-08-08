from django.contrib import admin
from COS.core.utils import DisableDeleteAdmin
from room_options.models import ( RoomDescriptionMapModel, RoomOptionsMasterModel,
                                  RoomDrillModelMap, DoorOpeningheightWidthMapModel,
                                  DoorOpeningSizeMapModel, DoorDrillMapModel,
                                  DrawerSizeMapModel,
                                  DrawerSizeMapModel,DoorSingleOpeningSizeMapModel,DoorSingleOpeningheightWidthMapModel)
from room_options.models.kd_shelf_models.kd_models import ( KdInsertBacking, 
                                  KdWidth, KdDepth, KdEdge, KdMaterial
                                  ) 

from room_options.models.adj_shelf_models.main_model import ( AdjInsertBacking, AdjWidth, 
                                    AdjEdge, AdjDepth, AdjMaterial, AdjExposedEnd
                                )

# Register your models here.

admin.site.register(RoomDrillModelMap)
admin.site.register(RoomDescriptionMapModel)
admin.site.register(DoorOpeningheightWidthMapModel,DisableDeleteAdmin)
admin.site.register(DoorOpeningSizeMapModel,DisableDeleteAdmin)
admin.site.register(DoorDrillMapModel,DisableDeleteAdmin)
admin.site.register(DrawerSizeMapModel)
admin.site.register(KdInsertBacking)
admin.site.register(KdDepth)
admin.site.register(KdWidth)
admin.site.register(KdMaterial)
admin.site.register(KdEdge)
admin.site.register(DoorSingleOpeningSizeMapModel,DisableDeleteAdmin)
admin.site.register(DoorSingleOpeningheightWidthMapModel,DisableDeleteAdmin)
admin.site.register(RoomOptionsMasterModel)
admin.site.register(AdjMaterial)
admin.site.register(AdjWidth)
admin.site.register(AdjDepth)
admin.site.register(AdjEdge)
admin.site.register(AdjInsertBacking)
admin.site.register(AdjExposedEnd)


