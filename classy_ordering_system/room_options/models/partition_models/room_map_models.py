from django.db import models
from COS.core.utils import TimestampedModel,IsActiveManager,SortingModel,SortingManager
from franchise.models import RoomModel
from room_options.conf import DepthInches

# Create your models here.

'''
ROOM OPTIONS MAP TABLE STARTS HERE
'''

class RoomDrillModelMap(TimestampedModel,SortingModel):
    drill_code = models.BigIntegerField(('DrillCode'))
    description = models.CharField(max_length=255)
    part_category = models.BigIntegerField(('Part Category'), null=True, blank=True)
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    width = models.DecimalField(('Width'), decimal_places=2, max_digits=20)
    depth = models.DecimalField(('Depth'), decimal_places=2, max_digits=20)
    hole_size = models.DecimalField(('Hole Size'), decimal_places=2, max_digits=20)
    pps_uom = models.DecimalField(('Price Per Sales UOM'), decimal_places=2, max_digits=20)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.height)
    
    class Meta:
        db_table = "room_drill_map"
        verbose_name = "Room Drill Option"
        verbose_name_plural = "Room Drill Options"


class RoomDescriptionMapModel(TimestampedModel,SortingModel):
    desc_id = models.BigIntegerField()
    desc_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return self.desc_text

    class Meta:
        db_table = "room_description_map"
        verbose_name = "Room Description Map"
        verbose_name_plural = "Room Descriptions Map"
'''
ROOM OPTIONS MAP TABLE STARTS HERE
'''

class DoorOpeningSizeMapModel(TimestampedModel,SortingModel):
    opening_size=models.IntegerField()
    text = models.CharField(max_length=255 , null=True,blank=True)
    is_active=models.BooleanField(default=True)
    is_18_hole_doors = models.BooleanField(default=False,null=True,blank=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.text)
    
    class Meta:
        db_table = "door_openings_size"
        verbose_name = "Door Openings size"
        verbose_name_plural = "Door Openings size Map "

class DoorOpeningheightWidthMapModel(TimestampedModel,SortingModel):
    opening_size=models.ForeignKey(DoorOpeningSizeMapModel, on_delete=models.CASCADE, related_name="door_opening_size")
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    width = models.DecimalField(('Width'), decimal_places=2, max_digits=20)
    holes= models.DecimalField(('Holes'), decimal_places=2, max_digits=20)
    depth = models.DecimalField(('Depth'), decimal_places=2, max_digits=20 ,null=True,blank=True)
    is_active=models.BooleanField(default=True) 
    is_18_hole_doors  =models.BooleanField(default=False,null=True,blank=True) 
    objects = IsActiveManager()
    def __str__(self):
        return str(self.height)
    
    class Meta:
        db_table = "door_openings_height_width_map"
        verbose_name = "Door Openings Height & width"
        verbose_name_plural = "Door Openings Height & width Map "

class DoorDrillMapModel(TimestampedModel,SortingModel):
    drill_id=models.IntegerField()
    description=models.CharField(max_length=255 , null=True,blank=True)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)
    
    class Meta:
        db_table = "door_drill_option"
        verbose_name = "Door Dill OPtion"
        verbose_name_plural = "Door Dill OPtions Map"

class DoorSingleOpeningSizeMapModel(TimestampedModel,SortingModel):
    opening_size=models.IntegerField()
    text=models.CharField(max_length=255 , null=True,blank=True)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.text)
    
    class Meta:
        db_table = "door_single_openings_size"
        verbose_name = "Door Single Openings size"
        verbose_name_plural = "Door Single  Openings size Map "

class DoorSingleOpeningheightWidthMapModel(TimestampedModel,SortingModel):
    opening_size=models.ForeignKey(DoorSingleOpeningSizeMapModel, on_delete=models.CASCADE, related_name="door_opening_size")
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    width = models.DecimalField(('Width'), decimal_places=2, max_digits=20)
    depth = models.DecimalField(('Depth'), decimal_places=2, max_digits=20 ,null=True,blank=True)
    is_active=models.BooleanField(default=True)    
    objects = IsActiveManager()
    def __str__(self):
        return str(self.height)
    
    class Meta:
        db_table = "door_single_openings_height_width_map"
        verbose_name = "Door Single Openings Height & width"
        verbose_name_plural = "Door Single Openings Height & width Map "


class DrawerSizeMapModel(TimestampedModel,SortingModel):
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    standard_size = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.standard_size)

    class Meta:
        db_table = "drawer_size_option"
        verbose_name = "Drawer Size OPtion"
        verbose_name_plural = "Drawer Size OPtions "


class GlassTypeMapModel(TimestampedModel,SortingModel):
    glass_type_code=models.BigIntegerField(('GlassTypeCode'),blank=True,null=True)
    glass_type = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.glass_type)

    class Meta:
        db_table = "door_glass_types_map"
        verbose_name = "Door Glass Types Map"
        verbose_name_plural = "Door Glass Types Map"


class CustomPartitionDrillMap(TimestampedModel, SortingModel):

    drillcode = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    category_code = models.CharField(max_length=10, blank=True, null=True)
    category_group = models.CharField(max_length=50, blank=True, null=True)
    part_sub_cat = models.CharField(max_length=50, blank=True, null=True)
    partcat = models.CharField(max_length=100, blank=True, null=True)
    rnd = models.BooleanField(default=False)
    flat = models.BooleanField(default=False)
    std = models.BooleanField(default=False)
    mm22 = models.BooleanField(default=False)
    corner = models.BooleanField(default=False)
    b2b = models.BooleanField(default=False)
    height = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    depth = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    width = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    edge_profile = models.CharField(max_length=100, blank=True, null=True)
    units_of_measure = models.CharField(max_length=100, blank=True, null=True)
    hole_size = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.description)

    class Meta:
        db_table = "cc_pard_drill_map"
        verbose_name = "Custom Partition Drill Map"
        verbose_name_plural = "Custom Partition Drill Maps"
