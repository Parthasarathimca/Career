from django.contrib import admin
from franchise.models import JobModel, RoomModel, RoomMatTypeModelMap, RoomColorChoiceModelMap, RoomProfileModelMap, RoomEdgeType
# Register your models here.

class ColorAdmin(admin.ModelAdmin):
    filter_horizontal = ('mat_type',)
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False


class RoomModelAdmin(admin.ModelAdmin):
    list_display = ['id', "job_id"]


admin.site.register(JobModel)
admin.site.register(RoomModel, RoomModelAdmin)
admin.site.register(RoomMatTypeModelMap)
admin.site.register(RoomColorChoiceModelMap,ColorAdmin)
admin.site.register(RoomProfileModelMap)
admin.site.register(RoomEdgeType)
