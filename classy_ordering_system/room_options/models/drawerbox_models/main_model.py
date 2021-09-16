from django.db import models
from COS.core.utils import TimestampedModel, SortingModel, SortingManager, IsActiveManager
from franchise.models import RoomModel
from room_options.conf import DRAWER_SIZE_CHOICES, DRAWER_TYPE_CHOICES, SUB_FRONT_CHOICES, DrawerBoxType

'''
Model for Drawer box
'''
class DrawerBox(TimestampedModel,SortingModel):

    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, related_name="room_drawer_boxes")
    height = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=10, null=True, blank=True, choices=DRAWER_SIZE_CHOICES)
    depth = models.DecimalField(decimal_places=3, max_digits=20, blank=True, null=True)
    opening = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    drill_sub_front = models.CharField(max_length=20, choices=SUB_FRONT_CHOICES, null=True, blank=True)
    standard_melamine = models.SmallIntegerField(choices=DrawerBoxType.DRAWER_BOX_TYPE_CHOICES, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return "{}-DrawerBox #{}".format(self.room.room_name, self.id)
    
    class Meta:
        db_table = "drawer_box"
        verbose_name = "Drawer Box"
        verbose_name_plural = "Drawer Boxes"
