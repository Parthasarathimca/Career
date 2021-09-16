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
import django
from django.contrib import admin
from django.urls import path, include
from accounts.views import DashboardView
from django.conf.urls.static import static
from django.conf import settings
# from accounts.views import LoginView

urlpatterns = [
    # path('classy/classy_admin/login/', LoginView.as_view()),
    path('classy/classy_admin/', admin.site.urls),
    path('classy/', DashboardView.as_view(), name='dashboard'),
    path('classy/accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('classy/franchise/', include(('franchise.urls', 'franchise'), namespace='franchise')),
    path('classy/room/', include(('room_options.urls', 'room_options'), namespace='room_options')),
    path('classy/inventory/', include(('inventory_options.urls', 'inventory_options'), namespace='inventory_options')),
    path('classy/production/', include(('production_center.urls', 'production_center'), namespace='production_center')),
    path('classy/jobline/', include(('jobline.urls', 'production_center'), namespace='production_center')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_template = 'admin/custom_index.html'
admin.autodiscover()
