from room_options.conf import WoodPanelType
from room_options.models.partition_models.room_map_models import GlassTypeMapModel, CustomPartitionDrillMap
from django.contrib import admin
from COS.core.utils import DisableDeleteAdmin
from room_options.custom_admin import CategoryAdmin, MaterialAdmin, EdgeTypeAdmin
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
from room_options.models.custom_models.custom_models import *
from room_options.models.LTI_doors_models.LTI_models import *
from room_options.models.wood_door_models.main_models import *




# Register your models here.

# admin.site.register(RoomDrillModelMap)
# admin.site.register(RoomDescriptionMapModel)
admin.site.register(DoorOpeningheightWidthMapModel,DisableDeleteAdmin)
admin.site.register(DoorOpeningSizeMapModel,DisableDeleteAdmin)
admin.site.register(DoorDrillMapModel,DisableDeleteAdmin)
admin.site.register(GlassTypeMapModel,DisableDeleteAdmin)
admin.site.register(DrawerSizeMapModel,DisableDeleteAdmin)
admin.site.register(KdInsertBacking,DisableDeleteAdmin)
admin.site.register(KdDepth,DisableDeleteAdmin)
admin.site.register(KdWidth,DisableDeleteAdmin)
admin.site.register(KdMaterial,DisableDeleteAdmin)
admin.site.register(KdEdge,DisableDeleteAdmin)
admin.site.register(DoorSingleOpeningSizeMapModel,DisableDeleteAdmin)
admin.site.register(DoorSingleOpeningheightWidthMapModel,DisableDeleteAdmin)
admin.site.register(RoomOptionsMasterModel,DisableDeleteAdmin)
admin.site.register(AdjMaterial,DisableDeleteAdmin)
admin.site.register(AdjWidth,DisableDeleteAdmin)
admin.site.register(AdjDepth,DisableDeleteAdmin)
admin.site.register(AdjEdge,DisableDeleteAdmin)
admin.site.register(AdjInsertBacking,DisableDeleteAdmin)
admin.site.register(AdjExposedEnd,DisableDeleteAdmin)
admin.site.register(CustomMapCategory, CategoryAdmin)
admin.site.register(CustomMapMaterial,MaterialAdmin)
admin.site.register(CustomMapBoardColor, DisableDeleteAdmin)
admin.site.register(CustomMapEdgeProfile, DisableDeleteAdmin)
admin.site.register(CustomMapEdgeType, EdgeTypeAdmin)
admin.site.register(CustomMapEdgeColor, DisableDeleteAdmin)
admin.site.register(CustomStainColor, DisableDeleteAdmin)
admin.site.register(CustomMapDrill, DisableDeleteAdmin)

admin.site.register(DoorDrawerBaseTypeMapModel, DisableDeleteAdmin)
admin.site.register(SolidDoorMapModel, DisableDeleteAdmin)
admin.site.register(DoorGlassOptionsMapModel, DisableDeleteAdmin)
admin.site.register(DoorColorsMapModel, DisableDeleteAdmin)
admin.site.register(DoorSizeMapModel, DisableDeleteAdmin)
admin.site.register(LTIDrawerSizeMapModel, DisableDeleteAdmin)
admin.site.register(WoodDoorColorChoiceMap, DisableDeleteAdmin)
admin.site.register(WoodDoorDrawerStyleMapModel, DisableDeleteAdmin)
admin.site.register(WoodSpeciesMapModel, DisableDeleteAdmin)
admin.site.register(WoodDrawerSizeMapModel, DisableDeleteAdmin)
admin.site.register(WoodDoorDrawerSizeMapModel, DisableDeleteAdmin)
admin.site.register(CustomPartitionDrillMap, DisableDeleteAdmin)

