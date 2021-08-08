from django.contrib import admin
from accounts.models import User, UserSecurityToken
# Register your models here.

'''
    User model admin to customize the options
'''
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user_role', 'is_active', 'is_verified']

    fieldsets = (
    (None, {'classes': ('wide',),
            'fields': ('name','email','user_role', 'password', 'is_active')}),)
    search_fields = ['name', 'email']
    readonly_fields = ['password']

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)
        self._token = UserSecurityToken.create_account_activation_token(
            obj.email, obj)
        self._token.send_verify_token_email(request)
        return self        

admin.site.register(User, UserAdmin)
admin.site.register(UserSecurityToken)
