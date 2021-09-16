from django import forms
from django.core.exceptions import ValidationError
from django.db.models.enums import Choices
from django.db.models.query_utils import QueryWrapper
from django.forms import widgets
from django.urls import conf
from room_options.models import (RoomOptionsMasterModel, 
                                RoomDrillModelMap, 
                                RoomMatTypeModelMap,
                                DoorOpeningheightWidthMapModel,DoorSingleOpeningheightWidthMapModel)

from room_options.conf import PARTITION_DRILL_CHOICES, DepthInches, PARTITION_MAT_CHOICES, PARTTION_HEIGHT_CHOICES, \
    PARTTION_DEPTH_CHOICES, DRAWER_TYPE_CHOICES, DogEared,CounterTopWidthDepth, EXPOSED_END_CHOICES
from franchise.models  import RoomModel
from room_options.conf import Description,ShelfTypeChoices,DrawerWidth, DrawerhamperTypes,LTIOverlayOptions1,DrawerHole
from room_options.models.kd_shelf_models.kd_models import *
from room_options.models.adj_shelf_models.main_model import AdjExposedEnd, AdjWidth, AdjDepth, AdjMaterial, AdjEdge, AdjInsertBacking
from room_options.models.LTI_doors_models.LTI_models import DoorSizeMapModel

