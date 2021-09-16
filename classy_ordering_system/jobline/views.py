from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from franchise.models import JobModel, RoomMatTypeModelMap
from django.template.loader import get_template
from jobline.models import Joblineimport


def joblinexml(request, job_id):

    job = JobModel.objects.get(job_id=job_id)
    material_list = RoomMatTypeModelMap.objects.filter(
        mat_code__in=Joblineimport.objects.filter(jobnum=job.job_id).values_list('materialtypecode'))

    template_xml = get_template('jobline/jobline.xml')
    context = {'job': job, 'material_list': material_list}
    output = template_xml.render(context)
    return HttpResponse(output, content_type='text/xml')
