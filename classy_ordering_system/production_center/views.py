from django.shortcuts import render
from random import randint

from django.db.models import Q
from django.db import connection
from django.http.response import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from franchise.models import JobModel, JobStatus, ProductionCenter
from COS.core.decorators import logged_user_view,is_production_center_view



@logged_user_view
@is_production_center_view
class DashboardView(TemplateView):
    '''
        Dashboard View
    '''
    template_name =  "production_center/dashboard.html"
    

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['received_orders'] = JobStatus.objects.filter(production_status='INPROGRESS').order_by('-modify_date')
            context['completed_orders'] = JobStatus.objects.filter(production_status='COMPLETED').order_by('-modify_date')
        else:
            context['received_orders'] = JobStatus.objects.filter(production_center=self.request.user,production_status='INPROGRESS').order_by('-modify_date')
            context['completed_orders'] = JobStatus.objects.filter(production_center=self.request.user,production_status='COMPLETED').order_by('-modify_date')
    
        return context    


class OrderSearchView(RedirectView):
    
    def search(self):
        self.search_id
        context={}
        context['type']=self.type
        if self.request.user.is_superuser:
            if self.type=='received':
                jobs = JobStatus.objects.filter(production_status='INPROGRESS').order_by('-modify_date')
            else:jobs = JobStatus.objects.filter(production_status='COMPLETED').order_by('-modify_date')
        else:
            if self.type=='received':
                jobs = JobStatus.objects.filter(production_center=self.request.user,production_status='INPROGRESS').order_by('-modify_date')
            else:jobs = JobStatus.objects.filter(production_center=self.request.user,production_status='COMPLETED').order_by('-modify_date')
        if not self.search_id:
            if self.type=='received':
                context['received_orders']= jobs 
            else:context['completed_orders']= jobs 
            return context    
        try:
            filtered_jobs=jobs.filter(Q(job__job_id=self.search_id)|Q(job_status_id=self.search_id)|Q(job__client_id=self.search_id))
            
        except ValueError as e:
            
            filtered_jobs=jobs.filter(job__client_name__icontains=self.search_id)
        if self.type=='received':
            context['received_orders']= filtered_jobs 
        else:context['completed_orders']=filtered_jobs
        return context
        

    def get(self, *args, **kwargs):
        context={}
        self.search_id=self.request.GET.get('search_id')
        self.type=self.request.GET.get('type')
        self.page=self.request.GET.get('page')
        context= self.search()
        template='production_center/production_order_list_search.html' 
        return render(self.request,template,context)


@logged_user_view
@is_production_center_view
class ProductionOrderView(TemplateView):
    '''
        Orders  View
    '''
    template_name =  "production_center/production_orders.html"
    
    def get_query_result(self,query,key):
        with connection.cursor() as cursor:
            self.status = cursor.execute(query)
            if self.status:
                result=cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                self.context[f'{key}_columns']=columns
                self.context[f'{key}_values']   =result

    def get_context_data(self, **kwargs):
        self.context = super(ProductionOrderView, self).get_context_data(**kwargs)
        job_id=kwargs['job_id']
        job_sub_ids=self.request.GET.get('job_sub_ids')
        #job_status_id=kwargs['job_sub_id']
        job_query=f"select * from job_final_display_view where job_id in ({job_id}) and job_status_id in ({job_sub_ids});"
        
        job_detail_query=f"select * from JobLineImport_final_display_view where JobNum in ({job_id}) and JobImportNum  in ({job_sub_ids});  "
        over_all_status_query=f"select production_status from  job_final_display_view where job_id in ({job_id}) and job_status_id in ({job_sub_ids});"
        self.get_query_result(job_query,'job_item')
        self.get_query_result(job_detail_query,'job_details')
        self.get_query_result(over_all_status_query,'over_all_status')
        
        self.context['overall_status']=self.context.get('over_all_status_values')[0][0] if self.context.get('over_all_status_values')[0] else None
        return self.context    


@is_production_center_view
class CompleteOrderView(RedirectView):
    
    def get(self, *args, **kwargs):
        self.job_id=self.request.GET.get('job_id')
        job_sub_ids=self.request.GET.get('job_sub_ids')
        self.job_sub_ids=list(job_sub_ids.replace(',',''))
        print("############",self.job_sub_ids)
        self.status=self.request.GET.get('status')
        user = self.request.user
        self.update_params={"production_status":self.status}
        JobStatus.objects.filter(job__job_id=self.job_id,job_status_id__in=self.job_sub_ids).update(**self.update_params)
        
        return HttpResponse(JsonResponse({'status':200}))
