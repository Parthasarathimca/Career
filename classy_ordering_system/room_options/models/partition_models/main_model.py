import uuid

from django.db import models
from django.db.models.deletion import SET_NULL
from COS.core.utils import TimestampedModel
from franchise.models import RoomModel,JobStatus
from room_options.conf import EdgeProfile, DogEared, LTIDoorType,LTIDrawerType, LTIOverlayOptions, LTIOverlayOptions1, MTChoices, CLEAT_EXPOSED_END_CHOICES, ShelfTypeChoices, \
    ShelfPartitionChoices, EXPOSED_END_CHOICES, FACE_COLOR_CHOICES, TOE_KICK_DEPTH_CHOICES, DrawerHole, \
    DrawerDrilSubFront, DrawerhamperTypes, PartitionCustomDrillPattern, DRAWER_SIZE_CHOICES, SUB_FRONT_CHOICES, \
    DrawerBoxType, DRAWER_BOX_SIDE_CHOICES, WoodPanelType, WOODDoorType
from franchise.models import RoomMatTypeModelMap, RoomEdgeType
from .room_map_models import *
from room_options.models.kd_shelf_models.kd_models import KdInsertBacking, KdEdge
from room_options.models.adj_shelf_models.main_model import AdjExposedEnd, AdjInsertBacking, AdjEdge
from room_options.models.drawerbox_models.main_model import DrawerBox
from inventory_options.models import BoardColor, Inventory
from room_options.models.LTI_doors_models.LTI_models import *

from franchise.conf import *
from room_options.models.wood_door_models.main_models import *
from ..toe_kicks_models.main_models import ToeKick


