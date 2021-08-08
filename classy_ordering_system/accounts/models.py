from django.db.models.fields import CharField
from django.utils import timezone
from enum import unique
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import (RegexValidator)
from django.urls import reverse, reverse_lazy
from django.conf import settings
from COS.core.utils import TimestampedModel
from accounts.conf import UserRole
from accounts import messages
from app.strings import Hash
from app.email import Email

# Create your models here.

class UserManager(BaseUserManager):
    '''
    Custom user manager
    '''
    def create_user(self, **kwargs):
        '''
        Create user
        '''
        password = kwargs.pop('password')
        if not kwargs.get('email'):
            raise ValueError('Users must have an email address')
        kwargs['email'] = self.normalize_email(kwargs['email'])
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        '''
        Create superuser
        '''
        user = self.create_user(**kwargs)
        user.is_superuser = user.is_staff =  user.is_verified = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    '''
        User model to keep the records of all type of users
    '''

    name = models.CharField(
        ('Name'), max_length=50, db_index=True,
        validators=[
            RegexValidator(regex=r'^[a-z A-Z]+$', message=messages.NAME_ERROR)])    
    email = models.EmailField('Email Address', unique=True)
    user_role = models.PositiveSmallIntegerField(
        ("User Role"), choices=UserRole.ROLE_CHOICES)
    company_name = models.CharField(('Company Name'), max_length=500, null=True, blank=True)
    company_name2 = models.CharField(('Company Name 2'), max_length=500, null=True, blank=True)
    address = models.TextField(('Address'), max_length=1000, null=True, blank=True)
    suite_number = models.CharField(('Suite Number'), max_length=50, null=True, blank=True)
    city = models.CharField(('City'), max_length=50, null=True, blank=True)
    state = models.CharField(('State'), max_length=50, null=True, blank=True)
    zip_code = models.CharField(('Zip code'), max_length=20, null=True, blank=True)
    phone_number = models.CharField(('Phone Number'), max_length=20, null=True, blank=True)
    fax_number = models.CharField(('Fax Number'), max_length=30, null=True, blank=True)
    license_number = models.CharField(('License Number'), max_length=30, null=True, blank=True)    
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = ['user_role']

    def __str__(self):
        return u'{0} ({1})'.format(self.name, self.email)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-id', )


class UserSecurityToken(TimestampedModel):

    '''
        Model to save the user security tokens
    '''

    FORGOT_PASSWORD = 1
    ACCOUNT_ACTIVATION_TOKEN = 2
    TOKEN_TYPE_CHOICE = (
        (FORGOT_PASSWORD, ('Forgot Password')),
        (ACCOUNT_ACTIVATION_TOKEN, ('Account Activation Token'))
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_token")
    extras = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=150)
    token_type = models.SmallIntegerField(choices=TOKEN_TYPE_CHOICE)
    expire_date = models.DateTimeField()

    def __str__(self):
        if self.user:
            return self.user.email
        return self.extras

    @staticmethod
    def create_token(expiry_date, token_type, user=None, extras=None):
        '''
        Create Token
        '''
        token = Hash.createhashforstring(user.email)
        data = {
            'user': user,
            'extras': extras,
            'token': token,
            'token_type': token_type,
            'expire_date': expiry_date
        }

        return UserSecurityToken.objects.create(**data)

    @staticmethod
    def create_account_activation_token(email, user):

        '''
            Method to create
            account activation
            token after expiring
            any other token if existed
        '''
        UserSecurityToken.objects.filter(user=user,
                                         extras=email,
                                         expire_date__gte=timezone.now(),
                                         token_type=UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN).update(expire_date=timezone.now())
        expire = timezone.now() + timezone.timedelta(**settings.ACCOUNT_VERIFY_TOKEN_EXPIRE_IN)
        token = UserSecurityToken.create_token(
            expire, UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN, user=user, extras=email)
        return token

    @staticmethod
    def create_forgot_password_token(email, user):

        '''
            Method to create
            account activation
            token after expiring
            any other token if existed
        '''
        UserSecurityToken.objects.filter(user=user,
                                         extras=email,
                                         expire_date__gte=timezone.now(),
                                         token_type=UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN).update(
            expire_date=timezone.now())
        expire = timezone.now() + timezone.timedelta(**settings.ACCOUNT_VERIFY_TOKEN_EXPIRE_IN)
        token = UserSecurityToken.create_token(
            expire, UserSecurityToken.FORGOT_PASSWORD, user=user, extras=email)
        return token

    def send_verify_token_email(self, request, email_type="activation"):

        '''  Send verification email 
            which will consist the 
            password resetting link 
        '''

        encrypt_email = (Hash.encrypt_string(self.user.email)).decode('utf-8')
        
        changepassword_path = reverse_lazy('accounts:reset-password', kwargs={
            'token': self.token,
            'id': encrypt_email})

        changepassword_link = '%s://%s/%s' % (request.scheme, request.get_host(),
                                              changepassword_path[1:])

        if email_type == 'activation':
            email_template = 'accounts/email/change_password.html'
            subject = messages.SUBJECT_ACCOUNT_ACTIVATION
        elif email_type == 'password_reset':
            email_template = 'accounts/email/updated-password-confirmation.html'
            subject = messages.PASSWORD_RESET_EMAIL
        else:
            raise ValueError("Token type not implement")

        Email(self.user.email,
            subject
            ).message_from_template(email_template,
                                    {'changepassword_link': changepassword_link},
                                    request
                                    ).send()
        return self


class Feedbacks(TimestampedModel):

    '''
        To track feedback of user
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_feedback')
    page = models.CharField(max_length=255, null=True, blank=True)
    feedback = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.BigIntegerField(null=True,blank=True)


    class Meta:
        db_table="feedbacks"
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbakcs"