class RoomPartitionForm(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['ed_type', 'left_side_drill_depth', 'left_side_drill_height',
                  'right_side_drill_depth', 'right_side_drill_height', 'notes',
                  'depth', 'height', 'mat_type', 'drill_pattern_left','drill_pattern_right',
                  'custom_drill_pattern_left', 'custom_drill_pattern_right', 'part_sub_category',
                  'quantity', 'edge_profile', 'left_3rd_line_hole', 'right_3rd_line_hole', 'dog_eared',
                  'custom_drill_code_lft', 'custom_drill_code_rgt']
        widgets = {
            'left_3rd_line_hole': forms.CheckboxInput(attrs={
                'class': "form-check-input"
            }),
            'right_3rd_line_hole': forms.CheckboxInput(attrs={
                'class': "form-check-input"
            }),
        }

    def __init__(self, request=None, description=None, form_type=None, *args, **kwargs):
        super(RoomPartitionForm, self).__init__(*args, **kwargs)
        self.request = request
        self.description = description
        self.form_type = form_type
        self.fields['height'] = forms.ChoiceField(choices=PARTTION_HEIGHT_CHOICES)
        self.fields['depth'] = forms.ChoiceField(choices=PARTTION_DEPTH_CHOICES)
        self.fields['mat_type'].choices.pop(0)
        self.fields['dog_eared'].choices.pop(0)
        self.fields['edge_profile'].choices.pop(0)
        self.fields['custom_drill_pattern_left'].choices.pop(0)
        self.fields['custom_drill_pattern_right'].choices.pop(0)

        if self.request.method == 'POST':
            if self.data.get('part_sub_category') == 'CUSTOM' and self.description == Description.PARTITION:
                self.fields['height'] = forms.CharField()
                self.fields['depth'] = forms.CharField()


    def clean(self):
        self.cleaned_data['description'] = self.description
        if self.form_type == 'STANDARD':
            if not self.cleaned_data['drill_pattern_right']:
                print(self.cleaned_data['drill_pattern_right'])
                self.cleaned_data['right_side_drill_height'] = None
                self.cleaned_data['right_side_drill_depth'] = None
                self.cleaned_data['right_3rd_line_hole'] = False
            if not self.cleaned_data['drill_pattern_left']:
                print(self.cleaned_data['drill_pattern_left'])
                self.cleaned_data['left_side_drill_height'] = None
                self.cleaned_data['left_side_drill_depth'] = None
                self.cleaned_data['left_3rd_line_hole'] = False

        return self.cleaned_data



class PairDoorsForm(forms.ModelForm):
    '''Pair door form class to  door info and store it to RoomOptionsMasterModel'''
    class Meta:
        model = RoomOptionsMasterModel
        fields = ['door_opening_size','door_drill_option','quantity','notes',
                  'door_class_insert','part_sub_category','height','width','depth', 'holes','door_glass_type']

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
        mat_type = RoomModel.objects.get(id=self.room.id).dd_mat_type
        if mat_type:
            self.cleaned_data['depth'] = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        data = self.cleaned_data
        return data

    def save(self):
        pk=self.request.GET.get('room_item')
        if pk:
           result=RoomOptionsMasterModel.objects.filter(room=self.room, id=pk).update(**self.cleaned_data)
        else:

            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self
 

class SingleDoorForm(forms.ModelForm):
    '''Single door form class to  door info and store it to RoomOptionsMasterModel'''
    class Meta:
        model = RoomOptionsMasterModel
        fields = ['door_single_opening_size', 'door_drill_option', 'quantity',
                  'notes', 'door_class_insert', 'part_sub_category',
                  'height','width','holes','door_glass_type']

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
        mat_type = RoomModel.objects.get(id=self.room.id).dd_mat_type
        if mat_type:
            self.cleaned_data['depth'] = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        data = self.cleaned_data
        return data

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
        fields = ['notes', 'part_sub_category', 'quantity', 'width', 'height',
                 'depth', 'mat_type', 'kd_shelf_edge', 'insert_backing'
                ]

    def __init__(self, request=None,  room=None, category=None, description=None, *args, **kwargs):
        super(RoomKdShelfForm, self).__init__(*args, **kwargs)
        try:
            if room:
                self.room_id = RoomModel.objects.get(id=room.id)
            self.category = category
            self.request = request
            self.description = description

            if self.request.method == 'POST' :
                if 'part_sub_category' in self.data.keys():
                    if self.data['part_sub_category'] == 'STANDARD':
                        self.fields['width'] = forms.ModelChoiceField(queryset = KdWidth.objects.all()) 
                        self.fields['width'].label_from_instance = lambda obj: "%s " % (round(obj.kd_width, 2))
                        self.fields['depth'] = forms.ModelChoiceField(queryset = KdDepth.objects.all()) 
                        self.fields['depth'].label_from_instance = lambda obj: "%s " % (round(obj.kd_depth, 2)) 
            else:
                self.fields['width'] = forms.ModelChoiceField(queryset = KdWidth.objects.all()) 
                self.fields['width'].label_from_instance = lambda obj: "%s " % (round(obj.kd_width, 2))
                self.fields['depth'] = forms.ModelChoiceField(queryset = KdDepth.objects.all()) 
                self.fields['depth'].label_from_instance = lambda obj: "%s " % (round(obj.kd_depth, 2)) 
                self.fields['mat_type'] = forms.ModelChoiceField(queryset = KdMaterial.objects.all()) 
                self.fields['mat_type'].label_from_instance = lambda obj: "%s " % (obj.kd_material_text)
                self.fields['kd_shelf_edge'] = forms.ModelChoiceField(queryset = KdEdge.objects.all()) 
                self.fields['kd_shelf_edge'].label_from_instance = lambda obj: "%s " % (obj.kd_edge_text)
                self.fields['insert_backing'] = forms.ModelChoiceField(queryset = KdInsertBacking.objects.all()) 
                self.fields['insert_backing'].label_from_instance = lambda obj: "%s " % (obj.kd_backing_text)
        
        except Exception as e:
            print(str(e), "exception in form")

    def clean(self):
        self.cleaned_data = super().clean()
        try:
            if self.request.POST.get('Plytype'):
                if self.request.POST.getlist('width') and self.request.POST.getlist('depth') and self.request.POST.getlist('quantity'):
                    post = self.request.POST
                    width = post.getlist('width')
                    depth = post.getlist('depth')
                    plytype = post.get('Plytype')
                    quantity = post.getlist('quantity')
                    self.cleaned_data['width'] = width[int(plytype)]
                    self.cleaned_data['depth'] = depth[int(plytype)]
                    self.cleaned_data['quantity'] = quantity[int(plytype)]
            else:
                self.cleaned_data['width'] = self.cleaned_data.get('width').kd_width
                self.cleaned_data['depth'] = self.cleaned_data.get('depth').kd_depth

            if self.cleaned_data.get('mat_type'):
                self.cleaned_data['mat_type'] = self.cleaned_data.get('mat_type').kd_material

        except:
            self.cleaned_data['width'] = self.cleaned_data.get('width')
            self.cleaned_data['depth'] = self.cleaned_data.get('depth')
            forms.ValidationError("Error has been occured")

        self.cleaned_data['description'] = self.description
        data = self.cleaned_data
        return data

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
        shelf = self.cleaned_data['shelf_type']
        shelf_type = dict(self.fields['shelf_type'].choices)[shelf]
        self.cleaned_data['part_sub_category'] = shelf_type.upper()
        if self.cleaned_data.get('shelf_type') == ShelfTypeChoices.get_adj_id(self):
            self.cleaned_data['drill_toe_kick']=None
            self.cleaned_data['shelfs_partitions']=None

        return self.cleaned_data

    def save(self):
        
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            id = self.room.id
            mat_type = RoomModel.objects.get(id=id).dd_mat_type
            if mat_type:
                height = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
            RoomOptionsMasterModel.objects.create(room=self.room, height=height, **self.cleaned_data)
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
        shelf = self.cleaned_data['shelf_type']
        shelf_type = dict(self.fields['shelf_type'].choices)[shelf]
        self.cleaned_data['part_sub_category'] = shelf_type.upper()
        self.cleaned_data['description2'] = f"CORNER-{shelf_type.upper()}"       
       
        if self.cleaned_data.get('shelf_type') == ShelfTypeChoices.get_adj_id(self):
            self.cleaned_data['drill_toe_kick']=None
            self.cleaned_data['shelfs_partitions']=None

        return self.cleaned_data

    def save(self):
        
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            id = self.room.id
            mat_type = RoomModel.objects.get(id=id).dd_mat_type
            if mat_type:
                height = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
            RoomOptionsMasterModel.objects.create(room=self.room, height=height, **self.cleaned_data)
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
        if request.GET.get('type')=='COUNTER_TOP':
            self.fields['width'] = forms.ChoiceField(choices =CounterTopWidthDepth.WIDTH_DEPTH)
        if request.GET.get('type') == 'CUSTOM_COUNTER_TOP' or 'CUSTOM':
            self.fields['exposed_ends'] = forms.ChoiceField(choices = EXPOSED_END_CHOICES[0:2])
        if 'type' not in request.GET or request.GET.get('type') == 'STANDARD':
            self.fields['exposed_ends'] = forms.ChoiceField(choices =EXPOSED_END_CHOICES[2:4])

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data
    
    def clean(self):
        self.cleaned_data['description'] = self.description
        self.cleaned_data['description2'] = self.cleaned_data.get('part_sub_category')
        try:
            if self.cleaned_data.get('shelf_type') == ShelfTypeChoices.get_adj_id(self):
                self.cleaned_data['drill_toe_kick'] = None
                self.cleaned_data['shelfs_partitions'] = None

            if self.cleaned_data['part_sub_category']  == "STANDARD":
                width=float(str(self.cleaned_data['width'])[0:2])
                depth=float(str(self.cleaned_data['width'])[2:])
                self.cleaned_data['width'] = width
                self.cleaned_data['depth'] = depth
               
            if self.cleaned_data['part_sub_category'] =='COUNTER_TOP':
                width_depth = self.cleaned_data['width'].split('X')
                self.cleaned_data['width'] = width_depth[0] if len(width_depth)>1 else 0
                self.cleaned_data['depth'] = width_depth[1] if len(width_depth)>1 else 0

            mat_type = RoomModel.objects.get(id=self.room.id).dd_mat_type
            if mat_type:
                self.cleaned_data['height'] = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        except Exception as e:
            print(str(e))
            
        data = self.cleaned_data
        return data

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
                self.fields['drawer_faces_holes'] = forms.ChoiceField(choices=DrawerHole.HOLE_CHOICES[8:10])         
            else:  self.fields['width'] = forms.ChoiceField(choices =DrawerWidth.DWRAWER_WIDTH_CHOICES) 
        if request.GET.get('type')=='STANDARD':
            self.fields['drawer_faces_holes'] = forms.ChoiceField(choices=DrawerHole.HOLE_CHOICES[0:8])  

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not data > 0:
            raise ValidationError("Quantity should be greater than 0")
        return data
    
    def clean(self):
        self.cleaned_data['description2'] = self.description

        if self.cleaned_data.get('drawer_faces_hamper_faces') == True:
            self.cleaned_data['description'] = 'HAMPER_FACE'
        else:
            self.cleaned_data['description'] = self.description          

        if self.cleaned_data.get('part_sub_category') == 'STANDARD':
            height = self.cleaned_data['drawer_faces_holes'].split('(')
            self.cleaned_data['height'] = height[1].replace('")', "")

        if self.cleaned_data.get('part_sub_category') == 'HAMPER_FACES':
            height = self.cleaned_data['drawer_faces_holes'].split('(')
            self.cleaned_data['height'] = height[1].replace(')', "")

        mat_type = RoomModel.objects.get(id=self.room.id).dd_mat_type
        if mat_type:
            self.cleaned_data['depth'] = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        data = self.cleaned_data
        return data

    def save(self):
        pk=self.request.GET.get('room_item')
        if pk:
           RoomOptionsMasterModel.objects.filter(room=self.room,id=pk).update(**self.cleaned_data)
        else:
            RoomOptionsMasterModel.objects.create(room=self.room, **self.cleaned_data)
        return self    

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['drawer_faces_holes','width','quantity','drawer_faces_drill_Sub_front','notes','part_sub_category','drawer_faces_hamper_faces','height']


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
        self.request = request
        self.description = description
      
        if self.request.method == 'POST' :
            if 'part_sub_category' in self.data.keys():
                if self.data['part_sub_category'] == 'STANDARD':
                    self.fields['width'] = forms.ModelChoiceField(queryset = AdjWidth.objects.all()) 
                    self.fields['width'].label_from_instance = lambda obj: "%s" % (round(obj.width, 2))
                    self.fields['depth'] = forms.ModelChoiceField(queryset = AdjDepth.objects.all()) 
                    self.fields['depth'].label_from_instance = lambda obj: "%s" % (round(obj.depth, 2))
                    
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
        try:
            if self.request.POST.get('Plytype'):
                if self.request.POST.getlist('width') and self.request.POST.getlist('depth') and self.request.POST.getlist('quantity'):
                    post = self.request.POST
                    width = post.getlist('width')
                    depth = post.getlist('depth')
                    plytype = post.get('Plytype')
                    quantity = post.getlist('quantity')
                    
                    self.cleaned_data['width'] = width[int(plytype)]
                    self.cleaned_data['depth'] = depth[int(plytype)]
                    self.cleaned_data['quantity'] = quantity[int(plytype)]
            else:
                self.cleaned_data['width'] = self.cleaned_data.get('width').width
                self.cleaned_data['depth'] = self.cleaned_data.get('depth').depth

            if self.cleaned_data.get('mat_type'):
                self.cleaned_data['mat_type'] = self.cleaned_data['mat_type']

            if self.cleaned_data.get('adj_shelf_edge'):
                self.cleaned_data['adj_shelf_edge'] = self.cleaned_data['adj_shelf_edge']

            if self.cleaned_data.get('adj_exposed_end'):
                self.cleaned_data['adj_exposed_end'] = self.cleaned_data['adj_exposed_end']
        except Exception as e:
          
            self.cleaned_data['width'] = self.cleaned_data.get('width')
            self.cleaned_data['depth'] = self.cleaned_data.get('depth')
            forms.ValidationError("Error has been occured")
            
        self.cleaned_data['description'] = self.description
        data = self.cleaned_data
        return data


class LTIDoorsForm(forms.ModelForm):

    def __init__(self,request=None,room=None,description=None, *args, **kwargs):
        super(LTIDoorsForm, self).__init__(*args, **kwargs)
        
        self.fields['overlay_options1']=forms.MultipleChoiceField(choices=LTIOverlayOptions1.OVERLAY_OPTIONS1)
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
        try:
            if not self.cleaned_data.get('lti_door_size') and self.cleaned_data.get('part_sub_category')=='LTI_DOORS':
                self.cleaned_data['lti_door_size']=DoorSizeMapModel.objects.get(description=self.description)
        except Exception as e:
            print(str(e))
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
        fields = ['droor_drawer_base_type','solid_door','glass_options','lti_door_color','lti_door_size','lti_door_type','overlay_options','overlay_options1','width','height','quantity','notes','drawer_type','lti_drawer_size','part_sub_category']


class WoodDoorsForm(forms.ModelForm):
    '''Deco Doors form class to deco door info and store it to RoomOptionsMasterModel'''
    class Meta:
        model = RoomOptionsMasterModel
        fields = ['description', 'description2', 'height', 'width', 'depth', 'part_sub_category', 'glazing', 'wood_panel_type', 'wood_door_style', 'wood_species',  'wood_stain_color', 'wood_door_french_lite', 'lti_door_type', 'quantity', 'overlay_options', 'overlay_options1', 'wood_door_custom_size', 'wood_door_size', 'wood_drawer_type', 'wood_drawer_size', 'notes', 'wood_door_material_type']

    def __init__(self, request=None, room=None, category=None,description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if room:
            self.room =RoomModel.objects.get(id=room.id)
        self.request = request
        self.description = description
           

    def clean(self):
        type = self.request.GET.get('type')
        overlay_chik = self.data.getlist('overlay-chk')
        overlay_chik = ','.join(overlay_chik)
        # self.cleaned_data['part_sub_category'] = type
        self.cleaned_data['description'] = self.description
        self.cleaned_data['description2'] = overlay_chik
        data = self.cleaned_data
        return data


