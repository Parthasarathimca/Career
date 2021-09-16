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

from inventory_options.views import WoodInventoryView,\
    WoodInventoryEditView, WoodInventoryDeleteView, HardwareInventoryView, MarketingMaterialInventory, HardwareInventoryEditView, HardwareInventoryDeleteView, MarketingInventoryDeleteView, MarketingInventoryEditView, WoodItemDEscriptionsAjaxView

urlpatterns = [
    path('wood_inventory/', WoodInventoryView.as_view(), name='wood-inventory'),
    path('wood_inventory/edit/<pk>', WoodInventoryEditView.as_view(), name='edit-wood-inventory'),
    path('wood_inventory/delete/<int:pk>', WoodInventoryDeleteView.as_view(), name='delete-wood-inventory'),
    path('wood-item-description-ajax', WoodItemDEscriptionsAjaxView.as_view(), name='wood-item-description-ajax'),

    path('hardware_inventory/', HardwareInventoryView.as_view(), name='hardware-inventory'),
    path('hardware_inventory/edit/<pk>', HardwareInventoryEditView.as_view(), name='edit-hardware-inventory'),
    path('hardware_inventory/delete/<pk>', HardwareInventoryDeleteView.as_view(), name='delete-hardware-inventory'),

    path('marketing_material_inventory', MarketingMaterialInventory.as_view(), name='marketing-material-inventory'),
    path('marketing_material_inventory/delete/<int:pk>', MarketingInventoryDeleteView.as_view(), name='delete-marketing-inventory'),
    path('marketing_material_inventory/edit/<int:pk>', MarketingInventoryEditView.as_view(), name='edit-marketing-inventory')
]
