from django.db import models
from COS.core.utils import TimestampedModel,IsActiveManager,SortingModel
from franchise.models import RoomModel

# Create your models here.

'''
KD SHELF MAP TABLE STARTS HERE
'''

class KdDepth(TimestampedModel,SortingModel):
    kd_depth = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    kd_depth_text = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.kd_depth_text)
    
    class Meta:
        db_table = "kd_depth"
        verbose_name = "Kd Depth"
        verbose_name_plural = "Kd Depth"


class KdWidth(TimestampedModel,SortingModel):
    kd_width = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    kd_width_text = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.kd_width_text)
    
    class Meta:
        db_table = "kd_width"
        verbose_name = "Kd Width"
        verbose_name_plural = "Kd Width"


class KdMaterial(TimestampedModel,SortingModel):
    kd_material = models.BigIntegerField()
    kd_material_text = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.kd_material_text)
    
    class Meta:
        db_table = "kd_material"
        verbose_name = "Kd Material"
        verbose_name_plural = "Kd Material"


class KdEdge(TimestampedModel,SortingModel):
    kd_edge = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    kd_edge_text = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.kd_edge_text)
    
    class Meta:
        db_table = "kd_edge"
        verbose_name = "Kd Shelf Edge"
        verbose_name_plural = "Kd Edge"


class KdInsertBacking(TimestampedModel,SortingModel):
    kd_backing_size = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    kd_backing_text = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.kd_backing_text)
    
    class Meta:
        db_table = "kd_shelf_insert_backing"
        verbose_name = "Kd Shelf Insert backing"
        verbose_name_plural = "Kd Shelf Insert backing"



