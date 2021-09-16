from room_options.models.partition_models.main_model import RoomOptionsMasterModel
from enum import unique
from django import forms
from django.forms import fields, widgets
from franchise.models import JobModel, RoomModel
from franchise import messages
from .models import *


class CreateWoodInventory(forms.ModelForm):

    # left_edge_type = forms.CharField()

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['description', 'inventory', 'description2', 'part_sub_category', 'quantity', 'notes', 'height', 'width', 'depth', 'mat_type']

    def __init__(self, user=None, request=None, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
        self.fields['description2'] = forms.ModelChoiceField(queryset = InventoryExtra.objects.filter(is_active=True)) 
        self.fields['description2'].label_from_instance = lambda obj: "%s" % obj.list_name
        # self.fields['board_color'] = forms.ModelChoiceField(queryset = BoardColor.objects.filter(is_active=True)) 
        # self.fields['board_color'].label_from_instance = lambda obj: "%s" % obj.color
        self.fields['edge_type'] = forms.ModelChoiceField(queryset = EdgeType.objects.filter(is_active=True))
        self.fields['edge_type'].label_from_instance = lambda obj: "%s" % obj.title


    def clean(self):
        self.cleaned_data['description'] = self.cleaned_data.get('part_sub_category')
        self.cleaned_data['description2'] = self.cleaned_data.get('description2')
        invnetory_obj = InventoryExtra.objects.get(list_name=self.cleaned_data.get('description2'))
        self.cleaned_data['height'] = invnetory_obj.height
        self.cleaned_data['width'] = invnetory_obj.width
        self.cleaned_data['depth'] = invnetory_obj.depth
        if MaterialType.objects.filter(mat_inventory_id=invnetory_obj.id, is_active=True).first():
            self.cleaned_data['mat_type'] = MaterialType.objects.filter(mat_inventory_id=invnetory_obj.id).first().id
        data = self.cleaned_data
        return data



class CreateHardwareInventory(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['description', 'inventory', 'description2', 'part_sub_category', 'quantity', 'notes']

    def __init__(self, user=None, request=None, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.description = description
    
        self.fields['category_description'] = forms.ModelChoiceField(queryset = HardwareInventory.objects.filter(is_active=True)) 
        self.fields['category_description'].label_from_instance = lambda obj: "%s" % obj.category_description

    def clean(self):
        # self.cleaned_data['part_sub_category'] = HardwareCategory.objects.get(id=self.cleaned_data.get('description2')).description
        self.cleaned_data['description'] = self.cleaned_data.get('description')
        self.cleaned_data['category'] = self.cleaned_data.get('description2')
        self.cleaned_data['description2'] = self.cleaned_data.get('category_description')
        
        data = self.cleaned_data
        return data


class CreateMarketingMaterialInventory(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['description', 'inventory', 'description2', 'quantity', 'notes']

    def __init__(self, user=None, request=None, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['item'] = forms.ModelChoiceField(queryset = MarketingInventory.objects.filter(is_active=True)) 
        self.fields['item'].label_from_instance = lambda obj: "%s" % obj.item

    def clean(self):
        # self.cleaned_data['description'] = self.cleaned_data.get('description')
        # self.cleaned_data['category'] = self.cleaned_data.get('description2')
        self.cleaned_data['description2'] = self.cleaned_data.get('item')
        data = self.cleaned_data
        return data