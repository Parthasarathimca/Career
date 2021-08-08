from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, FormView, View
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from franchise.models import JobModel, RoomModel,RoomColorChoiceModelMap
from franchise.forms import CreateJobForm, CreateRoomForm
from COS.core.decorators import logged_user_view
from room_options.models import RoomOptionsMasterModel
from django.contrib.auth.decorators import login_required
from room_options.conf import UrlMap

# Create your views here.


class FranchiseDashboardView(TemplateView):
    template_name = 'franchise/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(FranchiseDashboardView, self).get_context_data(**kwargs)
        context['active_jobs'] = JobModel.objects.filter(user=self.request.user)
        context['all_rooms'] = RoomModel.objects.filter(job__user=self.request.user)
        return context

@logged_user_view()
class CreateJobView(FormView):
    form_class = CreateJobForm
    template_name = 'franchise/create_job.html'

    def get_context_data(self, **kwargs):
        context = super(CreateJobView, self).get_context_data(**kwargs)
        context['jobs_in_progress'] = JobModel.objects.filter(user=self.request.user).order_by('-modify_date')
        return context

    def get_form_kwargs(self):
        '''update form args '''
        data = super(CreateJobView, self).get_form_kwargs()
        data.update({'request': self.request,

                     })
        return data


    def form_valid(self, form):
        self.instance = form.save()
        redirect_url = reverse_lazy('franchise:job-detail',
                                                kwargs={'job_id': self.instance.id}
                                            )        
        return HttpResponseRedirect(redirect_url) 
    

@logged_user_view()
class CreateRoomView(FormView):
    form_class = CreateRoomForm
    template_name = 'franchise/create_room.html'

    def get_form_kwargs(self):
        kwargs = super(CreateRoomView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['job'] = JobModel.objects.get(id=self.kwargs['job_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(CreateRoomView, self).get_context_data(**kwargs)
        context['job'] = JobModel.objects.get(id=self.kwargs['job_id'])
        return context

    def form_valid(self, form):
        form.save()
        return super(CreateRoomView, self).form_valid(form) 
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        url = reverse('franchise:job-detail', kwargs={'job_id':self.kwargs['job_id']})
        return url

class JobDetailView(TemplateView):
    template_name = "franchise/job_detail.html"
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['job'] = get_object_or_404(JobModel, id=self.kwargs['job_id'], user=self.request.user)
        context['rooms'] =RoomModel.objects.filter(job_id=self.kwargs['job_id'])
        context['room_first'] = RoomModel.objects.filter(job_id=self.kwargs['job_id']).first()
        # self.data_list=[]
        # self.room_option_list=[]
        # self.room_list=[]
        # unique_jobs=JobModel.objects.filter(id=self.kwargs['job_id'],user=self.request.user).prefetch_related('job_room')
        # for idx, job in enumerate(unique_jobs):
        #     self.data_list.append({'text':job.id})
        #     rooms=job.job_room.all()
        #     for idx_r ,each_room in  enumerate(rooms):
        #         room=RoomModel.objects.get(id=each_room.id)
        #         self.room_list.append({'text':room.room_name})
        #         room_options= RoomOptionsMasterModel.objects.filter(room=each_room)
        #         for each_room_options in room_options:
        #             self.room_option_list.append({'text':each_room_options.description})
        #         self.room_list[idx_r].update({'children':self.room_option_list})
        #         self.room_option_list=[]
        #     self.data_list[idx].update({'children':self.room_list})
        #     self.room_list=[]
        # context['job_details_tree']=self.data_list
        return context

class RoomDetailView(View):

    def get(self, *args, **kwargs):
        room = RoomModel.objects.get(id=self.kwargs['room_id'], job__user = self.request.user)
        room_details = {
            'bd_color': room.bd_color.color,
            'ed_profile': room.ed_profile.profile_text,
            'ed_color': room.ed_color.color,
            'dd_color': room.dd_color.color
        }

        return JsonResponse(room_details)
        


@login_required
def room_dropdowns(request):
    context={}
    id=request.GET.get('selected_value')
    context['dropdown_options'] = RoomColorChoiceModelMap.objects.filter(mat_type=id)
    return  render(request,'franchise/room_dropdowns.html',{"options": context})


class JobDetailTreeDataView(View):
    def form_url(self,each_room_options):
        url_conf=UrlMap()
        base_url=url_conf.url_map()
        url= base_url.get(each_room_options.description).format(str(each_room_options.room.id),str(each_room_options.id),each_room_options.part_sub_category)  if url_conf.url_map().get(each_room_options.description)else "#"
        return url

    def check_room_option(self,each_room_options):
        if self.room_option_list:
            exist=[ idx  for idx,i in enumerate(self.room_option_list) if i.get('text')==each_room_options.description]
           
            if exist:    
                self.room_option_list[exist[0]].get('children').append({'id':self.form_url(each_room_options),'text':"Height-<b>"+str(each_room_options.height)+
                    "</b>, Width -<b>"+str(each_room_options.width)+"</b>, Depth- <b>"+str(each_room_options.depth)+"</b>, Category- <b>"+str(each_room_options.part_sub_category)+",</b> Quantity-<b>"+str(each_room_options.quantity)
                    })
            else:
                self.room_option_list.append({'text':each_room_options.description,'children':[{'id':self.form_url(each_room_options), 'text':"Height-<b>"+str(each_room_options.height)+
                    "</b>, Width -<b>"+str(each_room_options.width)+"</b>, Depth- <b>"+str(each_room_options.depth)+"</b>, Category- <b>"+str(each_room_options.part_sub_category)+",</b> Quantity-<b>"+str(each_room_options.quantity)
                    }]})  
        else:
            self.room_option_list.append({'text':each_room_options.description,'children':[{'id':self.form_url(each_room_options),'text':"Height-<b>"+str(each_room_options.height)+
                    "</b>, Width -<b>"+str(each_room_options.width)+"</b>, Depth- <b>"+str(each_room_options.depth)+"</b>, Category- <b>"+str(each_room_options.part_sub_category)+",</b> Quantity-<b>"+str(each_room_options.quantity)
                    }]})
        return self.room_option_list
        
    def get(self, *args, **kwargs):
        self.context={}
        self.data_list=[]
        self.room_option_list=[]
        self.room_list=[]
        unique_jobs=JobModel.objects.filter(id=self.kwargs['job_id'],user=self.request.user).prefetch_related('job_room')
        for idx, job in enumerate(unique_jobs):
            self.data_list.append({'text':'Job Id-'+str(job.job_id)})
            rooms=job.job_room.all()
            for idx_r ,each_room in  enumerate(rooms):
                room=RoomModel.objects.get(id=each_room.id)
                self.room_list.append({'text':room.room_name})
                room_options= RoomOptionsMasterModel.objects.filter(room=each_room)
                for each_room_options in room_options:
                    self.room_option_list=self.check_room_option(each_room_options)
                self.room_list[idx_r].update({'children':self.room_option_list})
                self.room_option_list=[]
            self.data_list[idx].update({'children':self.room_list})
            self.room_list=[]
        self.context['job_details_tree']=self.data_list       
        return JsonResponse(self.data_list,safe=False )
        
