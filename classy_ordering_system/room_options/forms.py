from django import forms
from django.core.exceptions import ValidationError
from django.db.models.enums import Choices
from django.db.models.query_utils import QueryWrapper
from django.forms import widgets
from django.forms.models import inlineformset_factory
from django.urls import conf
from room_options.models import (RoomOptionsMasterModel, 
                                RoomDrillModelMap, 
                                RoomMatTypeModelMap,
                                DoorOpeningheightWidthMapModel,DoorSingleOpeningheightWidthMapModel)

from room_options.conf import PARTITION_DRILL_CHOICES, DepthInches, PARTITION_MAT_CHOICES, PARTTION_HEIGHT_CHOICES, \
    PARTTION_DEPTH_CHOICES, DRAWER_TYPE_CHOICES, DogEared
from franchise.models  import RoomModel
from room_options.conf import Description,ShelfTypeChoices,DrawerWidth
from room_options.models.kd_shelf_models.kd_models import *
from room_options.models.adj_shelf_models.main_model import AdjExposedEnd, AdjWidth, AdjDepth, AdjMaterial, AdjEdge, AdjInsertBacking

class RoomPartitionForm(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['ed_type', 'left_side_drill_depth', 'left_side_drill_height',
                  'right_side_drill_depth', 'right_side_drill_height', 'notes',
                     'depth', 'height', 'mat_type',
                    'drill_pattern_left','drill_pattern_right', 'part_sub_category',
                    'quantity', 'edge_profile', 'left_3rd_line_hole', 'right_3rd_line_hole', 'dog_eared']
        widgets = {
            'left_3rd_line_hole': forms.CheckboxInput(attrs={
                'class': "form-check-input"
            }),
            'right_3rd_line_hole': forms.CheckboxInput(attrs={
                'class': "form-check-input"
            }),
        }

    def __init__(self, id=None, request=None, category=None, description=None, *args, **kwargs):
        super(RoomPartitionForm, self).__init__(*args, **kwargs)
        self.id = id
        self.category = category
        self.request = request
        self.description = description
        self.fields['height'] = forms.ChoiceField(choices=PARTTION_HEIGHT_CHOICES)
        self.fields['depth'] = forms.ChoiceField(choices=PARTTION_DEPTH_CHOICES)
        self.fields['mat_type'].choices.pop(0)
        self.fields['dog_eared'].choices.pop(0)
        self.fields['edge_profile'].choices.pop(0)
        if self.request.method == 'POST' :
            if self.data.get('part_sub_category') == 'CUSTOM' and self.description == Description.PARTITION:
                self.fields['height'] = forms.CharField()
                self.fields['depth'] = forms.CharField()
            elif self.data.get('part_sub_category') == 'CUSTOM' and (self.description == Description.KD_SHELF or self.description == Description.ADJ_SHELF):
                self.fields['depth'] = forms.CharField()

    def clean(self):
        self.cleaned_data['description'] = self.description
        return self.cleaned_data



class PairDoorsForm(forms.ModelForm):
    '''Pair door form class to  door info and store it to RoomOptionsMasterModel'''
    class Meta:
        model = RoomOptionsMasterModel
        fields = ['door_opening_size','door_drill_option','quantity','notes',
                  'door_class_insert','part_sub_category','height','width','holes' ]

    def __init__(self, request=None, room=None, category=None,description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room =RoomModel.objects.get(id=room.id)
        self.request=request
        self.description = description
  
        #self.fields['door_opening_size'] = forms.ChoiceField(choices=DoorOpeningSize.DOOR_OPENING_SIZE_CHOICES)
        #self.fields['door_drill_option] = forms.ChoiceField(choices=DoorDrillOption.DOOR_DRILL_OPTION_CHOICES)
        
        self.fields['height'] = forms.ModelChoiceField(queryset = DoorOpeningheightWidthMapModel.objects.all()) 
        #self.fields['height'].label_from_instance = lambda obj: "%s  X %s (31 holes)" % (round(obj.width, 2), round(obj.height, 2))
        #self.fields['height'] = forms.ModelChoiceField(queryset= DoorOpeningheightWidthMapModel.objects.none())
        if self.request.method == 'POST' :
           
            if 'part_sub_category' in self.data.keys():
                if self.data['part_sub_category'] == 'CUSTOM':
                    self.fields['height'] = forms.DecimalField()
                    self.fields['width'] = forms.DecimalField()
                    
        else: 
            self.fields['height'] = forms.ModelChoiceField(queryset = DoorOpeningheightWidthMapModel.objects.all()) 
            self.fields['height'].label_from_instance = lambda obj: "%s  X %s (31 holes)" % (round(obj.width, 2), round(obj.height, 2))      
    def clean(self):
        try:    
            if isinstance(self.cleaned_data['height'], DoorOpeningheightWidthMapModel):
                self.cleaned_data['holes'] = self.cleaned_data['height'].holes
                self.cleaned_data['width'] = 0
                self.cleaned_data['width'] = self.cleaned_data['height'].width
                self.cleaned_data['height'] = self.cleaned_data['height'].height
                
        except:
            forms.ValidationError("Error has been occured")
        self.cleaned_data['description']=self.description
        return self.cleaned_data

    def save(self):
        pk=self.request.GET.get('room_item')
        if pk:
           result=RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:

            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self
 

class SingleDoorForm(forms.ModelForm):
    '''Single door form class to  door info and store it to RoomOptionsMasterModel'''
    class Meta:
        model = RoomOptionsMasterModel
        fields = ['door_single_opening_size', 'door_drill_option', 'quantity',
                  'notes', 'door_class_insert', 'part_sub_category',
                  'height','width','holes']

    def __init__(self, request=None, room=None, category=None,description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room =RoomModel.objects.get(id=room.id)
        self.request=request
        self.description=description
        self.fields['height'] = forms.ModelChoiceField(queryset = DoorSingleOpeningheightWidthMapModel.objects.all()) 
        self.fields['height'].label_from_instance = lambda obj: "%s  X %s " % (round(obj.width, 2), round(obj.height, 2))
        if self.request.method == 'POST' :
            if 'part_sub_category' in self.data.keys():
                if self.data['part_sub_category'] == 'CUSTOM':
                    self.fields['height'] = forms.DecimalField()
                    self.fields['width'] = forms.DecimalField()
                    
        else: 
            self.fields['height'] = forms.ModelChoiceField(queryset = DoorSingleOpeningheightWidthMapModel.objects.all()) 
            self.fields['height'].label_from_instance = lambda obj: "%s  X %s (31 holes)" % (round(obj.width, 2), round(obj.height, 2))      
    def clean(self):
        try:    
            if isinstance(self.cleaned_data['height'], DoorSingleOpeningheightWidthMapModel):
               # self.cleaned_data['holes'] = self.cleaned_data['height'].holes
                self.cleaned_data['width'] = 0
                self.cleaned_data['width'] = self.cleaned_data['height'].width
                self.cleaned_data['height'] = self.cleaned_data['height'].height
        except:
            forms.ValidationError("Error has been occured")
        self.cleaned_data['description']=self.description
        return self.cleaned_data

    def save(self):
        pk=self.request.GET.get('room_item')
        if pk:
           result=RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:

            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self
 


class DrawerBoxForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DrawerBoxForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].required = True
        self.fields['part_sub_category'] = forms.ChoiceField(choices=DRAWER_TYPE_CHOICES)
        self.fields['part_sub_category'].widget.attrs = {'class': "form-select form-select-solid drawer_size",
                                                         "data-hide-search": "true", "data-control": "select2",
                                                         "data-placeholder": "Select Drawer size"}


    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['height', 'notes', 'quantity', 'part_sub_category']
        widgets = {
            'height': forms.TextInput(attrs={
                'class': "form-control form-control-solid"
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4, 'cols': 15,
                'class': "form-control form-control-solid"
            }),
            'quantity': forms.TextInput(attrs={
                'class': "form-control form-control-solid"
            }),
            'part_sub_category': forms.Select(attrs={"class": "form-select form-select-solid drawer_size",
                                                    "data-hide-search":"true",
                                                    "data-placeholder": "Select Drawer size"
            })
        }


class RoomKdShelfForm(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['notes', 'part_sub_category', 'quantity', 'width', 
                 'depth', 'mat_type', 'kd_shelf_edge', 'insert_backing'
                ]

    def __init__(self, request=None,  room=None, category=None, description=None, *args, **kwargs):
        super(RoomKdShelfForm, self).__init__(*args, **kwargs)
        try:
            # self.id = id
            if room:
                self.room_id = RoomModel.objects.get(id=room.id)
            self.category = category
            self.request = request
            self.description = description

            if self.request.method == 'POST' :
                if 'part_sub_category' in self.data.keys():
                    if self.data['part_sub_category'] == 'CUSTOM':
                        self.fields['depth'] = forms.DecimalField()
                        self.fields['width'] = forms.DecimalField()
                        self.fields['insert_backing'] = forms.ModelChoiceField(queryset = KdInsertBacking.objects.all()) 
                        self.fields['insert_backing'].label_from_instance = lambda obj: "%s " % (obj.kd_backing_text)
                        self.fields['mat_type'] = forms.ModelChoiceField(queryset = KdMaterial.objects.all()) 
                        self.fields['mat_type'].label_from_instance = lambda obj: "%s " % (obj.kd_material_text)
                        self.fields['kd_shelf_edge'] = forms.ModelChoiceField(queryset = KdEdge.objects.all()) 
                        self.fields['kd_shelf_edge'].label_from_instance = lambda obj: "%s " % (obj.kd_edge_text)
                    elif self.data['part_sub_category'] == '1_IN_KD':
                        self.fields['depth'] = forms.DecimalField()
                        self.fields['width'] = forms.DecimalField()
                        self.fields['kd_shelf_edge'] = forms.ModelChoiceField(queryset = KdEdge.objects.all()) 
                        self.fields['kd_shelf_edge'].label_from_instance = lambda obj: "%s " % (obj.kd_edge_text)
                    else:
                        self.fields['width'] = forms.ModelChoiceField(queryset = KdWidth.objects.all()) 
                        self.fields['width'].label_from_instance = lambda obj: "%s " % (round(obj.kd_width, 2))
                        print(self.fields['width'], "self.fields['width']self.fields['width']self.fields['width']")
                        self.fields['depth'] = forms.ModelChoiceField(queryset = KdDepth.objects.all()) 
                        self.fields['depth'].label_from_instance = lambda obj: "%s " % (round(obj.kd_depth, 2))
                        self.fields['mat_type'] = forms.ModelChoiceField(queryset = KdMaterial.objects.all()) 
                        self.fields['mat_type'].label_from_instance = lambda obj: "%s " % (obj.kd_material_text)
                else:
                    print("No part_sub_category")
            else:
                self.fields['width'] = forms.ModelChoiceField(queryset = KdWidth.objects.all()) 
                self.fields['width'].label_from_instance = lambda obj: "%s " % (round(obj.kd_width, 2))
                self.fields['depth'] = forms.ModelChoiceField(queryset = KdDepth.objects.all()) 
                self.fields['depth'].label_from_instance = lambda obj: "%s " % (round(obj.kd_depth, 2)) 
        except Exception as e:
            print(str(e), "exception in form")

    def save(self):
        pk = self.request.GET.get('id')
        print(pk, "pkk")
        if pk:
            result = RoomOptionsMasterModel.objects.filter(room=self.room_id,id=pk).update(**self.cleaned_data)
        else:

            RoomOptionsMasterModel.objects.create(room=self.room_id, **self.cleaned_data)
        return self

    def clean(self):
        self.cleaned_data = super().clean()
        try:
            if self.cleaned_data.get('mat_type'):
                self.cleaned_data['mat_type'] = self.cleaned_data.get('mat_type').kd_material
            self.cleaned_data['width'] = self.cleaned_data.get('width').kd_width
            self.cleaned_data['depth'] = self.cleaned_data.get('depth').kd_depth
        except:
            self.cleaned_data['width'] = self.cleaned_data.get('width')
            self.cleaned_data['depth'] = self.cleaned_data.get('depth')
        self.cleaned_data['description'] = self.description
        return self.cleaned_data

class LSelfForm(forms.ModelForm):

    def __init__(self,request=None,room=None,description=None, *args, **kwargs):
        super(LSelfForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].required = True
        self.request=request
        self.room=room
        self.description=description
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data
    
    def clean(self):
        self.cleaned_data['description'] = self.description
        if self.cleaned_data.get('shelf_type') == ShelfTypeChoices.get_adj_id(self):
            self.cleaned_data['drill_toe_kick']=None
            self.cleaned_data['shelfs_partitions']=None

        return self.cleaned_data

    def save(self):
        
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self    

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['width','width2','depth','depth2' ,'quantity','notch_mitered_pard','mat_type','shelf_type','shelfs_partitions','drill_toe_kick','part_sub_category','notes']
       
class CornerSelfForm(forms.ModelForm):

    def __init__(self,request=None,room=None,description=None, *args, **kwargs):
        super(CornerSelfForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].required = True
        self.request=request
        self.room=room
        self.description=description
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data
    
    def clean(self):
        self.cleaned_data['description'] = self.description
        if self.cleaned_data.get('shelf_type') == ShelfTypeChoices.get_adj_id(self):
            self.cleaned_data['drill_toe_kick']=None
            self.cleaned_data['shelfs_partitions']=None

        return self.cleaned_data

    def save(self):
        
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self    

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['width','width2','depth','depth2' ,'quantity','notch_mitered_pard','mat_type','shelf_type','shelfs_partitions','drill_toe_kick','part_sub_category','notes']
       


class TopSelfForm(forms.ModelForm):

    def __init__(self,request=None,room=None,description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].required = True
        self.request=request
        self.room=room
        self.description=description
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data
    
    def clean(self):
        self.cleaned_data['description'] = self.description
        if self.cleaned_data.get('shelf_type') == ShelfTypeChoices.get_adj_id(self):
            self.cleaned_data['drill_toe_kick']=None
            self.cleaned_data['shelfs_partitions']=None

        return self.cleaned_data

    def save(self):
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self    

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['mat_type','exposed_ends','quantity','width','depth','notes','part_sub_category']

class DrawerFacesForm(forms.ModelForm):

    def __init__(self,request=None,room=None,description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].required = True
        self.request=request
        self.room=room
        self.description=description
        
        if request.GET.get('type') !='CUSTOM':
            if request.GET.get('type')=='HAMPER_FACES':
                self.fields['width'] = forms.ChoiceField(choices =DrawerWidth.DWRAWER_WIDTH_CHOICES[2:4])         
            else:  self.fields['width'] = forms.ChoiceField(choices =DrawerWidth.DWRAWER_WIDTH_CHOICES) 

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data
    
    def clean(self):
        self.cleaned_data['description'] = self.description
        return self.cleaned_data

    def save(self):
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self    

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['drawer_faces_holes','width','quantity','drawer_faces_drill_Sub_front','notes','part_sub_category','drawer_faces_hamper_type','drawer_faces_hamper_faces','height']


class AdjShelveForm(forms.ModelForm):
    '''Single door form class to  door info and store it to RoomOptionsMasterModel'''
    class Meta:
        model = RoomOptionsMasterModel
        fields = [
                    'notes', 'part_sub_category', 'quantity', 'width', 'adj_exposed_end',
                    'depth', 'mat_type', 'adj_shelf_edge', 'adj_insert_backing'
                ]

    def __init__(self, request=None, room=None, category=None,description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if room:
            self.room =RoomModel.objects.get(id=room.id)
        self.request=request
        self.description=description
        self.fields['width'] = forms.ModelChoiceField(queryset = AdjWidth.objects.all()) 
        self.fields['width'].label_from_instance = lambda obj: "%s" % (round(obj.width, 2))
        self.fields['depth'] = forms.ModelChoiceField(queryset = AdjDepth.objects.all()) 
        self.fields['depth'].label_from_instance = lambda obj: "%s" % (round(obj.depth, 2))

        if self.request.method == 'POST' :
            if 'part_sub_category' in self.data.keys():
                if self.data['part_sub_category'] == 'CUSTOM':
                    self.fields['depth'] = forms.DecimalField()
                    self.fields['width'] = forms.DecimalField()
                    self.fields['adj_exposed_end'] = forms.ModelChoiceField(queryset = AdjExposedEnd.objects.all()) 
                    self.fields['adj_exposed_end'].label_from_instance = lambda obj: "%s" % obj.end_code_text
                if self.data['part_sub_category'] == 'SHOE_SHELF':
                    self.fields['depth'] = forms.DecimalField()
                    self.fields['width'] = forms.DecimalField()
                    
        else: 
            self.fields['width'] = forms.ModelChoiceField(queryset = AdjWidth.objects.all()) 
            self.fields['width'].label_from_instance = lambda obj: "%s" % (round(obj.width, 2))
            self.fields['depth'] = forms.ModelChoiceField(queryset = AdjDepth.objects.all()) 
            self.fields['depth'].label_from_instance = lambda obj: "%s" % (round(obj.depth, 2))    
            self.fields['adj_shelf_edge'] = forms.ModelChoiceField(queryset = AdjEdge.objects.all()) 
            self.fields['adj_shelf_edge'].label_from_instance = lambda obj: "%s" % obj.edge_text    
            self.fields['mat_type'] = forms.ModelChoiceField(queryset = AdjMaterial.objects.all()) 
            self.fields['mat_type'].label_from_instance = lambda obj: "%s" % obj.material_text
            self.fields['adj_insert_backing'] = forms.ModelChoiceField(queryset = AdjInsertBacking.objects.all()) 
            self.fields['adj_insert_backing'].label_from_instance = lambda obj: "%s" % obj.backing_text   

    def clean(self):
        self.cleaned_data = super().clean()
        try: 
            if self.cleaned_data.get('mat_type'):
                self.cleaned_data['mat_type'] = self.cleaned_data['mat_type']

            if self.cleaned_data.get('adj_shelf_edge'):
                self.cleaned_data['adj_shelf_edge'] = self.cleaned_data['adj_shelf_edge']

            if self.cleaned_data.get('adj_exposed_end'):
                self.cleaned_data['adj_exposed_end'] = self.cleaned_data['adj_exposed_end']

            self.cleaned_data['width'] = self.cleaned_data.get('width').width
            self.cleaned_data['depth'] = self.cleaned_data.get('depth').depth

        except Exception as e:
            self.cleaned_data['width'] = self.cleaned_data.get('width')
            self.cleaned_data['depth'] = self.cleaned_data.get('depth')
            forms.ValidationError("Error has been occured")
        self.cleaned_data['description']=self.description
        return self.cleaned_data

    def save(self):
        pk=self.request.GET.get('id')
        if pk:
           result=RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:

            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self
