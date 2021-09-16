"""classy_ordering_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

from accounts.views import (ResetPasswordView, ResetPasswordSuccessView,
                            LoginView, logoutview, ForgotPasswordRequestView, FeedbackView, TwoFactorAuthView,EmployeeView,EmployeeDeleteView)

urlpatterns = [
    re_path(r'reset_password/(?P<token>.+)/(?P<id>.+)$',
        ResetPasswordView.as_view(), name="reset-password"),

    path('reset_password_success', ResetPasswordSuccessView.as_view(), name="reset-password-success"),
    path('login/', LoginView.as_view(), name='login'),
    path('second-auth/', TwoFactorAuthView.as_view(), name='two-factor'),
    path('logout/', logoutview.as_view(), name='logout'),
    path('forgotpassword/', ForgotPasswordRequestView.as_view(),  name="forgot-password"),
    path('email-confirm/', TemplateView.as_view(template_name="accounts/email-confirm.html"),
         name="sent-forgot-password-email"),
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('employee/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('feedbacks/', FeedbackView.as_view(), name='feedbacks'),
    
]
