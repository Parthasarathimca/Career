from django.db import models
from COS.core.utils import TimestampedModel,IsActiveManager,SortingModel, SortingManager
from franchise.models import RoomModel

# Create your models here.

'''
WOOD DOOR MAP TABLE STARTS HERE
'''

class WoodDoorDrawerStyleMapModel(TimestampedModel, SortingModel):
    style_code = models.BigIntegerField()
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return self.description
    
    class Meta:
        db_table = "wood_door_drawer_style_type_map"
        verbose_name = "Wood Doors/Drawers Types"
        verbose_name_plural = "Wood Doors/Drawers Types Map"

class WoodSpeciesMapModel(TimestampedModel, SortingModel):
    wood_door_drawer_style = models.ForeignKey(WoodDoorDrawerStyleMapModel, on_delete=models.CASCADE, related_name='wood_style', null=True, blank=True)
    code = models.BigIntegerField()
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return self.description
    
    class Meta:
        db_table = "wood_species_style_type_map"
        verbose_name = "Wood Species Map"
        verbose_name_plural = "Wood Species Map"

class WoodDoorColorChoiceMap(TimestampedModel, SortingModel):
    wood_species = models.ForeignKey(WoodSpeciesMapModel, on_delete=models.CASCADE, related_name='wood_style', null=True, blank=True)
    color_code = models.IntegerField(null=True,blank=True)
    color_name = models.CharField(max_length=255 , null=True,blank=True)
    picture = models.ImageField(upload_to='door_color', null=True, blank=True)    
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.color_name)
    
    class Meta:
        db_table = "wood_door_colors_map"
        verbose_name = "Wood Door Colors Map"
        verbose_name_plural = "Wood Door Colors Map"

class WoodDrawerSizeMapModel(TimestampedModel, SortingModel):
    hole_size = models.DecimalField(('Hole Size'), decimal_places=2, max_digits=20)
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    description=models.CharField(max_length=255 , null=True,blank=True)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)
    
    class Meta:
        db_table = "wood_drawer_size_map"
        verbose_name = "Wood Drawer Size Map"
        verbose_name_plural = "Wood Drawer Size Map"


class WoodDoorDrawerSizeMapModel(TimestampedModel,SortingModel):
    hole_size = models.DecimalField(('Hole Size'), decimal_places=2, max_digits=20)
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    description = models.CharField(max_length=255 , null=True,blank=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)
    
    class Meta:
        db_table = "wood_door_drawer_size_map"
        verbose_name = "Wood DDoor rawer Size Map"
        verbose_name_plural = "Wood Door Drawer Size Map"
