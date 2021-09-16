from re import T, VERBOSE
from django.db import models
from accounts.models import User
from COS.core.utils import TimestampedModel,SortingModel,SortingManager
from jobline.models import Joblineimport
from  .conf import *
from datetime import datetime    


# Create your models here.


'''
    MAPPING TABLES START HERE
'''


class RoomColorChoiceModelMap(TimestampedModel,SortingModel):
    #mat_type=models.ManyToManyField(RoomMatTypeModelMap, related_name='mat_type_color')
    color = models.CharField(max_length=400)
    color_code = models.BigIntegerField(null=True, blank=True)
    flat = models.BooleanField(default=False)
    round = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='color_pics', null=True, blank=True)
    objects=SortingManager()
    
    def __str__(self):
        return self.color

    class Meta:
        db_table = 'room_colors_choice_map'
        verbose_name = "Room Color Choice Map"
        verbose_name_plural = "Room Color Choices Map"


class RoomStainColorChoiceModelMap(TimestampedModel, SortingModel):
    color = models.CharField(max_length=400)
    color_code = models.BigIntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to='stain_pics', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = SortingModel()

    def __str__(self):
        return self.color

    class Meta:
        db_table = "room_stain_colors_choice_map"
        verbose_name = "Room Stain Color Map"
        verbose_name_plural = "Room Stain Color Choices Map"


class RoomMatTypeModelMap(TimestampedModel,SortingModel):
    # production_center = models.ForeignKey(User,unique=True, related_name='production_center_mat_type', on_delete=models.CASCADE, null=True, blank=True)
    # color=models.ManyToManyField(RoomColorChoiceModelMap, related_name='mat_type_color')
    color_stain = models.ManyToManyField(RoomStainColorChoiceModelMap, related_name='mat_type_stain_color', null=True, blank=True)
    mat_code = models.BigIntegerField()
    mat_description = models.TextField(max_length=255)  
    size = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    objects=SortingManager()
    def __str__(self):
        return self.mat_description

    class Meta:
        db_table = 'room_material_type_map'
        verbose_name = "Room Material Type Map"
        verbose_name_plural = "Room Material Types Map"


class RoomProfileModelMap(TimestampedModel,SortingModel):
    profile_code = models.BigIntegerField()
    profile_text = models.CharField(max_length=255)
    objects=SortingManager()
    def __str__(self):
        return self.profile_text

    class Meta:
        db_table = 'room_profile_map'
        verbose_name = "Room Profile Map"
        verbose_name_plural = "Room Profiles Map"   

class RoomEdgeType(TimestampedModel,SortingModel):
    color=models.ManyToManyField(RoomColorChoiceModelMap, related_name='edge_type_color')
    edge_type_code = models.BigIntegerField()
    edge_type_text = models.CharField(max_length=255)
    objects=SortingManager()
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_job')
    job_id = models.BigIntegerField(unique=True)
    job_description = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.BigIntegerField()
    client_name=models.CharField(max_length=255, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=orderStatus.STATUS_CHOICES, default='INPROGRESS')
    email = models.EmailField('Email Address',null=True,blank=True)
    job_install_start_date=models.DateTimeField(('install_start_date'), blank=True,null=True)
    job_install_end_date=models.DateTimeField(('install_end_date'), blank=True,null=True)
    job_updated_at=models.DateTimeField(('job_updated_at'), blank=True,null=True)
    designer=models.CharField(max_length=255, null=True, blank=True)
    is_project_admin= models.BooleanField(default=False,null=True,blank=True)
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
    mat_color_stain = models.ForeignKey(RoomStainColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_mat_color_stain", null=True, blank=True)
    
    job_created_at=models.DateTimeField(('Create at'), blank=True,null=True)
    dd_color = models.ForeignKey(RoomColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_dd_color",null=True,blank=True)
    dd_mat_type = models.ForeignKey(RoomMatTypeModelMap, on_delete=models.CASCADE, related_name="room_dd_mat_type",null=True,blank=True)
    dd_ed_type = models.ForeignKey(RoomEdgeType, on_delete=models.CASCADE, related_name="room_dd_ed_type",null=True,blank=True)
    dd_ed_profile = models.ForeignKey(RoomProfileModelMap, on_delete=models.CASCADE, related_name="room_dd_ed_profile",null=True,blank=True)
    dd_ed_color = models.ForeignKey(RoomColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_dd_ed_color",null=True,blank=True)
    dd_mat_color_stain = models.ForeignKey(RoomStainColorChoiceModelMap, on_delete=models.CASCADE, related_name="room_dd_mat_stain", null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=orderStatus.STATUS_CHOICES, default='INPROGRESS')

    def __str__(self):
        return self.room_name

    @property
    def joblines(self):
        return Joblineimport.objects.filter(roomid=self.id)

    class Meta:
        db_table = "room"
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

class ProductionCenter(TimestampedModel):
    production_center_name = models.CharField(max_length=255,null=True,blank=True)
    

    
    def __str__(self):
        return self.production_center_name

    class Meta:
        db_table = 'production_center'
        verbose_name = "Production Center"
        verbose_name_plural = "Production Centers"   

class JobStatus(TimestampedModel):
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name="job_status")
    job_status_id=models.IntegerField(blank=True,null=True)
    production_center=models.ForeignKey(User,on_delete=models.CASCADE,related_name='job_production_center',null=True,blank=True)
    order_send_time=models.DateTimeField(default=datetime.now(),blank=True,null=True)
    production_status = models.CharField(max_length=100,null=True,blank=True)

    
    # def __str__(self):
    #     return self.job

    class Meta:
        db_table = 'job_status_master'
        verbose_name = "Job Status"
        verbose_name_plural = "Jab Status"   

class CategoryCode(TimestampedModel, SortingModel):
    category_code = models.BigIntegerField(null=True, blank=True)
    category_description = models.CharField(max_length=255, null=True, blank=True)
    H1 = models.CharField(max_length=255, null=True, blank=True)
    W1 = models.CharField(max_length=255, null=True, blank=True)
    D1 = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    objects = SortingManager()

    def __str__(self):
        return self.category_code

    class Meta:
        db_table = "category_code_map"
        verbose_name = "Category Code Map"
        verbose_name_plural = "Category Codes Map"

class ProdMeterialColorMap(TimestampedModel,SortingModel):
    production_center=models.ForeignKey(User, on_delete=models.CASCADE, related_name="prod_mat_color_map",null=True,blank=True)
    meterial_type=models.ManyToManyField(RoomMatTypeModelMap,  related_name="prod_mat_type",null=True,blank=True)
    color=models.ManyToManyField(RoomColorChoiceModelMap,related_name="prod_color",null=True,blank=True)
    objects=SortingManager()
    def __str__(self):
        meterial_type = ", ".join(str(seg) for seg in self.meterial_type.all())
        return f"{self.production_center.name},{ meterial_type}"
 
    class Meta:
        db_table = 'prod_meterial_color_map'
        verbose_name = "Production center Meterial Color Map"
        verbose_name_plural = "Production center Meterial Color Map"   

