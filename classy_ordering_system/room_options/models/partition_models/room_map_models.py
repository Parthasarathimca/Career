from django.db import models
from COS.core.utils import TimestampedModel,IsActiveManager
from franchise.models import RoomModel
from room_options.conf import DepthInches

# Create your models here.

'''
ROOM OPTIONS MAP TABLE STARTS HERE
'''

class RoomDrillModelMap(TimestampedModel):
    drill_code = models.BigIntegerField(('DrillCode'))
    description = models.CharField(max_length=255)
    part_category = models.BigIntegerField(('Part Category'), null=True, blank=True)
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    width = models.DecimalField(('Width'), decimal_places=2, max_digits=20)
    depth = models.DecimalField(('Depth'), decimal_places=2, max_digits=20)
    hole_size = models.DecimalField(('Hole Size'), decimal_places=2, max_digits=20)
    pps_uom = models.DecimalField(('Price Per Sales UOM'), decimal_places=2, max_digits=20)

    def __str__(self):
        return str(self.height)
    
    class Meta:
        db_table = "room_drill_map"
        verbose_name = "Room Drill Option"
        verbose_name_plural = "Room Drill Options"


class RoomDescriptionMapModel(TimestampedModel):
    desc_id = models.BigIntegerField()
    desc_text = models.CharField(max_length=255)

    def __str__(self):
        return self.desc_text

    class Meta:
        db_table = "room_description_map"
        verbose_name = "Room Description Map"
        verbose_name_plural = "Room Descriptions Map"
'''
ROOM OPTIONS MAP TABLE STARTS HERE
'''

class DoorOpeningSizeMapModel(TimestampedModel):
    opening_size=models.IntegerField()
    text=models.CharField(max_length=255 , null=True,blank=True)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.text)
    
    class Meta:
        db_table = "door_openings_size"
        verbose_name = "Door Openings size"
        verbose_name_plural = "Door Openings size Map "

class DoorOpeningheightWidthMapModel(TimestampedModel):
    opening_size=models.ForeignKey(DoorOpeningSizeMapModel, on_delete=models.CASCADE, related_name="door_opening_size")
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    width = models.DecimalField(('Width'), decimal_places=2, max_digits=20)
    holes= models.DecimalField(('Holes'), decimal_places=2, max_digits=20)
    depth = models.DecimalField(('Depth'), decimal_places=2, max_digits=20 ,null=True,blank=True)
    is_active=models.BooleanField(default=True)    
    objects = IsActiveManager()
    def __str__(self):
        return str(self.height)
    
    class Meta:
        db_table = "door_openings_height_width_map"
        verbose_name = "Door Openings Height & width"
        verbose_name_plural = "Door Openings Height & width Map "

class DoorDrillMapModel(TimestampedModel):
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

class DoorSingleOpeningSizeMapModel(TimestampedModel):
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

class DoorSingleOpeningheightWidthMapModel(TimestampedModel):
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


class DrawerSizeMapModel(TimestampedModel):
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    standard_size = models.CharField(max_length=3)

    def __str__(self):
        return str(self.standard_size)

    class Meta:
        db_table = "drawer_size_option"
        verbose_name = "Drawer Size OPtion"
        verbose_name_plural = "Drawer Size OPtions "