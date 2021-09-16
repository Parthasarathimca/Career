''' Decorators '''
from franchise.models import ProductionCenter
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.urls import reverse
from  accounts.conf import UserRole

def anonymous_only(redirect_to=None):
    ''' 
    Anonymous Decorator Function 
    '''

    def decorator(view_func):
        ''' Decorator '''
        def wrapper(request, *args, **kwargs):
            ''' Wrapper '''
            redirect_url = kwargs.get('redirect_to', reverse_lazy('dashboard'))
            if not request.user.is_anonymous and request.method == 'GET':
                redirect_to = redirect(redirect_url)
            else:
                redirect_to = view_func(request, *args, **kwargs)
            return redirect_to
        return wrapper
    return decorator

def anonymous_view(cls=None, **function_args):
    ''' 
    Anonymous View Dispatch
    '''
    if cls is not None:
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)
        original = cls.dispatch
        modified = method_decorator(
            anonymous_only(**function_args))(original)
        cls.dispatch = modified
        return cls
    else:
        def inner_decorator(inner_cls):
            ''' Inner Decorator '''
            return anonymous_view(inner_cls, **function_args)
        return inner_decorator

def check_user_response(request, next_url, redirect_to):
    '''
    Decorator
    Check User Response
    '''
    response = None
    if request.user.is_anonymous:
        redirect_url = redirect_to if redirect_to else reverse('accounts:login')
        redirect_url = '%s?redirect_to=%s' % (
            redirect_url, next_url) if next_url else redirect_url
        response = JsonResponse(data={'login': True, 'next': redirect_url}) if request.is_ajax() else redirect(
            redirect_url)
    return response

def logged_only(redirect_to=None, next_url=None):
    ''' Logged User View Only
    if request is not from logged in user it redirect
    to the url provided in redirect_to parameters'''

    def decorator(view_func):
        ''' Decorator '''
        def wrapper(request, *args, **kwargs):
            ''' Wrapper '''
            response = check_user_response(request, next_url, redirect_to)
            if not response:
                response = view_func(request, *args, **kwargs)
            return response
        return wrapper

    return decorator

def logged_user_view(cls=None, **function_args):
    '''
    Logged User View
    '''
    if cls is not None:
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)

        original = cls.dispatch
        modified = method_decorator(
            logged_only(**function_args))(original)
        cls.dispatch = modified


        return cls
    else:
        def inner_decorator(inner_cls):
            '''
            Inner Decorators
            '''
            return logged_user_view(inner_cls, **function_args)

        return inner_decorator

def can_access_account():
    ''' 
    Check access for accounts view 
    '''
    def decorator(view_func):
        ''' Decorator '''
        def wrapper(request, *args, **kwargs):
            redirect_url = kwargs.get('redirect_to', reverse_lazy('dashboard'))
            if  request.user.is_employee :  
                redirect_to = redirect(redirect_url)
            else:
                redirect_to = view_func(request, *args, **kwargs)
            return redirect_to
        return wrapper  
    return decorator

def can_accounts_view(cls=None, **function_args):
    ''' 
    can_access_account  View Dispatch
    '''
    if cls is not None:
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)
        original = cls.dispatch
        modified = method_decorator(
            can_access_account(**function_args))(original)
        cls.dispatch = modified
        return cls
    else:
        def inner_decorator(inner_cls):
            ''' Inner Decorator '''
            return can_accounts_view(inner_cls, **function_args)
        return inner_decorator


# For Production center
def is_production_center():
    ''' 
    Check access for Prodcution center
    '''
    def decorator(view_func):
        ''' Decorator '''
        def wrapper(request, *args, **kwargs):
            redirect_url = kwargs.get('redirect_to', reverse_lazy('dashboard'))
            if request.user.user_role == UserRole.PRODUCTION_CENTER or request.user.is_superuser:    
                redirect_to = view_func(request, *args, **kwargs)
            else:
                redirect_to = redirect(redirect_url)              
            return redirect_to
        return wrapper  
    return decorator

def is_production_center_view(cls=None, **function_args):
    ''' 
    Is Productio Center  View Dispatch
    '''
    if cls is not None:
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)
        original = cls.dispatch
        modified = method_decorator(
            is_production_center(**function_args))(original)
        cls.dispatch = modified
        return cls
    else:
        def inner_decorator(inner_cls):
            ''' Inner Decorator '''
            return is_production_center_view(inner_cls, **function_args)
        return inner_decorator

# For Checking non productin center role 
def is_classy_user():
    ''' 
    Check access for Prodcution center
    '''
    def decorator(view_func):
        ''' Decorator '''
        def wrapper(request, *args, **kwargs):
            urls='production_center:production-dashboard' if request.user.user_role == UserRole.PRODUCTION_CENTER else 'dashboard'
            redirect_url = kwargs.get('redirect_to', reverse_lazy(urls))
            if request.user.user_role != UserRole.PRODUCTION_CENTER or request.user.is_superuser:  
                redirect_to = view_func(request, *args, **kwargs)
            else:
                redirect_to = redirect(redirect_url)              
            return redirect_to
        return wrapper  
    return decorator

def is_classy_user_view(cls=None, **function_args):
    ''' 
    Is classy user  View Dispatch
    '''
    if cls is not None:
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)
        original = cls.dispatch
        modified = method_decorator(
            is_classy_user(**function_args))(original)
        cls.dispatch = modified
        return cls
    else:
        def inner_decorator(inner_cls):
            ''' Inner Decorator '''
            return is_classy_user_view(inner_cls, **function_args)
        return inner_decorator

