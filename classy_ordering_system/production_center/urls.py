
from django.contrib import admin
from django.urls import path

from .views import DashboardView,OrderSearchView,ProductionOrderView,CompleteOrderView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='production-dashboard'),   
    path('order-search/', OrderSearchView.as_view(), name='order-search'),
    path('orders/<int:job_id>/', ProductionOrderView.as_view(), name='orders'),
    path('order-complete/', CompleteOrderView.as_view(), name='order-complete'),
]
