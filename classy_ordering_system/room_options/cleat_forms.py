from django import forms
from room_options.models import RoomOptionsMasterModel

from room_options.conf import CLEAT_WIDTH_CHOICES


class CleatForm(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = [ 'width', 'height', 'notes', 'mat_type', 'quantity', 'cleat_exposed_ends']

    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type', "STANDARD")
        super(CleatForm, self).__init__(*args, **kwargs)
        if form_type == 'STANDARD':
            self.fields['width'] = forms.ChoiceField(choices=CLEAT_WIDTH_CHOICES)
        elif form_type == 'CUSTOM':
            self.fields['width'] = forms.CharField()
            self.fields['height'] = forms.CharField(widget=forms.HiddenInput())
        elif form_type == 'COVER':
            self.fields['width'] = forms.CharField(widget=forms.HiddenInput())
            self.fields['height'] = forms.CharField(widget=forms.HiddenInput())


        self.fields['width'].widget.attrs = ({
            'class': 'form-control width form-control-solid numberWithFloat custom-width',
            'placeholder': "Width",
        })

        self.fields['mat_type'].choices.pop(0)
        self.fields['quantity'] = forms.CharField()
        self.fields['quantity'].widget.attrs = ({"class": "form-control form-control-solid quantity qty onlyNumber custom-qty",
                                                "placeholder":"Qty"})

