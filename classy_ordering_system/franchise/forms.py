from enum import unique
from django import forms
from django.forms import fields, widgets
from franchise.models import JobModel, RoomModel,ProdMeterialColorMap,RoomMatTypeModelMap
from COS.core.utils import Projects


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
        fields = ['job_id', 'client_id','client_name','job_description','email','job_install_start_date','job_install_end_date','job_updated_at',
        'designer','is_project_admin']

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

    def clean(self):
        project_obj=Projects()
        available_projects=project_obj.get_available_projects(self.request.user.tenent_id)
        #available_projects=project_obj.get_available_projects()
        available_projects=available_projects.get('projects')
        selected_project=[ i for i in available_projects if i.get('id')== int(self.cleaned_data.get('job_id'))]
        selected_project=selected_project[0] if len(selected_project)==1 else {}
        self.cleaned_data['email']=selected_project.get('email')
        self.cleaned_data['job_install_start_date']=selected_project.get('install_start_date')
        self.cleaned_data['job_install_end_date']=selected_project.get('install_end_date')
        self.cleaned_data['job_updated_at']=selected_project.get('updated_at')
        self.cleaned_data['designer']=selected_project.get('designer')
        self.cleaned_data['is_project_admin']=selected_project.get('isProjectAdmin')
    def save(self):
        job = JobModel.objects.create(user=self.request.user, **self.cleaned_data)
        return job

class CreateRoomForm(forms.ModelForm):

    is_dd_same = forms.NullBooleanField()

    class Meta:
        model = RoomModel
        fields = ['is_dd_same','room_name', 'mat_type', 'bd_color', 'ed_color', 'ed_profile', 'ed_type',
                    'dd_color','dd_mat_type','dd_ed_profile', 'dd_ed_type', 'dd_ed_color', 'mat_color_stain', 'dd_mat_color_stain',]
       # fields = ['room_name', 'is_dd_same', 'room_name', 'mat_type', 'bd_color', 'ed_color', 'ed_profile', 'ed_type']                    
        widgets = {
            'mat_type': forms.RadioSelect(),
            'dd_mat_type': forms.Select(attrs={"class": "form-select form-select-solid drawer_size",
                                                    "id":"dd_mat_type",
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


    def __init__(self, request=None,user=None, job=None, *args, **kwargs):
        from franchise.views import get_production_center_id
        self.request=request
        super(CreateRoomForm, self).__init__(*args, **kwargs)
        self.job = job
        self.fields['job'] = forms.ModelChoiceField(queryset=JobModel.objects.filter(user=user))
        production_center_id=get_production_center_id(self.request)
        prod_mat= ProdMeterialColorMap.objects.filter(production_center__id__in=production_center_id)
        
        prod_mat=prod_mat.values('meterial_type__id')
        
        prod_mat_ids= [mat.get('meterial_type__id') for mat in prod_mat]
        print(">>>>>>>",RoomMatTypeModelMap.objects.filter(id__in=prod_mat_ids))
        self.fields['mat_type']=forms.ModelChoiceField(queryset=RoomMatTypeModelMap.objects.filter(id__in=prod_mat_ids))

    def clean(self):

        self.cleaned_data['job'] = self.job
        if 'is_dd_same' in self.cleaned_data.keys():
            if self.cleaned_data['is_dd_same']:
                self.cleaned_data.pop('is_dd_same')
                self.cleaned_data['dd_color'] = self.cleaned_data.get('bd_color')
                self.cleaned_data['dd_mat_type'] = self.cleaned_data.get('mat_type')
                self.cleaned_data['dd_ed_type'] = self.cleaned_data.get('ed_type')
                self.cleaned_data['dd_ed_profile'] = self.cleaned_data.get('ed_profile')
                self.cleaned_data['dd_ed_color'] = self.cleaned_data.get('ed_color')
                self.cleaned_data['dd_mat_color_stain'] = self.cleaned_data.get('mat_color_stain')
            else:
                self.cleaned_data.pop('is_dd_same')

            # else:
        #     if not self.cleaned_data.get('dd_color', None) or not self.cleaned_data.get('dd_mat_type', None) or not self.cleaned_data.get('dd_ed_type', None) or not self.cleaned_data.get('dd_ed_profile', None) or not self.cleaned_data.get('dd_ed_color', None):
        #         raise forms.ValidationError("Kindly fill all the fields")
        data = self.cleaned_data
        return self.cleaned_data

    def save(self):
       
        RoomModel.objects.create(**self.cleaned_data)
        return self


