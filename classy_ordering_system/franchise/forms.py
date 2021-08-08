from enum import unique
from django import forms
from django.forms import fields, widgets
from franchise.models import JobModel, RoomModel
from franchise import messages

class CreateJobForm(forms.ModelForm):

    # job_id = forms.IntegerField(required=True, 
    #                             error_messages={
    #                             'required': messages.FIELD_REQUIRED,
    #                             'invalid': messages.ENTER_INTEGER
    #                             })

    # job_description = forms.CharField(widget=forms.Textarea, required=True,
    #                                 error_messages={
    #                             'required': messages.FIELD_REQUIRED,
    #                             })

    # client_id = forms.IntegerField(required=True,
    #                                 error_messages={
    #                             'required': messages.FIELD_REQUIRED,
    #                             'invalid': messages.ENTER_INTEGER
    #                             })

    class Meta:
        model = JobModel
        fields = ['job_id', 'client_id']

    def __init__(self, request=None, user=None, image_path=None, *args, **kwargs):
        self.request = request
        super(CreateJobForm, self).__init__(*args, **kwargs)

    def clean_job_id(self):
        job_id = self.data['job_id']
        try:
            JobModel.objects.get(job_id=job_id) 
            raise forms.ValidationError("This job id already exists")
        except JobModel.DoesNotExist:
            pass
        
        return job_id
    
    def save(self):
        job = JobModel.objects.create(user=self.request.user, **self.cleaned_data)
        return job


class CreateRoomForm(forms.ModelForm):

    is_dd_same = forms.NullBooleanField()

    class Meta:
        model = RoomModel
        fields = ['is_dd_same','room_name', 'mat_type', 'bd_color', 'ed_color', 'ed_profile', 'ed_type',
                    'dd_color','dd_mat_type','dd_ed_profile', 'dd_ed_type', 'dd_ed_color']
       # fields = ['room_name', 'is_dd_same', 'room_name', 'mat_type', 'bd_color', 'ed_color', 'ed_profile', 'ed_type']                    
        widgets = {
            'mat_type': forms.RadioSelect(),
            'dd_mat_type': forms.Select(attrs={"class": "form-select form-select-solid drawer_size",
                                                    "id":"dd_mat_type",
                                                    "data-hide-search":"true",
                                                    "data-control":"select2",
                                                    "required":"true",
                                                    "data-placeholder": "Select  Material Type"
            }),
            'dd_ed_profile': forms.Select(attrs={"class": "form-select form-select-solid drawer_size",
                                                    "data-hide-search":"true",
                                                    "required":"true",
                                                    "data-control":"select2",
                                                    "data-placeholder": "Select  Edge Type"
            }),
            
        }


    def __init__(self, user=None, job=None, *args, **kwargs):
        super(CreateRoomForm, self).__init__(*args, **kwargs)
        self.job = job
        self.fields['job'] = forms.ModelChoiceField(queryset=JobModel.objects.filter(user=user))


    def clean(self):
        self.cleaned_data['job'] = self.job
        if 'is_dd_same' in self.cleaned_data.keys():
            if self.cleaned_data['is_dd_same']:
                self.cleaned_data.pop('is_dd_same')
                self.cleaned_data['dd_color'] = self.cleaned_data['bd_color']
                self.cleaned_data['dd_mat_type'] = self.cleaned_data['mat_type']
                self.cleaned_data['dd_ed_type'] = self.cleaned_data['ed_type']
                self.cleaned_data['dd_ed_profile'] = self.cleaned_data['ed_profile']
                self.cleaned_data['dd_ed_color'] = self.cleaned_data['ed_color']
            else:
                self.cleaned_data.pop('is_dd_same')

            # else:
        #     if not self.cleaned_data.get('dd_color', None) or not self.cleaned_data.get('dd_mat_type', None) or not self.cleaned_data.get('dd_ed_type', None) or not self.cleaned_data.get('dd_ed_profile', None) or not self.cleaned_data.get('dd_ed_color', None):
        #         raise forms.ValidationError("Kindly fill all the fields")
        return self.cleaned_data

    def save(self):
       
        RoomModel.objects.create(**self.cleaned_data)
        return self


