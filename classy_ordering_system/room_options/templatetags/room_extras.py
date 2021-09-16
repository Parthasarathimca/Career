from django import template
from room_options.models import RoomOptionsMasterModel
from room_options.models import DrawerSizeMapModel

register = template.Library()


@register.simple_tag(takes_context=True)
def url_cutter(context, room):
    request = context['request']
    sp = request.path.split('/')
    item_url = [sp[0], sp[1], sp[2], sp[3], str(room.id)]
    print("/".join(item_url))
    return "/".join(item_url)


@register.simple_tag()
def get_std_size(std_size):
    try:
        db = DrawerSizeMapModel.objects.get(height=std_size)
    except DrawerSizeMapModel.DoesNotExist:
        return "-"
    return db.standard_size


@register.simple_tag()
def is_in_list(list, val):

    for value, text in list:
        if float(value) == float(val):
            return "checked"


@register.simple_tag()
def chk_true(val, chk):
    if val is None:
        return ""
    if val == chk:
        return "checked"
    return ""


@register.simple_tag()
def row_job_status(job_id):
    all_orders_count=RoomOptionsMasterModel.objects.filter(room__job__id=job_id).count()
    send_orders_count=RoomOptionsMasterModel.objects.filter(room__job__id=job_id,order_status='SENT').count()
    if all_orders_count>send_orders_count:
       return 'INPROGRESS'
    elif all_orders_count==send_orders_count:
        return 'SENT'

