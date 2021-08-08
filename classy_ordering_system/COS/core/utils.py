'''
Utility Modules
'''
from django.contrib import admin
from django.db import models


class TimestampedModel(models.Model):
    '''
    Timestamped Model 
    '''
    create_date = models.DateTimeField(('Create Date'), auto_now_add=True)
    modify_date = models.DateTimeField(('Modify Date'), auto_now=True)

    class Meta:
        abstract = True

class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super(IsActiveManager, self).get_queryset().filter(is_active=True)


class DisableDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False
