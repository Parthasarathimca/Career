from django.db import models
from COS.core.utils import TimestampedModel
from franchise.models import RoomModel
from room_options.conf import DRAWER_SIZE_CHOICES, DRAWER_TYPE_CHOICES

'''
Model for Drawer box
'''



class DrawerBox(TimestampedModel):

    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, related_name="room_drawer_boxes")
    size_type = models.CharField(max_length=10, choices=DRAWER_TYPE_CHOICES, default="Standard")
    height = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.IntegerField(default=0)
    std_size = models.CharField(max_length=10, null=True, blank=True, choices=DRAWER_SIZE_CHOICES)
    notes = models.TextField()

    def __str__(self):
        return "{}-DrawerBox #{}".format(self.room.room_name, self.id)

    class Meta:
        db_table = "drawer_box"
        verbose_name = "Drawer Box"
        verbose_name_plural = "Drawer Boxes"