class RoomOptionsMasterModel(TimestampedModel):

    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, related_name="job_room_option", blank=True, null=True)
    description = models.CharField(('Description'), max_length=50,blank=True,null=True)
    description2 = models.CharField(('Description2'), max_length=255, null=True, blank=True)
    UOM = models.CharField(('UOM'), max_length=15,blank=True ,null=True)
    height = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    width = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    depth = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    quantity = models.BigIntegerField('Quantity',blank=True,null=True)
    holes= models.DecimalField(('Holes'), decimal_places=2, max_digits=20,blank=True,null=True)

    #partition
    # to be removed
    drill_pattern_height = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    drill_pattern_width = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    drill_pattern_depth = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)

    drill_pattern_left = models.BooleanField(default=False,blank=True,null=True)
    drill_pattern_right = models.BooleanField(default=False,blank=True,null=True)
    custom_drill_pattern_left = models.SmallIntegerField(choices=PartitionCustomDrillPattern.DRILL_PATTERN_CHOICES, null=True, blank=True)
    custom_drill_pattern_right = models.SmallIntegerField(choices=PartitionCustomDrillPattern.DRILL_PATTERN_CHOICES, null=True, blank=True)

    custom_drill_code_rgt = models.ForeignKey('room_options.CustomPartitionDrillMap', on_delete=models.CASCADE,
                                                blank=True, null=True, related_name="right_custom_drill_map")
    custom_drill_code_lft = models.ForeignKey('room_options.CustomPartitionDrillMap', on_delete=models.CASCADE,
                                              blank=True, null=True, related_name="left_custom_drill_map")

    left_side_drill_depth = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    left_side_drill_height = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    right_side_drill_depth = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    right_side_drill_height = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    mat_type = models.SmallIntegerField(choices=MTChoices.PARTION_MT_CHOICES, null=True, blank=True)
    part_sub_category = models.CharField(max_length=20,blank=True,null=True)
    edge_profile = models.SmallIntegerField(choices=EdgeProfile.EDGE_PROFILE_CHOICES, null=True, blank=True)
    ed_type = models.ForeignKey(RoomEdgeType, on_delete=models.CASCADE, related_name="room_option_ed_type", null=True, blank=True )
    left_3rd_line_hole = models.BooleanField(null=True, blank=True)
    right_3rd_line_hole = models.BooleanField(null=True, blank=True)
    dog_eared = models.SmallIntegerField(choices=DogEared.DOG_EARED_CHOICES, null=True, blank=True)
    
    #Pair Door 
    door_glass_type = models.ForeignKey(GlassTypeMapModel, on_delete=models.CASCADE, related_name="glass_types",blank=True,null=True)
    door_opening_size = models.ForeignKey(DoorOpeningSizeMapModel, on_delete=models.CASCADE, related_name="door_openigs",blank=True,null=True)
    #Single Door
    door_single_opening_size = models.ForeignKey(DoorSingleOpeningSizeMapModel, on_delete=models.CASCADE, related_name="door_single_openigs",blank=True,null=True)
    door_drill_option = models.ForeignKey(DoorDrillMapModel, on_delete=models.CASCADE, related_name="door_drill_optoins",blank=True,null=True)
    notes = models.CharField(('notes'), max_length=255, null=True, blank=True)
    door_class_insert = models.BooleanField(default=False,blank=True,null=True)

    # kd shelve
    insert_backing = models.ForeignKey(KdInsertBacking, on_delete=models.CASCADE, related_name="kd_shelf_insert_backing", blank=True, null=True)
    kd_shelf_edge = models.ForeignKey(KdEdge, on_delete=models.CASCADE, related_name="kd_shelf_edge", blank=True, null=True)

    #cleets
    cleat_exposed_ends = models.CharField(max_length=20, choices=CLEAT_EXPOSED_END_CHOICES, null=True, blank=True)
    
    #L -shelf
    width2 = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    depth2 = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    notch_mitered_pard=models.BooleanField(default=False, blank=True, null=True)
    shelf_type = models.SmallIntegerField(choices=ShelfTypeChoices.SHELF_TYPE_CHOICES, null=True, blank=True)
    shelfs_partitions=models.SmallIntegerField(choices=ShelfPartitionChoices.SHELF_PARTITION_CHOICES, null=True, blank=True)
    drill_toe_kick=models.BooleanField(default=False, blank=True, null=True)

    #Top Shelf
    exposed_ends = models.CharField(max_length=20, choices=EXPOSED_END_CHOICES, null=True, blank=True)
    # edgebanding=models.BooleanField(default=False, blank=True, null=True)

    #Adjustable Shelves
    adj_insert_backing = models.ForeignKey(AdjInsertBacking, on_delete=models.CASCADE, related_name="adj_shelf_insert_backing", blank=True, null=True)
    adj_shelf_edge = models.ForeignKey(AdjEdge, on_delete=models.CASCADE, related_name="adj_shelf_edge", blank=True, null=True)
    adj_exposed_end = models.ForeignKey(AdjExposedEnd, on_delete=models.CASCADE, related_name="adj_exposed_end", blank=True, null=True)
    #toe Kick
    toe_kick_form = models.ForeignKey(ToeKick, null=True, blank=True,
                                        on_delete=models.CASCADE, related_name='toe_kick_facets')

    plywood = models.BooleanField(default=False, blank=True, null=True)
    #Dwawer Faces
    drawer_faces_holes= models.CharField(max_length=20, choices=DrawerHole.HOLE_CHOICES, null=True, blank=True)
    drawer_faces_drill_Sub_front= models.CharField(max_length=20, choices=DrawerDrilSubFront.DRILL_SUB_FRONT_CHOICES, null=True, blank=True)
    # drawer_faces_hamper_type=models.CharField(max_length=20, choices=DrawerhamperTypes.HAMPER_FACES_TYPES, null=True, blank=True)
    drawer_faces_hamper_faces=models.BooleanField(default=False, blank=True, null=True)
    
    #Drawer Box
    drawer_box_form = models.ForeignKey(DrawerBox, null=True, blank=True,
                                         on_delete=models.CASCADE, related_name='drawer_box_facets')

    # inventry
    inventory = models.ForeignKey(Inventory, models.CASCADE, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=orderStatus.STATUS_CHOICES, default='INPROGRESS')
    

    #custom
    custom_bd_color = models.ForeignKey('room_options.CustomMapBoardColor', models.CASCADE, null=True, blank=True, related_name='board_color_room_options')
    custom_drill_left = models.ForeignKey('room_options.CustomMapDrill', models.CASCADE, null=True, blank=True, related_name='drill_left_room_options')
    custom_drill_right = models.ForeignKey('room_options.CustomMapDrill', models.CASCADE, null=True, blank=True, related_name='drill_right_room_options')
    custom_st_color = models.ForeignKey('room_options.CustomStainColor', models.CASCADE, null=True, blank=True, related_name='stain_color_room_options')
    custom_material = models.ForeignKey('room_options.CustomMapMaterial', models.CASCADE, null=True, blank=True, related_name='material_room_options')
    l1ep = models.ForeignKey('room_options.CustomMapEdgeProfile', models.CASCADE, null=True, blank=True, related_name='custom_edge_profile_l1')
    l1et = models.ForeignKey('room_options.CustomMapEdgeType', models.CASCADE, null=True, blank=True, related_name='custom_edge_type_l1')
    l1ec = models.ForeignKey('room_options.CustomMapEdgeColor', models.CASCADE, null=True, blank=True, related_name='custom_edge_color_l1')

    l2ep = models.ForeignKey('room_options.CustomMapEdgeProfile', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_profile_l2')
    l2et = models.ForeignKey('room_options.CustomMapEdgeType', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_type_l2')
    l2ec = models.ForeignKey('room_options.CustomMapEdgeColor', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_color_l2')

    s1ep = models.ForeignKey('room_options.CustomMapEdgeProfile', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_profile_s1')
    s1et = models.ForeignKey('room_options.CustomMapEdgeType', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_type_s1')
    s1ec = models.ForeignKey('room_options.CustomMapEdgeColor', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_color_s1')

    s2ep = models.ForeignKey('room_options.CustomMapEdgeProfile', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_profile_s2')
    s2et = models.ForeignKey('room_options.CustomMapEdgeType', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_type_s2')
    s2ec = models.ForeignKey('room_options.CustomMapEdgeColor', models.CASCADE, null=True, blank=True,
                             related_name='custom_edge_color_s2')
                        
    #LTI Doors
    droor_drawer_base_type=models.ForeignKey(DoorDrawerBaseTypeMapModel, on_delete=models.CASCADE, related_name="door_drawer_base_types", blank=True, null=True)
    solid_door=models.ForeignKey(SolidDoorMapModel, on_delete=models.CASCADE, related_name="solid_doors", blank=True, null=True)
    glass_options=models.ForeignKey(DoorGlassOptionsMapModel, on_delete=models.CASCADE, related_name="glass_options", blank=True, null=True)
    lti_door_color=models.ForeignKey(DoorColorsMapModel, on_delete=models.CASCADE, related_name="lti_door_color", blank=True, null=True)
    lti_door_size=models.ForeignKey(DoorSizeMapModel, on_delete=models.CASCADE, related_name="lti_door_size", blank=True, null=True)
    lti_door_type= models.CharField(max_length=20, choices=LTIDoorType.DOOR_TYPES, null=True, blank=True)
    overlay_options= models.CharField(max_length=20, choices=LTIOverlayOptions.OVERLAY_OPTIONS, null=True, blank=True)
    overlay_options1= models.CharField(max_length=500, null=True, blank=True)
    
    drawer_type= models.CharField(max_length=20, choices=LTIDrawerType.DRAWER_TYPES, null=True, blank=True)
    lti_drawer_size=models.ForeignKey(LTIDrawerSizeMapModel, on_delete=models.CASCADE, related_name="lti_drawer_size", blank=True, null=True)
    
    # Wood Doors
    glazing = models.BooleanField(default=False, null=True, blank=True)
    wood_panel_type = models.CharField(max_length=20, choices=WoodPanelType.PANEL_OPTIONS, null=True, blank=True)
    wood_door_style = models.ForeignKey(WoodDoorDrawerStyleMapModel, on_delete=models.CASCADE, related_name="wood_door_style", null=True, blank=True)
    wood_species = models.ForeignKey(WoodSpeciesMapModel, on_delete=models.CASCADE, related_name="wood_door_species", null=True, blank=True)
    wood_door_size = models.ForeignKey(WoodDrawerSizeMapModel, on_delete=models.CASCADE, related_name="wood_door_size", null=True, blank=True)
    wood_stain_color = models.ForeignKey(WoodDoorColorChoiceMap, on_delete=models.CASCADE, related_name="wood_door_stain", null=True, blank=True)    
    wood_door_french_lite = models.CharField(max_length=20, choices=WoodPanelType.FRENCH_LITES, null=True, blank=True)
    wood_door_custom_size = models.CharField(max_length=55, null=True, blank=True)
    wood_drawer_type = models.CharField(max_length=55, choices=WOODDoorType.DOOR_TYPES, null=True, blank=True)
    wood_drawer_size = models.ForeignKey(WoodDoorDrawerSizeMapModel, on_delete=models.CASCADE, related_name="wood_drawer_type", null=True, blank=True)
    wood_door_material_type = models.CharField(max_length=55, null=True, blank=True)
    
    #job status
    job_status=models.ForeignKey(JobStatus,on_delete=SET_NULL, related_name="job_Status", blank=True, null=True)

    def __str__(self):
        return str(self.room)
    
    class Meta:
        db_table = "room_options_master"
        verbose_name = "Room Option Master"
        verbose_name_plural = "Room Options Master"

