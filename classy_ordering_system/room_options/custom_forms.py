import inspect
from decimal import Decimal

from django import forms

from inventory_options.models import BoardColor
from room_options.models import RoomOptionsMasterModel

from room_options.conf import Description, BOARD_COLOR_CHOICES
from room_options.models.custom_models.custom_models import CustomMapCategory, CustomMapEdgeType, CustomMapEdgeProfile, \
    CustomMapEdgeColor


class CustomForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=CustomMapCategory.objects.all(), initial=0)

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['custom_material', 'notes', 'quantity',  'height', 'width', 'depth', 'l1ep', 'l1et', 'custom_bd_color',
                  'custom_st_color', 'l1ec', 'l2ep', 'l2et', 'l2ec', 's1ep', 's1et', 's1ec', 's2ep', 's2et', 's2ec',
                  'custom_drill_left', 'custom_drill_right']

    def __init__(self, *args, **kwargs):

        super(CustomForm, self).__init__(*args, **kwargs)
        self.fields['width'] = forms.CharField(required=False)
        self.fields['width'].widget.attrs = ({
            'class': "form-control form-control-solid numberWithFloat width",
            'placeholder': "Width",
        })
        self.fields['height'] = forms.CharField(required=False)
        self.fields['height'].widget.attrs = ({"class": "form-control form-control-solid numberWithFloat height",
                                               "placeholder": "Height"})
        self.fields['depth'] = forms.CharField(required=False)
        self.fields['depth'].widget.attrs = ({"class": "form-control form-control-solid numberWithFloat depth",
                                               "placeholder": "Depth"})
        self.fields['quantity'] = forms.CharField(required=False)
        self.fields['quantity'].widget.attrs = ({"class": "form-control form-control-solid onlyNumber quantity",
                                                 "placeholder": "Qty"})

    def clean_height(self):
        if self.cleaned_data['height'] != '':
            return Decimal(self.cleaned_data['height'])
        return None

    def clean_width(self):
        if self.cleaned_data['width'] != '':
            return Decimal(self.cleaned_data['width'])
        return None

    def clean_depth(self):
        if self.cleaned_data['depth'] != '':
            return Decimal(self.cleaned_data['depth'])
        return None

