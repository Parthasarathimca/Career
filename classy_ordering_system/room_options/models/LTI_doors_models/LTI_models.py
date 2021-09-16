from django.db import models
from COS.core.utils import TimestampedModel,IsActiveManager,SortingModel,SortingManager

class DoorDrawerBaseTypeMapModel(TimestampedModel,SortingModel):
    door_drawer_base_id=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=255 , null=True,blank=True)
    picture = models.ImageField(upload_to='door_drawer_base_types', null=True, blank=True)
    
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)
    
    class Meta:
        db_table = "lti_door_drawer_base_types_map"
        verbose_name = "LTI Doors/Drawers Types"
        verbose_name_plural = "LTI Doors/Drawers Types Map"

class SolidDoorMapModel(TimestampedModel,SortingModel):
    solid_door_id=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=255 , null=True,blank=True)
    picture = models.ImageField(upload_to='solid_door', null=True, blank=True)
    
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)
    
    class Meta:
        db_table = "lti_solid_door_map"
        verbose_name = "LTI Solid Doors Map"
        verbose_name_plural = "LTI Solid Doors Map"
class DoorGlassOptionsMapModel(TimestampedModel,SortingModel):
    glass_options_id=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=255 , null=True,blank=True)
    picture = models.ImageField(upload_to='glass_options', null=True, blank=True)
    
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)+','+str(self.picture)
    
    class Meta:
        db_table = "lti_door_glass_options_map"
        verbose_name = "LTI Door Glass OPtions Map"
        verbose_name_plural = "LTI Door Glass OPtions Map"

class DoorColorsMapModel(TimestampedModel,SortingModel):
    color_id=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=255 , null=True,blank=True)
    picture = models.ImageField(upload_to='door_color', null=True, blank=True)
    
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)
    
    class Meta:
        db_table = "lti_door_colors_map"
        verbose_name = "LTI Door Colors Map"
        verbose_name_plural = "LTI Door Colors Map"

class DoorSizeMapModel(TimestampedModel,SortingModel):
    hole_size = models.DecimalField(('Hole Size'), decimal_places=2, max_digits=20)
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    description=models.CharField(max_length=255 , null=True,blank=True)
    is_standard=models.BooleanField(default=False,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)+','+str(self.height)
    
    class Meta:
        db_table = "lti_door_size_map"
        verbose_name = "LTI Door Size Map"
        verbose_name_plural = "LTI Door Size Map"

class LTIDrawerSizeMapModel(TimestampedModel,SortingModel):
    hole_size = models.DecimalField(('Hole Size'), decimal_places=2, max_digits=20)
    height = models.DecimalField(('Height'), decimal_places=2, max_digits=20)
    description=models.CharField(max_length=255 , null=True,blank=True)
    is_routed=models.BooleanField(default=False,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.description)+','+str(self.height)
    
    class Meta:
        db_table = "lti_drawer_size_map"
        verbose_name = "LTI Drawer Size Map"
        verbose_name_plural = "LTI Drawer Size Map"