from django import forms
from room_options.models import RoomOptionsMasterModel, DrawerBox

from room_options.conf import DRAWER_SIZE_CHOICES, DRAWER_BOX_DEPTH_CHOICES, DrawerOpening, \
    SUB_FRONT_CHOICES, DrawerBoxType


class DrawerBoxForm(forms.ModelForm):
    custom_height = forms.CharField(required=False)

    class Meta:
        model = DrawerBox
        fields = ['height', 'quantity', 'size', 'depth', 'opening', 'drill_sub_front', 'standard_melamine', 'notes']

    def __init__(self, *args, **kwargs):
        super(DrawerBoxForm, self).__init__(*args, **kwargs)
        self.fields['size'] = forms.ChoiceField(choices=DRAWER_SIZE_CHOICES)
        self.fields['opening'] = forms.ChoiceField(choices=DrawerOpening.DRAWER_OPENING_CHOICES)
        self.fields['depth'] = forms.ChoiceField(choices=DRAWER_BOX_DEPTH_CHOICES)
        self.fields['drill_sub_front'] = forms.ChoiceField(choices=SUB_FRONT_CHOICES)
        self.fields['height'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['standard_melamine'] = forms.ChoiceField(choices=DrawerBoxType.DRAWER_BOX_TYPE_CHOICES,
                                                             required=False, widget=forms.RadioSelect)
        self.fields['standard_melamine'].empty_label = None


        self.fields['quantity'] = forms.CharField()
        # self.fields['quantity'].widget.attrs = ({"class": "form-control form-control-solid no_of_boxes onlyNumber",
        #                                         "placeholder": "Qty"})
