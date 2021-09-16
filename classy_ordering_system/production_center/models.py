from accounts.models import User
from django.db import models
from COS.core.utils import TimestampedModel,SortingModel,SortingManager
from accounts.conf import UserRole
class TenentProductionCenterMap(TimestampedModel,SortingModel):
    
    tenent_id=models.ManyToManyField(User, related_name='tenet_production_center', null=True, blank=True)
    production_center = models.ForeignKey(User, related_name='production_center_tenent', on_delete=models.CASCADE, null=True, blank=True)
    objects=SortingManager()
    def __str__(self):
        return self.production_center.name

    class Meta:
        db_table = 'tenent_production_center_map'
        verbose_name = "Tenent Production Center Map"
        verbose_name_plural = "Tenent Production Center Map"