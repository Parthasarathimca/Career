'''
Utility Modules
'''
from django.contrib import admin
from django.db import models
from django.shortcuts import render
from COS.settings import *
import requests
from django.urls import reverse, reverse_lazy



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
        return super(IsActiveManager, self).get_queryset().filter(is_active=True).order_by('sort')

class SortingManager(models.Manager):
    def get_queryset(self):
        return super(SortingManager, self).get_queryset().order_by('sort')


class DisableDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

class SortingModel(models.Model):
    '''
    Sorting Model 
    '''
    sort=models.BigIntegerField(blank=True,null=True)
    class Meta:
        abstract = True



class BearerToken(object):
    def get_bearer_token(self):
        self.API_LOGIN_URL=API_LOGIN_URL
        param={'email':API_EMAIL,'password':API_PASSWORD}
        try:
            login_response= requests.post(self.API_LOGIN_URL,data=param)
            print("API LOGIN: ",login_response)
            if login_response.status_code==200:
                result=login_response.json()
                return result.get("token")
            else:
                return None
        except Exception as e:
            print('API Connection Error',e)
            
class TenentData(BearerToken): 
    def __init__(self) -> None:
        super().__init__()
        
    def get_tenent_data(self):
       # return {'tenants': [{'id': 10, 'name': 'demo', 'created_at': '2021-08-11 16:10:32', 'updated_at': '2021-08-11 16:10:32'}, {'id': 11, 'name': 'Phoenix', 'created_at': '2021-07-29 18:17:45', 'updated_at': '2021-07-29 18:17:45'}, {'id': 12, 'name': 'Prescott', 'created_at': '2021-07-29 18:18:27', 'updated_at': '2021-07-29 18:18:27'}, {'id': 13, 'name': 'Las Vegas', 'created_at': '2021-07-29 18:18:39', 'updated_at': '2021-07-29 18:18:39'}, {'id': 14, 'name': 'San Diego', 'created_at': '2021-07-29 18:18:57', 'updated_at': '2021-07-29 18:18:57'}, {'id': 15, 'name': 'Dallas', 'created_at': '2021-07-29 18:19:02', 'updated_at': '2021-07-29 18:19:02'}, {'id': 16, 'name': 'Salt Lake', 'created_at': '2021-07-29 18:19:13', 'updated_at': '2021-07-29 18:19:13'}, {'id': 17, 'name': 'Denver', 'created_at': '2021-07-29 18:19:21', 'updated_at': '2021-07-29 18:19:21'}, {'id': 18, 'name': 'Tucson', 'created_at': '2021-07-29 18:19:33', 'updated_at': '2021-07-29 18:19:33'}, {'id': 19, 'name': 'Las Cruces', 'created_at': '2021-07-29 18:19:51', 'updated_at': '2021-07-29 18:19:51'}]}
        self.API_TENENT_LIST=API_TENENT_LIST
        token= self.get_bearer_token()
        if token:
            param={'token':token}
            tenent_responce= requests.post(self.API_TENENT_LIST,data=param)
            if tenent_responce:
                return tenent_responce.json()
        return {}        
            
    def get_dropdown_values(self):
        from accounts.models import User
        tenent_data=self.get_tenent_data()
        data={}
        if tenent_data:
            tenent_data=tenent_data.get('tenants')
            all_users=User.objects.exclude(tenent_id__isnull=True)
            existing_user_tenent_id=[i.tenent_id for i in all_users]
            tenent_data=[ i for i in tenent_data if i.get('id') not in existing_user_tenent_id]
            tenent_ids=[(i.get('id'),i.get('id')) for i in tenent_data ] 
            tenent_names=[(i.get('name'),i.get('name')+" ("+ str(i.get('id'))+ " )") for i in tenent_data] 
            tenent_emails=[(i.get('name'),i.get('name')) for i in tenent_data] 
            data={'tenent_ids':tenent_ids,'tenent_names':tenent_names,'tenent_emails':tenent_emails}
        return data

class Projects(BearerToken):


    def get_available_projects(self,tenent_id=None):
        self.API_PROJECT_LIST=API_PROJECT_LIST
        params={}
        token=self.get_bearer_token()
        if token:
            token_vals={'token':token}
            if tenent_id:
                params={'projects.tenantId':tenent_id}
            api_response= requests.post(self.API_PROJECT_LIST,params=params,data=token_vals)
            if api_response:
                return api_response.json()

