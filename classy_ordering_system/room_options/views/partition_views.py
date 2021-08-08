from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import FormView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from room_options.forms import RoomPartitionForm
from COS.core.decorators import logged_user_view
from room_options.models import RoomOptionsMasterModel
from room_options.conf import Description
# Create your views here.
from room_options.utils import RoomViewMixin

class RoomPartition(FormView, RoomViewMixin):
    form_class = RoomPartitionForm

    def get_template_for_display(self, partition_type):
        if partition_type == 'CUSTOM':
            template_name = 'room_options/partitions/custom_partition.html'
        else:
            template_name = 'room_options/partitions/create_partition.html'
        return template_name

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:room-partition', kwargs={'room_id': self.kwargs['room_id']})

    def get_context_data(self, **kwargs):
        context = super(RoomPartition, self).get_context_data(**kwargs)
        context['partitions'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.PARTITION)
        return context

    def get_form_kwargs(self):
        '''update form args '''
        data = super(RoomPartition, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': Description.PARTITION})
        return data

    def form_invalid(self, form):
        return super(RoomPartition, self).form_invalid(form)

    def form_valid_save(self, form, type):
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.PARTITION
        obj.category = type
        obj.save()
        messages.success(self.request, 'Partition has been added')
        return super(RoomPartition, self).form_valid(form)


@logged_user_view()
class RoomPartitionView(RoomPartition):
    
    form_class = RoomPartitionForm
    req_type = "Standard"

    def get_template_names(self):
        return self.get_template_for_display(self.request.GET.get('type'))

    def get_initial(self):
        initial = super(RoomPartitionView, self).get_initial()
        details = {}
        try:
            option = RoomOptionsMasterModel.objects.get(room__job__user=self.request.user, pk=self.kwargs['id'])
            details={
                        'ed_type': option.ed_type,
                        'notes': option.notes,
                        'drill_pattern_width' : option.drill_pattern_width,
                        'drill_pattern_depth' : option.drill_pattern_depth,
                        'drill_pattern_height' : float(option.drill_pattern_height) if option.drill_pattern_height else None,
                        'mat_type' : option.mat_type,
                        'drill_pattern_left' : option.drill_pattern_left,
                        'drill_pattern_right' : option.drill_pattern_right,
                        'part_sub_category' : option.part_sub_category,
                        'quantity' : option.quantity,
                        'edge_profile' : option.edge_profile,
                        'left_3rd_line_hole' : option.left_3rd_line_hole,
                        'right_3rd_line_hole' : option.right_3rd_line_hole,
                        'dog_eared' : option.dog_eared
                        }        
        except:
            pass

        initial.update(details)
        return initial

    def form_valid(self, form):
        return self.form_valid_save(form, self.request.GET.get('type'))




class RoomPartitionEditView(UpdateView, RoomPartition):

    model = RoomOptionsMasterModel

    def get_template_names(self):
        obj = self.get_object()
        return self.get_template_for_display(obj.part_sub_category)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(RoomPartitionEditView, self).get_context_data(**kwargs)
        context['room_partition'] = self.get_object()
        context.update(kwargs)

        return context


