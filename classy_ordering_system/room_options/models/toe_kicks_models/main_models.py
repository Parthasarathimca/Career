from django.db import models
from COS.core.utils import TimestampedModel, SortingModel, SortingManager, IsActiveManager
from franchise.models import RoomModel
from room_options.conf import FACE_COLOR_CHOICES

'''
Model for Toe Kicks
'''


class ToeKick(TimestampedModel, SortingModel):
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, related_name="room_toe_kicks")
    quantity = models.IntegerField(default=0)
    width = models.DecimalField(decimal_places=2, max_digits=20)
    height = models.DecimalField(decimal_places=2, max_digits=20)
    depth = models.DecimalField(decimal_places=2, max_digits=20)
    end_caps = models.BooleanField(default=False, blank=True, null=True)
    face_color = models.CharField(max_length=20, choices=FACE_COLOR_CHOICES, null=True, blank=True)
    plywood = models.BooleanField(default=False, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return "{}-Toe9Kicks #{}".format(self.room.room_name, self.id)

    class Meta:
        db_table = "toe_kicks"
        verbose_name = "Toe Kick"
        verbose_name_plural = "Toe Kicks"
