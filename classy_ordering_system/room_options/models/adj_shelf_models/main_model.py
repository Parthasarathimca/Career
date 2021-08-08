from django.db import models
from COS.core.utils import TimestampedModel,IsActiveManager
from franchise.models import RoomModel

# Create your models here.

'''
ADJUSTABLE SHELF MAP TABLE STARTS HERE
'''

class AdjDepth(TimestampedModel):
    depth = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    depth_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.depth_text)
    
    class Meta:
        db_table = "adj_depth"
        verbose_name = "Adj Depth"
        verbose_name_plural = "Adj Depth"


class AdjWidth(TimestampedModel):
    width = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    width_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.width_text)
    
    class Meta:
        db_table = "adj_width"
        verbose_name = "Adj Width"
        verbose_name_plural = "Adj Width"


class AdjMaterial(TimestampedModel):
    material = models.BigIntegerField()
    material_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.material_text)
    
    class Meta:
        db_table = "adj_material"
        verbose_name = "Adj Material"
        verbose_name_plural = "Adj Material"


class AdjEdge(TimestampedModel):
    edge = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    edge_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.edge_text)
    
    class Meta:
        db_table = "adj_edge"
        verbose_name = "Adj Shelf Edge"
        verbose_name_plural = "Adj Edge"


class AdjInsertBacking(TimestampedModel):
    backing_size = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    backing_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.backing_text)
    
    class Meta:
        db_table = "adj_shelf_insert_backing"
        verbose_name = "Adj Shelf Insert backing"
        verbose_name_plural = "Adj Shelf Insert backing"


class AdjExposedEnd(TimestampedModel):
    end_code = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    end_code_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()


    def __str__(self):
        return str(self.end_code_text)
    
    class Meta:
        db_table = "adj_exposed_end"
        verbose_name = "Adj Exposed End"
        verbose_name_plural = "Adj Exposed End"