from datetime import datetime, timedelta
from random import randint

from django.core.serializers.json import DjangoJSONEncoder
from django.http import request,Http404,HttpResponse,JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth import logout
from franchise.models import JobModel, RoomModel
from accounts.forms import ResetPasswordForm, LoginForm, ForgotPasswordRequestForm, TwoFactorForm,EmployeeCreateForm
from accounts.models import User, UserSecurityToken,Feedbacks
from COS.core.decorators import anonymous_view, is_classy_user, is_classy_user_view
from app.strings import Hash
from app.email import Email
from COS.core.decorators import logged_user_view,can_accounts_view
import json
from accounts.conf import UserRole
import os
from twilio.rest import Client


class ResetPasswordView(FormView):

    '''
        View to handle the password reset
    '''

    form_class = ResetPasswordForm
    template_name = "accounts/reset_password.html"

    def get_success_url(self):
        '''get succcess url '''
        return reverse('accounts:reset-password-success')

    def get(self, request, *args, **kwargs):
        '''get request'''
        valid_link= self._is_valid_link(*args)
        if valid_link == 'expired':
            self.template_name = 'accounts/reset_password_link_expired.html'
            return render(request, self.template_name)
        return super(ResetPasswordView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        '''update form args '''
        data = super(ResetPasswordView, self).get_form_kwargs()
        self.valid_token = self._is_valid_link()
        data.update({'request': self.request,
                     'token': self.valid_token
                     })
        return data


    def _is_valid_link(self):
        '''check if change password link is valid '''
        email = Hash.decrypt_string(self.kwargs['id'].encode('utf-8'))
        email = email.decode('utf-8')
        valid_token = None

        try:
            user = get_user_model().objects.filter(email__iexact=email).get()
            try:
                user_token = UserSecurityToken.objects.filter(token=self.kwargs['token'],
                                                              extras=email,
                                                              token_type=UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN).get()
                if user_token.expire_date > timezone.now():
                    valid_token = user_token
                else:
                    valid_token = 'expired'

            except UserSecurityToken.DoesNotExist:
                valid_token = 'invalid'
        except get_user_model().DoesNotExist:
            valid_token = 'invalid'
        return valid_token

    def form_valid(self, form):
        ''' form valid '''
        form.save()
        return super(ResetPasswordView, self).form_valid(form)

class ResetPasswordSuccessView(TemplateView):
    '''
       Success template after resetting the password 
    '''    
    template_name = "accounts/reset_password_success.html"


@anonymous_view()
class LoginView(FormView):
    '''Login view '''

    form_class = LoginForm

    def get_success_url(self):
        if self.request.session.get('two_factor_auth') == None:
            return reverse_lazy('dashboard')
        else:     
            return reverse_lazy('accounts:two-factor') 



    def get_template_names(self):
        # if self.request.path == '/classy/classy_admin/login/':
        #     return 'admin/login.html'
        # else:
        return 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
       
        return context

    def form_valid(self, form):
        user = form.get_user()
        token = randint(10000, 99999)
        print(token)
        if user.two_factor_auth:
            try:
                account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                client = Client(account_sid, auth_token)
                if user.phone_number:
                    message = client.messages.create(
                            messaging_service_sid=os.environ.get('SERVICE_ID'), 
                            body=f'Your Classy web app verification code is {token}',
                            to = user.phone_number,
                            from_=os.environ.get('FROM')
                        )

                    two_factor_sms = json.dumps({
                        'token': token,
                        'user_id': user.id,
                        'expires': datetime.now() + timedelta(seconds=20 * 60)
                    }, cls=DjangoJSONEncoder)
                    self.request.session['two_factor_sms'] = two_factor_sms
            except Exception as e:
                pass

            two_factor_auth = json.dumps({
                'token': token,
                'user_id': user.id,
                'expires': datetime.now() + timedelta(seconds=20 * 60)
            }, cls=DjangoJSONEncoder)
            self.request.session['two_factor_auth'] = two_factor_auth
            Email(user.email,
                "2-Factor Authentication OTP"
                ).message_from_template('accounts/email/two_factor_otp.html',
                                        {'token': token},
                                        self.request
                                        ).send()
        else:
            try:
                user_model = get_user_model()
                auth_user = user_model.objects.get(pk=user.id)
                auth_login(self.request, auth_user, backend='django.contrib.auth.backends.ModelBackend')
            except Exception as e:
                raise str(e)
        return super(LoginView, self).form_valid(form)


@anonymous_view()
class TwoFactorAuthView(FormView):
    form_class = TwoFactorForm
    template_name = "accounts/two_factor.html"

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')
        elif self.request.user.user_role == UserRole.PRODUCTION_CENTER:  
            return reverse_lazy('production_center:production-dashboard')
        else:
            return reverse_lazy('dashboard')

    def get_form_kwargs(self):
        data = super(TwoFactorAuthView, self).get_form_kwargs()
        data.update({'request': self.request})
        return data

    def form_valid(self, form):
        return super(TwoFactorAuthView, self).form_valid(form)


@logged_user_view
@is_classy_user_view
class DashboardView(TemplateView):
    '''
        Dashboard View
    '''
    template_name =  "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['active_jobs'] = JobModel.objects.filter(user=self.request.user)
        context['all_rooms'] = RoomModel.objects.filter(job__user=self.request.user)
        return context    

class logoutview(RedirectView):
    
    '''
        Terminate the user session
    '''
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        redirect_url = reverse_lazy('dashboard')
        return redirect_url


@anonymous_view(redirect_to='/accounts/dashboard')
class ForgotPasswordRequestView(FormView):
    ''' 
    ForgotPassword Request View 
    '''
    form_class = ForgotPasswordRequestForm
    template_name = 'accounts/forgot_password.html'

    def get(self, request, *args, **kwargs):
        '''
        get request
        '''
        auth_logout(request)
        return super(ForgotPasswordRequestView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        ''' get form kwargs '''
        data = super(ForgotPasswordRequestView, self).get_form_kwargs()
        data.update({'request': self.request})
        return data

    def form_valid(self, form):
        '''form valid'''
        _ = self.__class__
        form.save() 
        return redirect(reverse('accounts:sent-forgot-password-email'))

@logged_user_view()
@can_accounts_view()
class EmployeeView(FormView):
    ''' 
     Add Employee Request View 
    '''
    form_class = EmployeeCreateForm
    template_name = 'accounts/employee.html'
    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        if  self.request.user.user_role==UserRole.EMPLOYEE:
            return context

        context['user_role'] =UserRole.EMPLOYEE
        context['users']=User.objects.filter(tenent_id=self.request.user.tenent_id).exclude(is_employee=0)
        if self.request.GET.get('user_item'):
            self.user_item_id=self.request.GET.get('user_item')
            context['user_item']=User.objects.get(id=self.user_item_id)
        return context

    def get(self, request, *args, **kwargs):
        '''
        get request
        '''      
        return super(EmployeeView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        ''' get form kwargs '''
        data = super(EmployeeView, self).get_form_kwargs()
        data.update({'request': self.request})
        return data

    def form_valid(self, form):
        '''form valid'''
        _ = self.__class__
        form.save() 
        return redirect(reverse('accounts:employee'))
    def form_invalid(self, form):
        print("Error",form.errors)
        return super().form_invalid(form)

@logged_user_view()
class EmployeeDeleteView(RedirectView):

    def get(self, *args, **kwargs):
        self.pk=self.request.GET.get('pk')
        User.objects.get(id=self.pk).delete()
        return HttpResponse(JsonResponse({'status': 204}))



@logged_user_view()
class FeedbackView(RedirectView):

   def post(self, *args, **kwargs):

        try:
            data=self.request.POST
            data=dict(data)
            data.pop('csrfmiddlewaretoken')  
            results={val :data[val][0] for val in data}
            results['user']=self.request.user
            results['email'] = self.request.user.email
            results['username'] = self.request.user.name
            Feedbacks.objects.create(**results)
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':201}))



