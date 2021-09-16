import json
from time import sleep

from django.http import Http404, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from room_options.forms import RoomPartitionForm
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.models import RoomOptionsMasterModel
from room_options.conf import Description, DogEared
# Create your views here.
from room_options.utils import RoomViewMixin
from room_options.models import *
@is_classy_user_view()
class RoomPartition(FormView, RoomViewMixin):
    form_class = RoomPartitionForm
    req_type = "Standard"

    def get_template_names(self):
        if self.req_type == 'CUSTOM':
            template_name = 'room_options/partitions/custom_partition.html'
        else:
            template_name = 'room_options/partitions/create_partition.html'
        return template_name


    def get_success_url(self, *args, **kwargs):
        if self.req_type == 'CUSTOM':
            return reverse_lazy('room_options:room-partition', kwargs={'room_id': self.kwargs['room_id']}) + "?type=CUSTOM"
        return reverse_lazy('room_options:room-partition', kwargs={'room_id': self.kwargs['room_id']})

    def get_context_data(self, **kwargs):
        context = super(RoomPartition, self).get_context_data(**kwargs)
        context['partitions'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.PARTITION)
        return context

    def get_form_kwargs(self):
        '''update form args '''
        data = super(RoomPartition, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': Description.PARTITION, 'form_type': self.req_type})
        return data


    def form_invalid(self, form):
        return super(RoomPartition, self).form_invalid(form)

    def form_valid_save(self, form, type):
        id = self.kwargs.get('room_id')
        mat_type = RoomModel.objects.get(id=id).dd_mat_type

        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.PARTITION
        obj.category = type
        if mat_type:
            obj.width = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        obj.save()
        messages.success(self.request, 'Partition has been added')
        return super(RoomPartition, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class RoomPartitionView(RoomPartition):
    
    form_class = RoomPartitionForm

    def dispatch(self, request, *args, **kwargs):
        self.req_type = self.request.GET.get('type', "STANDARD")
        return super(RoomPartitionView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RoomPartitionView, self).get_initial()
        details = {'edge_profile': 1, 'dog_eared':  DogEared.NO_DOG, 'mat_type': 1, 'custom_drill_pattern_left': 1,
                   'custom_drill_pattern_right': 1, 'left_3rd_line_hole': False, 'right_3rd_line_hole': False}
        initial.update(details)
        return initial

    def form_valid(self, form):
        return self.form_valid_save(form, self.request.GET.get('type'))

@is_classy_user_view()
class RoomPartitionEditView(UpdateView, RoomPartition):

    model = RoomOptionsMasterModel

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        self.req_type = obj.part_sub_category
        return super(RoomPartitionEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(RoomPartitionEditView, self).get_context_data(**kwargs)
        context['room_partition'] = self.get_object()
        context.update(kwargs)

        return context


@method_decorator(csrf_exempt, name='dispatch')
class DrillPatternMapView(View):

    def post(self, request, *args, **kwargs):
        ret_arr = [{"id": '', "text": "Select"}]
        request_data = json.loads(request.body)
        rnd = flat = False
        if request_data['type'] == 'rnd':
            rnd = True
        else:
            flat = True
        obj = CustomPartitionDrillMap.objects.filter(height__lte=request_data['height'],
                                                     depth__lte=request_data['depth'],
                                                     rnd=rnd, flat=flat,
                                                     mm22=request_data['is_22mm'], category_code='1031')
        for i in obj:
            ret_arr.append({"id": i.id, "text": i.description})

        return JsonResponse({"result": ret_arr}, status=200)

