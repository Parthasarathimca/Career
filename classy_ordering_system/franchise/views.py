from production_center.models import TenentProductionCenterMap
from accounts.models import User
import json
from django.shortcuts import get_object_or_404, render,HttpResponse
from django.views.generic import TemplateView, FormView, View,RedirectView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse,Http404
from franchise.models import JobModel, RoomMatTypeModelMap, RoomModel,RoomColorChoiceModelMap,JobStatus,RoomStainColorChoiceModelMap,ProdMeterialColorMap
from franchise.forms import CreateJobForm, CreateRoomForm
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options import models
from room_options.models import RoomOptionsMasterModel
from production_center.models import TenentProductionCenterMap
from django.contrib.auth.decorators import login_required
from room_options.conf import UrlMap
from django.apps import apps
from COS.core.utils import Projects
from django.db import connection
from accounts.conf import UserRole
            
# Create your views here.   



class FranchiseDashboardView(TemplateView):
    template_name = 'franchise/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(FranchiseDashboardView, self).get_context_data(**kwargs)
        context['active_jobs'] = JobModel.objects.filter(user=self.request.user)
        context['all_rooms'] = RoomModel.objects.filter(job__user=self.request.user)
        return context

@logged_user_view()
@is_classy_user_view
class CreateJobView(FormView):
    form_class = CreateJobForm
    template_name = 'franchise/create_job.html'

    def get_context_data(self, **kwargs):
        project_obj=Projects()
        available_projects=None
        context = super(CreateJobView, self).get_context_data(**kwargs)
        inprogress_job=JobModel.objects.values('job_id')
        inprogress_job=[i.get('job_id')for i in inprogress_job]
        if self.request.user.is_superuser:
            context['jobs_in_progress'] = JobModel.objects.exclude(id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            context['jobs_send'] = JobModel.objects.filter(id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            available_projects=project_obj.get_available_projects()
            
        else:
            context['jobs_in_progress'] = JobModel.objects.filter(user=self.request.user).exclude(id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            context['jobs_send'] = JobModel.objects.filter(user=self.request.user,id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            available_projects=project_obj.get_available_projects(self.request.user.tenent_id)
        
        if available_projects:    
            available_projects=[project for project in available_projects.get('projects') if project.get('id') not in inprogress_job]
            context['available_projects']=available_projects   
            context['type']='Available'
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
    
    def form_invalid(self, form):
        print("Error",form.errors)
        return super().form_invalid(form)

class JobListView(RedirectView):
    
    def search(self):
        self.search_id
        context={}
        context['type']=self.type
        if self.type=='Available':
            filter_available_projects=[project for project in self.available_projects if  str(project.get('id')) in self.search_id or  str(project.get('client_id')) == self.search_id]
            if not filter_available_projects:
                filter_available_projects=[project for project in self.available_projects if  self.search_id.lower() in project.get('client_name').lower() ]
            context['available_projects']= filter_available_projects 
            return context       
        elif self.type=='Inprogress' or self.type=='send':
            if self.type=='Inprogress':
                if self.request.user.is_superuser:
                    jobs = JobModel.objects.exclude(id__in=JobStatus.objects.values_list('job')).values('id','job_id','client_id','client_name').order_by('-modify_date')
                else:jobs = JobModel.objects.filter(user=self.request.user).exclude(id__in=JobStatus.objects.values_list('job')).values('job_id','client_id','client_name').order_by('-modify_date')
            else:
                if self.request.user.is_superuser:
                    jobs=  JobModel.objects.filter(id__in=JobStatus.objects.values_list('job')).values('id','job_id','client_id','client_name').order_by('-modify_date')
                else:jobs = JobModel.objects.filter(user=self.request.user,id__in=JobStatus.objects.values_list('job')).values('job_id','client_id','client_name').order_by('-modify_date')
            
            if not self.search_id:
                if self.type=='Inprogress':
                    context['jobs_in_progress']= jobs 
                else:context['jobs_send']=jobs
                
                return context    
            filtered_jobs=[i for i in jobs if str(i.get('job_id'))==self.search_id or str(i.get('client_id'))==self.search_id]
            if not filtered_jobs:
                
                filtered_jobs=JobModel.objects.filter(user=self.request.user,client_name__icontains=self.search_id)
            if self.type=='Inprogress':
                context['jobs_in_progress']= filtered_jobs 
            else:context['jobs_send']=filtered_jobs
            return context
            

    def get(self, *args, **kwargs):
        context={}
        self.search_id=self.request.GET.get('search_id')
        self.type=self.request.GET.get('type')
        self.page=self.request.GET.get('page')
        project_obj=Projects()if self.type=='Available' else None
        if project_obj:
            if self.request.user.is_superuser:
                available_projects=project_obj.get_available_projects()
            else:available_projects=project_obj.get_available_projects(self.request.user.tenent_id)
            inprogress_job=JobModel.objects.values('job_id')
            inprogress_job=[i.get('job_id')for i in inprogress_job]
            self.available_projects=[project for project in available_projects.get('projects') if project.get('id') not in inprogress_job] 
            
        context= self.search()
        template='franchise/orders_list_search.html' if self.page == "SEND_ORDER" else  'franchise/job_list.html'
        return render(self.request,template,context)



@logged_user_view()
@is_classy_user_view()
class CreateRoomView(FormView):
    form_class = CreateRoomForm
    template_name = 'franchise/create_room.html'

    def get_form_kwargs(self):
        kwargs = super(CreateRoomView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['job'] = JobModel.objects.get(id=self.kwargs['job_id'])
        kwargs.update({'request': self.request,

                     })
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
    

@is_classy_user_view()
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
        

def get_production_center_id(request):
    if request.user.is_superuser:
        production_center=TenentProductionCenterMap.objects.all()
    else:production_center=TenentProductionCenterMap.objects.filter(tenent_id=request.user.id)
    #production_center=TenentProductionCenterMap.objects.filter(tenent_id=9)
    production_center=production_center.values("production_center") if production_center else []
    production_center_id= [pc.get("production_center") for pc in production_center]
    return production_center_id

@login_required
def room_dropdowns(request):
    context={}
    id=request.GET.get('selected_value')
    dropdown_type=request.GET.get('dropdown_type')
    production_center_id=get_production_center_id(request)
    if dropdown_type=='BOARD':
        if production_center_id and id :
            prod_mat_color= ProdMeterialColorMap.objects.filter(production_center__id__in=production_center_id,meterial_type=id)
            context['dropdown_options']=list(prod_mat_color.values_list('color__id','color__color','color__picture'))
    elif dropdown_type=='EDGE':
        context['dropdown_options'] = list(RoomColorChoiceModelMap.objects.filter(edge_type_color__id=id).values_list('id', 'color', 'picture'))
    elif dropdown_type == 'BOARD_STAIN':
        context['dropdown_options'] = list(RoomStainColorChoiceModelMap.objects.filter(mat_type_stain_color__id=id).values_list('id', 'color', 'picture'))
    return JsonResponse(context)
    # return  render(request,'franchise/room_dropdowns.html',{"options": context, 'data_length': len(context)})



@is_classy_user_view()
class JobDetailTreeDataView(View):
    SEND_ORDERS='SENT'
   
    def get_delete_url(self,delete_id,model,description=None,is_send_job=''):
        return ''' <button type="button" class="btn btn-outline-danger del-data {3} " data-delete_id={0} data-model={1} data-description='{2}' >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                <path d="M5.5 5.    5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>
                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>
                </svg> </button>'''.format(str(delete_id),model,description,is_send_job)
        
    
    def form_url(self,each_room_options):
        url_conf=UrlMap()
        base_url=url_conf.url_map()
        url= base_url.get(each_room_options.description).format(str(each_room_options.room.id),str(each_room_options.id),each_room_options.part_sub_category)  if url_conf.url_map().get(each_room_options.description)else "#"
        return url

    def check_room_option(self,each_room_options):
        if self.room_option_list:
            exist=[ idx  for idx,i in enumerate(self.room_option_list) if i.get('text')==each_room_options.description]
           
            if exist:    
                text="Height-<b>"+str(each_room_options.height)+"</b>, Width -<b>"+str(each_room_options.width)+"</b>, Depth- <b>"+str(each_room_options.depth)+"</b>, Category- <b>"+str(each_room_options.part_sub_category)+",</b> Quantity-<b>"+str(each_room_options.quantity)
                self.room_option_list[exist[0]].get('children').append({'id':self.form_url(each_room_options),'delete_url': self.get_delete_url(each_room_options.id,'RoomOptionsMasterModel'),'text':text
                    })   
                if each_room_options.order_status==self.SEND_ORDERS : self.disabled_nodes_list.append(self.form_url(each_room_options))
            else:
                text="Height-<b>"+str(each_room_options.height)+"</b>, Width -<b>"+str(each_room_options.width)+"</b>, Depth- <b>"+str(each_room_options.depth)+"</b>, Category- <b>"+str(each_room_options.part_sub_category)+",</b> Quantity-<b>"+str(each_room_options.quantity)
                self.room_option_list.append({ 'text':each_room_options.description,'delete_url': self.get_delete_url(self.room.id,'RoomOptionsMasterModel',each_room_options.description,self.is_send_job),'children':[{'id':self.form_url(each_room_options),'delete_url': self.get_delete_url(each_room_options.id,'RoomOptionsMasterModel'), 'text':text
                    }]})
               #if each_room_options.order_status==self.SEND_ORDERS : self.disabled_nodes_list.append(each_room_options.description+"_"+str(each_room_options.room.id))   
                if each_room_options.order_status==self.SEND_ORDERS :self.disabled_nodes_list.append(self.form_url(each_room_options))
        else:
            text="Height-<b>"+str(each_room_options.height)+"</b>, Width -<b>"+str(each_room_options.width)+"</b>, Depth- <b>"+str(each_room_options.depth)+"</b>, Category- <b>"+str(each_room_options.part_sub_category)+",</b> Quantity-<b>"+str(each_room_options.quantity)
            self.room_option_list.append({'text':each_room_options.description,'delete_url': self.get_delete_url(self.room.id,'RoomOptionsMasterModel',each_room_options.description,self.is_send_job ),'children':[{'id':self.form_url(each_room_options),'delete_url': self.get_delete_url(each_room_options.id,'RoomOptionsMasterModel'),'text':text
                    }]})
            #if each_room_options.order_status==self.SEND_ORDERS : self.disabled_nodes_list.append(each_room_options.description+"_"+str(each_room_options.room.id)) 
            if each_room_options.order_status==self.SEND_ORDERS :  self.disabled_nodes_list.append(self.form_url(each_room_options))
        return self.room_option_list

    def get_tree_details(self,request_type=None):
        self.context={}
        self.data_list=[]
        self.room_option_list=[]
        self.room_list=[]
        self.disabled_nodes_list=[]
        
        if self.request.user.is_superuser:
            unique_jobs=JobModel.objects.filter(id=self.kwargs['job_id']).prefetch_related('job_room')
        else:unique_jobs=JobModel.objects.filter(id=self.kwargs['job_id'],user=self.request.user).prefetch_related('job_room')
        
        self.is_send_job=JobStatus.objects.filter(job_id=self.kwargs['job_id']).count()
        self.is_send_job= 'd-none' if self.is_send_job else ''
        
        for idx, job in enumerate(unique_jobs):
            self.data_list.append({'text':'Job Id- <b>'+str(job.job_id)+'<b>','delete_url':self.get_delete_url(job.id,'JobModel',None,self.is_send_job),'id':job.job_id  })
            
            #if job.order_status==self.SEND_ORDERS :self.disabled_nodes_list.append(job.job_id) 

            rooms=job.job_room.all()
            for idx_r ,each_room in  enumerate(rooms):
                self.room=RoomModel.objects.get(id=each_room.id)
                #if self.room.order_status==self.SEND_ORDERS :self.disabled_nodes_list.append(self.room.room_name) 
            
                self.room_list.append({'text':'<b>'+self.room.room_name+'<b>','delete_url':self.get_delete_url(self.room.id,'RoomModel',None,self.is_send_job)})
                room_options= RoomOptionsMasterModel.objects.filter(room=each_room).order_by('part_sub_category')
                for each_room_options in room_options:
                    self.room_option_list=self.check_room_option(each_room_options)
                self.room_list[idx_r].update({'children':self.room_option_list})
                self.room_option_list=[]
            self.data_list[idx].update({'children':self.room_list})
            self.room_list=[]
        self.context['job_details_tree']=self.data_list       
        if (self.request.is_ajax()and request_type ==None)  :
            return JsonResponse(self.data_list,safe=False )
        else:return self.disabled_nodes_list

    
    def get(self, *args, **kwargs):
        return self.get_tree_details()
        # self.context={}
        # self.data_list=[]
        # self.room_option_list=[]
        # self.room_list=[]
        # self.disabled_nodes_list=[]
        # unique_jobs=JobModel.objects.filter(id=self.kwargs['job_id'],user=self.request.user).prefetch_related('job_room')
        # for idx, job in enumerate(unique_jobs):
        #     self.data_list.append({'text':'Job Id-'+str(job.job_id)})
            
        #     if job.order_status==self.SEND_ORDERS :self.disabled_nodes_list.append(job.name) 

        #     rooms=job.job_room.all()
        #     for idx_r ,each_room in  enumerate(rooms):
        #         self.room=RoomModel.objects.get(id=each_room.id)
        #         if self.room.order_status==self.SEND_ORDERS :self.disabled_nodes_list.append(self.room) 
            
        #         self.room_list.append({'text':'<b>'+self.room.room_name+'<b>','delete_url':self.get_delete_url(self.room.id,'RoomModel')})
        #         room_options= RoomOptionsMasterModel.objects.filter(room=each_room)
        #         for each_room_options in room_options:
        #             if each_room_options==self.SEND_ORDERS :self.disabled_nodes_list.append(each_room_options.description) 
        #             self.room_option_list=self.check_room_option(each_room_options)
        #         self.room_list[idx_r].update({'children':self.room_option_list})
        #         self.room_option_list=[]
        #     self.data_list[idx].update({'children':self.room_list})
        #     self.room_list=[]
        # self.context['job_details_tree']=self.data_list       
        # if self.request.is_ajax():
        #     return JsonResponse(self.data_list,safe=False )
        # else:return self.disabled_nodes_list

@is_classy_user_view()    
class DeleteRoomView(RedirectView):
    
    def get(self, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        self.pk=self.request.GET.get('pk')
        self.model_name=self.request.GET.get('model')
        self.description=self.request.GET.get('description')
        #try:
        user = self.request.user
        self.app_name='room_options' if self.model_name=='RoomOptionsMasterModel' else 'franchise'
        model=apps.get_model(app_label=self.app_name, model_name=self.model_name) 
       
        if self.description and self.description != 'None':
            model.objects.filter(room__id=self.pk,description=self.description).delete()
        else:
            deld=model.objects.get(id=self.pk).delete()
        # except:
        #     raise Http404
        return HttpResponse(JsonResponse({'status':200}))
        


@is_classy_user_view()
class InvertoryOrder(TemplateView):
    template_name = 'franchise/create_inventory.html'

    def get_context_data(self, **kwargs):
        context = super(InvertoryOrder, self).get_context_data(**kwargs)
        context['active_jobs'] = JobModel.objects.filter(user=self.request.user)
        context['all_rooms'] = RoomModel.objects.filter(job__user=self.request.user)
        return context

@is_classy_user_view()
class JobDetailSendOrder(RedirectView):

    def update_room_masters(self):
        start=0
        if self.role_back_data:
            self.update_param.update({'order_status':'INPROGRESS'})
        else:self.update_param.update({'job_status':self.job_Status})

        for counter in range(0,len(self.send_order_list)+1,3):
            data=self.send_order_list[start:counter]
            start=counter
            if counter==0:continue
            if data[1] !='RoomOptionsMasterModel':
                continue    
            self.model_name=data[1]
            self.description=data[2]
            self.pk=data[0]
            self.app_name='room_options' if self.model_name=='RoomOptionsMasterModel' else 'franchise'
            model=apps.get_model(app_label=self.app_name, model_name=self.model_name) 
            if not  self.description or self.description == 'None' :
               
               model.objects.filter(id=self.pk,job_status_id__isnull=True).update(**self.update_param)
               self.rolback=False

    def roll_back(self):
        self.job_Status.delete()
        self.role_back_data=True    
        self.update_room_masters()

    def call_sp(self):
        try:
            print('SP Call : ',(self.job_Status.job.job_id,self.job_Status.job_status_id,self.job_Status.production_center.name,self.job_Status.order_send_time,))
            with connection.cursor() as cursor:
                result = cursor.callproc("JobLineImport_insert_p",(self.job_Status.job.job_id,self.job_Status.job_status_id,self.job_Status.production_center.name,self.job_Status.order_send_time))# calls JobLineImport_insert_p PROCEDURE 
                print("SP Result : ",result)
        except Exception as e:
            print("Exception : ",e)
            self.roll_back()
        
    def job_status_update(self):
        job_status_id=JobStatus.objects.filter(job_id=self.job_id).count()+1
        self.payload={'job_id':self.job_id,'production_center_id':self.production_center,'production_status':'INPROGRESS','job_status_id':job_status_id}
        self.job_Status=JobStatus.objects.create(**self.payload)
        
    def get(self, *args, **kwargs):
     
        send_order_list=self.request.GET.get('send_order_list')
        self.production_center=self.request.GET.get('production_center')
        self.job_id=kwargs['job_id']
        self.send_order_list=json.loads(send_order_list)
        self.user = self.request.user
        self.update_param={'order_status':'SENT'}
        self.rolback=True
        self.role_back_data=False
        
         #job status insert
        result=self.job_status_update()
        #RoomOptionsMaster status change
        self.update_room_masters()
        #Store Procedure Call
        self.call_sp()
        
        if self.rolback:
            self.roll_back()

        return HttpResponse(JsonResponse({'status':200}))
            
@is_classy_user_view()
class JobDetailView(TemplateView,JobDetailTreeDataView):
    template_name = "franchise/job_detail.html"
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['job'] = get_object_or_404(JobModel, id=self.kwargs['job_id'])
        else:context['job'] = get_object_or_404(JobModel, id=self.kwargs['job_id'], user=self.request.user)
        context['rooms'] =RoomModel.objects.filter(job_id=self.kwargs['job_id'])
        context['room_first'] = RoomModel.objects.filter(job_id=self.kwargs['job_id']).first()
        disabled_nodes=super().get_tree_details()
        context['disabled_nodes']=disabled_nodes
        return context

class SendOrder(TemplateView):
    template_name = "franchise/send_order.html"
    def get_context_data(self, **kwargs):
        context = super(SendOrder, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['jobs_in_progress'] = JobModel.objects.exclude(id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            context['jobs_send'] =  JobModel.objects.filter(id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
        else:
            context['jobs_in_progress'] = JobModel.objects.filter(user=self.request.user).exclude(id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            context['jobs_send'] = JobModel.objects.filter(user=self.request.user,id__in=JobStatus.objects.values_list('job')).order_by('-modify_date')
            
        return context
class SendOrderTreeView(TemplateView,JobDetailTreeDataView):
    
    def get(self, *args, **kwargs):
        template_name = "franchise/send_order_tree.html"
        context = {}
        if self.request.user.is_superuser:
            context['job'] = get_object_or_404(JobModel, id=self.kwargs['job_id'])
            context['production_center'] =User.objects.filter(user_role=UserRole.PRODUCTION_CENTER)
            #context['default_pc']=TenentProductionCenterMap.objects.filter(tenent_id=7)
        else:
            context['job'] = get_object_or_404(JobModel, id=self.kwargs['job_id'], user=self.request.user)
            context['production_center'] =User.objects.filter(user_role=UserRole.PRODUCTION_CENTER)
            context['default_pc']=TenentProductionCenterMap.objects.filter(tenent_id=self.request.user.id)
        context['rooms'] =RoomModel.objects.filter(job_id=self.kwargs['job_id'])
        context['room_first'] = RoomModel.objects.filter(job_id=self.kwargs['job_id']).first()
        disabled_nodes=super().get_tree_details(True)
        context['disabled_nodes']=disabled_nodes
        all_orders_count=RoomOptionsMasterModel.objects.filter(room__job__id=self.kwargs['job_id']).count()
        send_orders_count=RoomOptionsMasterModel.objects.filter(room__job__id=self.kwargs['job_id'],order_status='SENT').count()
        if all_orders_count>send_orders_count:
            context['tree_job_stauts']='INPROGRESS'
        elif all_orders_count==send_orders_count:
            context['tree_job_stauts']='SENT'

        print("context",context)
        return render(self.request,template_name,context)