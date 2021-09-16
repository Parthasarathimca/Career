from django.contrib import admin
from franchise.models import JobModel, RoomModel, RoomMatTypeModelMap, RoomColorChoiceModelMap, RoomProfileModelMap, RoomEdgeType, RoomStainColorChoiceModelMap, CategoryCode,ProdMeterialColorMap
from accounts.models import User
from django import forms
from accounts.conf import UserRole



class ColorAdmin(admin.ModelAdmin):
    filter_horizontal = ('color', )
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False


class MatColorAdmin(admin.ModelAdmin):
    filter_horizontal = ('color_stain', )
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False


class RoomModelAdmin(admin.ModelAdmin):
    list_display = ['id', "job_id"]

class CustomProdModelForm(forms.ModelForm):
    class Meta:
        model = ProdMeterialColorMap
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomProdModelForm, self).__init__(*args, **kwargs)
        self.fields['production_center'].queryset = User.objects.filter(user_role=UserRole.PRODUCTION_CENTER)

class ProdMatColorAdmin(admin.ModelAdmin):
    filter_horizontal = ('meterial_type','color' )
    form=CustomProdModelForm

admin.site.register(JobModel)
admin.site.register(RoomModel, RoomModelAdmin)
admin.site.register(RoomMatTypeModelMap,MatColorAdmin)
admin.site.register(RoomColorChoiceModelMap)
admin.site.register(RoomProfileModelMap)
admin.site.register(RoomEdgeType,ColorAdmin)
admin.site.register(RoomStainColorChoiceModelMap)
admin.site.register(CategoryCode)
admin.site.register(ProdMeterialColorMap,ProdMatColorAdmin)