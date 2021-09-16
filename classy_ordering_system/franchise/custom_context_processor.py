from django.db.models.functions import TruncMonth
from django.db.models import Count
import datetime
from .models import JobModel,JobStatus

def order_status_renderer(request):
    from datetime import timedelta
    job_status_ids=JobStatus.objects.distinct().values_list('job')
    today=datetime.datetime.today()
    if not request.user.is_authenticated or request.user.is_anonymous  :
        return {}

    if  request.user.is_staff or request.user.is_superuser:
        total_orders = JobModel.objects.filter()
    else:total_orders = JobModel.objects.filter(user=request.user)
    sent = total_orders.filter(id__in=job_status_ids).annotate(
        month=TruncMonth('create_date')).order_by('-month')
    inprogress = total_orders.exclude(id__in=job_status_ids).order_by('-modify_date')
    #month=JobModel.objects.annotate(month=TruncMonth('create_date')).values('month').annotate(total=Count('job_id'))
    day_wise=total_orders.filter(create_date__year=today.year,create_date__month=today.month,create_date__day=today.day).count()
    week_wise=total_orders.filter(create_date__gte=today-timedelta(days=7) ).count()
    month_wise=total_orders.filter(create_date__year=today.year,create_date__month=today.month).count()
    year_wise=total_orders.filter(create_date__year=today.year).count()

    data= {
        'inprogress': inprogress,
        'total_sent': sent,
        'sent': sent[1:],
        'sent_first': sent[0] if sent.count() > 0 else None,
        'total_orders': total_orders,
        'total_orders_sent': sent,
        'total_orders_inprogress': inprogress,
        'day_count':day_wise,
        'week_count':week_wise,
        'month_count':month_wise,
        'year_count':year_wise,
    }
    return data