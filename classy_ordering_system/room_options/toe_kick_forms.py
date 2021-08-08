from django import forms
from room_options.models import RoomOptionsMasterModel

from room_options.conf import  TOE_KICK_DEPTH_CHOICES


class ToeKickForm(forms.ModelForm):

    class Meta:
        model = RoomOptionsMasterModel
        fields = ['width', 'height', 'notes', 'quantity', 'end_caps', 'face_color', 'toe_kick_depth', 'plywood']
        widgets = {
            'plywood': forms.CheckboxInput(attrs={
                'class': "form-check-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ToeKickForm, self).__init__(*args, **kwargs)

        self.fields['toe_kick_depth'] = forms.ChoiceField(choices=TOE_KICK_DEPTH_CHOICES, required=False)

        self.fields['width'] = forms.CharField()
        self.fields['height'] = forms.CharField()

        self.fields['width'].widget.attrs = ({
            'class': "form-control form-control-solid width toe-width numberWithFloat",
            'placeholder': "Width",
        })
        self.fields['height'].widget.attrs = ({
            'class': "form-control height form-control-solid toe-height numberWithFloat",
            'placeholder': "Height",
        })

        self.fields['quantity'] = forms.CharField()
        self.fields['quantity'].widget.attrs = (
            {"class": "form-control quantity form-control-solid toe-kicks onlyNumber",
             "placeholder": "Quantity"}
        )

    def clean_toe_kick_depth(self):
        data = self.cleaned_data['toe_kick_depth']
        if data == 0:
            return None
        return data
