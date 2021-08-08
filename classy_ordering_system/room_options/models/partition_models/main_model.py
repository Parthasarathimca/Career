from django.db import models
from COS.core.utils import TimestampedModel
from franchise.models import RoomModel
from room_options.conf import EdgeProfile, DogEared, MTChoices, CLEAT_EXPOSED_END_CHOICES, ShelfTypeChoices, \
    ShelfPartitionChoices, EXPOSED_END_CHOICES, FACE_COLOR_CHOICES, TOE_KICK_DEPTH_CHOICES,DrawerHole,DrawerDrilSubFront,DrawerhamperTypes
from franchise.models import RoomMatTypeModelMap, RoomEdgeType
from .room_map_models import *
from room_options.models.kd_shelf_models.kd_models import KdInsertBacking, KdEdge
from room_options.models.adj_shelf_models.main_model import AdjExposedEnd, AdjInsertBacking, AdjEdge

class RoomOptionsMasterModel(TimestampedModel):

    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, related_name="job_room_option")
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

    #Adjustable Shelves
    adj_insert_backing = models.ForeignKey(AdjInsertBacking, on_delete=models.CASCADE, related_name="adj_shelf_insert_backing", blank=True, null=True)
    adj_shelf_edge = models.ForeignKey(AdjEdge, on_delete=models.CASCADE, related_name="adj_shelf_edge", blank=True, null=True)
    adj_exposed_end = models.ForeignKey(AdjExposedEnd, on_delete=models.CASCADE, related_name="adj_exposed_end", blank=True, null=True)
    #toe Kick
    end_caps = models.BooleanField(default=False, blank=True, null=True)
    face_color = models.CharField(max_length=20, choices=FACE_COLOR_CHOICES, null=True, blank=True)
    toe_kick_depth = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    plywood = models.BooleanField(default=False, blank=True, null=True)
    #Dwawer Faces
    drawer_faces_holes= models.CharField(max_length=20, choices=DrawerHole.HOLE_CHOICES, null=True, blank=True)
    drawer_faces_drill_Sub_front= models.CharField(max_length=20, choices=DrawerDrilSubFront.DRILL_SUB_FRONT_CHOICES, null=True, blank=True)
    drawer_faces_hamper_type=models.CharField(max_length=20, choices=DrawerhamperTypes.HAMPER_FACES_TYPES, null=True, blank=True)
    drawer_faces_hamper_faces=models.BooleanField(default=False, blank=True, null=True)
    
    def __str__(self):
        return str(self.room)
    
    class Meta:
        db_table = "room_options_master"
        verbose_name = "Room Option Master"
        verbose_name_plural = "Room Options Master"

