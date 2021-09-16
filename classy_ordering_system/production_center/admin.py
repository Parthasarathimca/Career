from django.contrib import admin
from django import forms
from .models import TenentProductionCenterMap
from accounts.models import User
from accounts.conf import UserRole
class CustomTenentProdModelForm(forms.ModelForm):
    class Meta:
        model = TenentProductionCenterMap
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomTenentProdModelForm, self).__init__(*args, **kwargs)
        self.fields['tenent_id'].queryset = User.objects.filter(user_role=UserRole.FRANCHISE)
        self.fields['production_center'].queryset = User.objects.filter(user_role=UserRole.PRODUCTION_CENTER)
        

class TenentProdAdmin(admin.ModelAdmin):
    form = CustomTenentProdModelForm
    filter_horizontal = ('tenent_id', )

admin.site.register(TenentProductionCenterMap,TenentProdAdmin)

