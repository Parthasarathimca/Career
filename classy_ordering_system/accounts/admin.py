from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from accounts.models import Feedbacks, User, UserSecurityToken
from django.conf import settings
from accounts.forms import CustomUserCreation
from COS.core.utils import DisableDeleteAdmin



# Register your models here.

'''
    User model admin to customize the options
'''
class UserAdmin(admin.ModelAdmin):
    
    add_form = CustomUserCreation
    list_display = ['tenent_id','name', 'email', 'user_role', 'is_active', 'is_verified','is_employee','two_factor_auth']

    fieldsets = (
    (None, {'classes': ('wide',),
            'fields': ('user_role','tenent_id','name','email','phone_number',  'is_active', 'two_factor_auth'),}),)
    search_fields = ['name', 'email']
    readonly_fields = ['password']

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)

        if not change:
            self._token = UserSecurityToken.create_account_activation_token(
                obj.email, obj)
            self._token.send_verify_token_email(request)
        return self      
    
    def get_form(self, request, obj=None, **kwargs):    
        """ 
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        data=super().get_form(request, obj, **defaults)
        data.request=request
        return data
     
    
admin.site.register(User, UserAdmin)
admin.site.register(UserSecurityToken)
admin.site.register(Feedbacks, DisableDeleteAdmin)
