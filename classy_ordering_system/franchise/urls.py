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

from franchise.views import FranchiseDashboardView, CreateJobView, CreateRoomView, JobDetailSendOrder, JobDetailView, RoomDetailView, SendOrder,room_dropdowns,JobDetailTreeDataView,DeleteRoomView, InvertoryOrder,JobListView\
    ,JobDetailSendOrder,SendOrderTreeView

urlpatterns = [
    path('create_job/', CreateJobView.as_view(), name='create-job'),
    path('job_detail/<int:job_id>', JobDetailView.as_view(), name='job-detail'),
    path('job_list/', JobListView.as_view(), name='job-list'),
    path('create_room/job/<int:job_id>', CreateRoomView.as_view(), name='create-room'),
    path('room_detail/<int:room_id>', RoomDetailView.as_view(), name='room-detail'),
    path('room_dropdowns/', room_dropdowns, name='room-dropdown'),
    path('job-details/tree-data/<int:job_id>', JobDetailTreeDataView.as_view(), name='job-detail-tree-data'),
    path('room/delete/', DeleteRoomView.as_view(), name='delete-room'),
    path('create_inventory/', InvertoryOrder.as_view(), name='create-inventory'),
    path('job-detail/send-order/<int:job_id>', JobDetailSendOrder.as_view(), name='job-detail-send-order'),
    path('send-order/', SendOrder.as_view(), name='send_order_page'),
    path('send-order/tree-view/<int:job_id>', SendOrderTreeView.as_view(), name='send_order_tree_view'),
   
]
