from re import VERBOSE
from django.db import models
from accounts.models import User
from COS.core.utils import TimestampedModel

# Create your models here.


'''
    MAPPING TABLES START HERE
'''

class RoomMatTypeModelMap(TimestampedModel):
    mat_code = models.BigIntegerField()
    mat_description = models.TextField(max_length=255)

    def __str__(self):
        return self.mat_description

    class Meta:
        db_table = 'room_material_type_map'
        verbose_name = "Room Material Type Map"
        verbose_name_plural = "Room Material Types Map"

class RoomColorChoiceModelMap(TimestampedModel):
    mat_type=models.ManyToManyField(RoomMatTypeModelMap, related_name='mat_type_color')
    color = models.CharField(max_length=400)
    #color_hex_code = models.CharField(max_length=20,null=True,blank=True)
    flat = models.BooleanField(default=False)
    round = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='color_pics', null=True, blank=True)
    
    def __str__(self):
        return self.color

    class Meta:
        db_table = 'room_colors_choice_map'
        verbose_name = "Room Color Choice Map"
        verbose_name_plural = "Room Color Choices Map"

class RoomProfileModelMap(TimestampedModel):
    profile_code = models.BigIntegerField()
    profile_text = models.CharField(max_length=255)

    def __str__(self):
        return self.profile_text

    class Meta:
        db_table = 'room_profile_map'
        verbose_name = "Room Profile Map"
        verbose_name_plural = "Room Profiles Map"   

class RoomEdgeType(TimestampedModel):
    edge_type_code = models.BigIntegerField()
    edge_type_text = models.CharField(max_length=255)

    def __str__(self):
        return self.edge_type_text

    class Meta:
        db_table = 'room_edge_type_map'
        verbose_name = "Room Edge Type Map"
        verbose_name_plural = "Room Edge Types Map"   
'''
    MAPPING TABLES END HERE
'''

class JobModel(TimestampedModel):
    STATUS_CHOICES = (
        ('SENT', 'Orders Sent'),
        ('INPROGRESS', 'Orders Inprogress'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_job')
    job_id = models.BigIntegerField(unique=True)
    job_description = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.job_id)
    
    class Meta:
        db_table = "job"
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

class RoomModel(TimestampedModel):
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name="job_room")
    room_name = models.CharField(max_length=255)
    room_key = models.CharField(max_length=255, null=True, blank=True)
    mat_type = models.ForeignKey(RoomMatTypeModelMap, on_delete=models.CASCADE, related_name="room_mat_type")
    bd_color = models.ForeignKey(RoomColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_bd_color")
    ed_color = models.ForeignKey(RoomColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_ed_color")
    ed_type = models.ForeignKey(RoomEdgeType, on_delete=models.CASCADE, related_name="room_ed_type")
    ed_profile = models.ForeignKey(RoomProfileModelMap, on_delete=models.CASCADE, related_name="room_ed_profile")
    
    dd_color = models.ForeignKey(RoomColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_dd_color",null=True,blank=True)
    dd_mat_type = models.ForeignKey(RoomMatTypeModelMap, on_delete=models.CASCADE, related_name="room_dd_mat_type",null=True,blank=True)
    dd_ed_type = models.ForeignKey(RoomEdgeType, on_delete=models.CASCADE, related_name="room_dd_ed_type",null=True,blank=True)
    dd_ed_profile = models.ForeignKey(RoomProfileModelMap, on_delete=models.CASCADE, related_name="room_dd_ed_profile",null=True,blank=True)
    dd_ed_color = models.ForeignKey(RoomColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_dd_ed_color",null=True,blank=True)

    def __str__(self):
        return self.room_name

    class Meta:
        db_table = "room"
        verbose_name = "Room"
        verbose_name_plural = "Rooms"