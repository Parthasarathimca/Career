from django.http import request,Http404,HttpResponse,JsonResponse
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
from accounts.forms import ResetPasswordForm, LoginForm, ForgotPasswordRequestForm
from accounts.models import UserSecurityToken,Feedbacks
from COS.core.decorators import anonymous_view
from app.strings import Hash
from COS.core.decorators import logged_user_view
import json

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
        return reverse_lazy('dashboard')

    def get_template_names(self):
        return 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.get_user()
        if form.is_valid:
            try:
                auth_login(self.request, user,backend='django.contrib.auth.backends.ModelBackend')
                response = super(LoginView, self).form_valid(form)
                return response
            except Exception as e:
                pass

@logged_user_view
class DashboardView(TemplateView):
    '''
        Dashboard View
    '''
    template_name = "accounts/dashboard.html"

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
class FeedbackView(RedirectView):
        
   def post(self, *args, **kwargs):
        
        try:
            data=self.request.POST
            data=dict(data)
            data.pop('csrfmiddlewaretoken')  
            results={val :data[val][0] for val in data}
            results['user']=self.request.user
            Feedbacks.objects.create(**results)
        except:
             raise Http404
        return HttpResponse(JsonResponse({'status':201}))
