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
from room_options.views import RoomPartitionView, RoomKDShelfView, DeleteRoomOptionView, RoomADJShelfView, \
    RoomPartitionEditView
from room_options.views.cleat_views import CleatView, CleatEditView
from room_options.views.pair_door_views import  PairDoorsView,DoorsDeleteView,room_opening_data
from room_options.views.single_door_views import SingleDoorView,room_single_opening_data
from room_options.views.l_shelf import LShelfView,LShelfDeleteView
from room_options.views.corner_shelf_views import CornerShelfView,CornorShelfDeleteView
from room_options.views.toe_kick_views import ToeKickView, ToeKickEditView
from room_options.views.top_shelf_views import TopShelfView,TopShelfDeleteView
from room_options.views.drawer_faces import DwawerFacesView,DwawerFacesDeleteView
from room_options.views.drawer_box_views import *

urlpatterns = [

    path('room_partition/<int:room_id>', RoomPartitionView.as_view(), name='room-partition'),
    path('room_partition/<int:room_id>/edit/<pk>', RoomPartitionEditView.as_view(), name='edit-room-partition'),

    path('room_kd_shelf/<int:room_id>', RoomKDShelfView.as_view(), name='room-kd-shelf'),
    path('room_update_kd_shelf/job/<int:room_id>/option/<int:id>', RoomKDShelfView.as_view(), name='update-room-kd-shelf'),
    path('room_adj_shelf/<int:room_id>', RoomADJShelfView.as_view(), name='room-adj-shelf'),
    path('room_update_adj_shelf/job/<int:room_id>/option/<int:id>', RoomADJShelfView.as_view(), name='update-room-adj-shelf'),
    path('delete/room_option/<int:pk>', DeleteRoomOptionView.as_view(), name='delete-room-option'),

    path('delete/doors/<int:pk>', DoorsDeleteView.as_view(), name='delete-doors'),
    path('pair_doors/<int:room_id>/', PairDoorsView.as_view(), name='pair-doors'),
    path('load_room_openigs/', room_opening_data, name='room-openings-data'),
    path('load_room_single_openigs/', room_single_opening_data, name='room-single-openings-data'),
    path('single_door/<int:room_id>/', SingleDoorView.as_view(), name='single-door'),

    path('drawer_box/<int:room_id>/', DrawerBoxView.as_view(), name='drawer-boxes'),
    path('drawer_box/<int:room_id>/edit/<pk>', DrawerBoxEditView.as_view(), name='edit-drawer-box'),
    path('drawer_box/<int:room_id>/delete/<pk>', DrawerBoxDeleteView.as_view(), name='delete-drawer-box'),

    path('cleat/<int:room_id>', CleatView.as_view(), name='cleat'),
    path('cleat/<int:room_id>/edit/<pk>', CleatEditView.as_view(), name='edit-cleat'),

    path('l-shelf/<int:room_id>/',LShelfView.as_view(),name='l-shelf'),
    path('delete/l-shelf/<int:room_id>/',LShelfDeleteView.as_view(),name='delete-l-shelf'),
    path('corner-shelf/<int:room_id>/',CornerShelfView.as_view(),name='corner-shelf'),
    path('delete/corner-shelf/<int:room_id>/',CornorShelfDeleteView.as_view(),name='delete-corner-shelf'), 

    path('top-shelf/<int:room_id>', TopShelfView.as_view(), name='top-shelf'),
    path('delete/top-shelf/<int:room_id>/',TopShelfDeleteView.as_view(),name='delete-top-shelf'), 
    
    path('drawer-faces/<int:room_id>', DwawerFacesView.as_view(), name='drawer-faces'),
    path('delete/drawer-faces/<int:room_id>/',DwawerFacesDeleteView.as_view(),name='delete-drawer-faces'),
    

    path('toe-kicks/<int:room_id>', ToeKickView.as_view(), name='toe-kick'),
    path('toe-kicks/<int:room_id>/edit/<pk>', ToeKickEditView.as_view(), name='edit-toe-kick'),

]

