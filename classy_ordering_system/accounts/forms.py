from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts import messages
from accounts.models import User, UserSecurityToken
from app.validators import validate_password


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
        'not_verified' :messages.USER_ACCOUNT_NOT_VERIFIED
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
                user = user_model._default_manager.get(email__iexact=email)
                if user.check_password(password):
                    self.user_cache = user
                if user.is_superuser or user.is_staff:
                    self.user_cache = None
            except user_model.DoesNotExist:
                self.user_cache = None
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