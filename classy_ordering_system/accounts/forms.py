import json

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.utils import timezone
from accounts import messages
from accounts import models
from accounts.models import User, UserSecurityToken
from app.validators import validate_password
from datetime import datetime
from django.contrib.auth.forms import UserChangeForm
from COS.core.utils import TenentData
from accounts.conf import UserRole

class ResetPasswordForm(forms.Form):
    '''
    Reset password form
    '''
    error_messages = {'password_mismatch': messages.PASSWORD_MISMATCH_FIELDS}

    password = forms.CharField(
        label=('Password'),
        validators=[
            validate_password,
        ])

    confirm_password = forms.CharField(
        label=('Confirm Password'),
        )

    class Meta(object):
        model = get_user_model()
        fields = ('password', 'confirm_password')

    def __init__(self, request=None, token=None, *args, **kwargs):
        self._token_cache = token
        self.request = request
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        Validate Password
        '''
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return self.cleaned_data

    def save(self):
        '''
        Saves the current instance by controlling the saving process.
        '''
        if not isinstance(self._token_cache, str):
            self._token_cache.user.set_password(self.cleaned_data['password'])
            self._token_cache.expire_date = timezone.now()
            self._token_cache.user.is_verified = True
            self._token_cache.user.is_active = True
            self._token_cache.user.save()
            self._token_cache.expire_date = timezone.now()
            self._token_cache.user.save()
            self._token_cache.save()

        return self

class TwoFactorForm(forms.Form):
    request = None
    token = forms.CharField(label="Email OTP")

    error_messages = {
        'token_not_found': messages.USER_TOKEN_NOT_FOUND,
        'expire': messages.USER_TOKEN_EXPIRE,
        'not_verified': messages.USER_TOKEN_NOT_VERIFIED
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TwoFactorForm, self).__init__(*args, **kwargs)

    def clean(self):
        auth2_string = self.request.session.get('two_factor_auth', None)
        auth_sms = self.request.session.get('two_factor_sms', None)
        if auth2_string is None:
            raise forms.ValidationError(self.error_messages['not_verified'])
        auth2 = json.loads(auth2_string)
        if auth_sms:
            auth_sms2 = json.loads(auth_sms)
        expires = datetime.fromisoformat(auth2['expires'])
        if datetime.now() > expires:
            raise forms.ValidationError("token is expired")
        if self.cleaned_data['token'] == str(auth2['token'] or str(auth_sms2['token'])):
            user_model = get_user_model()
            user = user_model.objects.get(pk=auth2['user_id'])
            try:
                auth_login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            except Exception as e:
                raise forms.ValidationError("Error in Logging in")
            del self.request.session['two_factor_auth']
        else:
            raise forms.ValidationError(self.error_messages['not_verified'])


class LoginForm(forms.ModelForm):

    '''
        Login Form
    '''
    email = forms.EmailField(label=("Email"),
                             required=True,
                             error_messages={
                                 'required': messages.FIELD_REQUIRED,
                                 'invalid': messages.USER_INVALID_EMAIL_ADDRESS})    

    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput,
        error_messages={'required': messages.FIELD_REQUIRED})

        
    error_messages = {
        'invalid_login': messages.USER_INVALID_EMAIL_PASSWORD,
        'inactive': messages.USER_ACCOUNT_NOT_ACTIVE,
        'not_verified' :messages.USER_ACCOUNT_NOT_VERIFIED,
        'unauthorized': messages.UNAUTHORIZED
    }

    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, request=None, *args, **kwargs):
        '''
        Initializes form with request and user_cache objects
        '''
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        user_model = get_user_model()
        self.username_field = user_model._meta.get_field(
            user_model.USERNAME_FIELD)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user_model = get_user_model()
            try:
                # url = self.data.get('current_url')
                user = user_model._default_manager.get(email__iexact=email)
                if user.check_password(password):
                    self.user_cache = user
                # if url == None:
                if user.is_superuser or user.is_staff:
                    self.user_cache = None
                    print("user not logged in")
            except user_model.DoesNotExist:
                self.user_cache = None
            # if url != None and url == '/classy/classy_admin/login/':

            #     if user.is_superuser == False:
            #         raise forms.ValidationError(
            #         self.error_messages['unauthorized'],
            #         code='unauthorized',
            #         params={'email': self.username_field.verbose_name},
            #     )
            
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_verified:
                raise forms.ValidationError(
                    self.error_messages['not_verified'],
                    code="not_active")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data 

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

class ForgotPasswordRequestForm(forms.Form):
    '''
    Forgot password form
    '''
    email = forms.EmailField(
        label=("Email"),
        required=True,
        error_messages={
            'required': messages.FIELD_REQUIRED,
            'invalid': messages.FORGOT_PASSWORD_INVALID_EMAIL
        })

    def __init__(self, request=None, *args, **kwargs):
        self._token = None
        self._user_cache = None
        self.request = request

        super(ForgotPasswordRequestForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        '''
        Validate Email
        '''
        user_model = get_user_model()
        try:
            self._user_cache = user_model.objects.get(
                email__iexact=self.cleaned_data['email'])
            if not self._user_cache.is_active:
                raise forms.ValidationError(messages.USER_ACCOUNT_NOT_ACTIVE)
        except user_model.DoesNotExist:
            raise forms.ValidationError('User with {} email does not exists'.format(self.cleaned_data['email']))
        return self.cleaned_data['email']

    def save(self):
        '''
        Saves the current instance by controlling the saving process.
        '''
        self._token = UserSecurityToken.create_forgot_password_token(self.cleaned_data['email'], self._user_cache)
        self._token.send_verify_token_email(self.request, "password_reset")
        return self

    def get_encoded_token(self):
        return self._token.encoded_token

class CustomUserCreation(UserChangeForm):
      def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        tenen=TenentData()
        tenent_data=tenen.get_dropdown_values()
        #tenent_data={'tenent_names':(('Tezt','Test',),),'tenent_ids':((1,1,),)}
        if self._meta.model.USERNAME_FIELD in self.fields and self.request.method  != 'POST':
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True
            self.fields['name']=forms.ChoiceField(choices=tenent_data.get("tenent_names"))
            #self.fields['email'] = forms.ChoiceField(choices=tenent_data.get("tenent_emails"))
            self.fields['tenent_id'] = forms.ChoiceField(choices=tenent_data.get("tenent_ids"))
       
        if self.request.method == 'POST' :
            if self.data.get('user_role')== UserRole.PRODUCTION_CENTER:
                self.fields['name'] = forms.CharField() 

  
class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['tenent_id','employee_id', 'name','email','phone_number','user_role','is_active','is_employee']

    def __init__(self, request=None, user=None, image_path=None, *args, **kwargs):
        self.request = request
        from room_options.conf import PARTTION_HEIGHT_CHOICES   
        super(EmployeeCreateForm, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        email_id=self.cleaned_data.get('email')
        if User.objects.filter(email=email_id).count():
            raise forms.ValidationError('Email already exist !')
        return email_id

    def save(self):
        pk=self.request.GET.get('user_item')
        if pk:
            user= User.objects.filter(id=pk).update(**self.cleaned_data)
        else:
            user = User.objects.create( **self.cleaned_data)
            self._token = UserSecurityToken.create_account_activation_token(
                user.email, user)
            self._token.send_verify_token_email(self.request)
        return user
        

    def clean(self):
        self.cleaned_data['tenent_id']=self.request.user.tenent_id if self.request.user else None
        self.cleaned_data['is_employee']=True
        return self.cleaned_data

 