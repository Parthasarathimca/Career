from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import FormView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from room_options.cleat_forms import CleatForm
from room_options.forms import RoomPartitionForm
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.models import RoomOptionsMasterModel
from room_options.conf import Description
# Create your views here.
from room_options.utils import RoomViewMixin
from room_options.models import *

@is_classy_user_view()
class BaseCleatView(FormView, RoomViewMixin):
    form_class = CleatForm
    req_type = "STANDARD"

    def get_template_names(self):
        if self.req_type == 'CUSTOM':
            template_name = 'room_options/cleats/custom.html'
        elif self.req_type == 'COVER':
            template_name = 'room_options/cleats/cover.html'
        else:
            template_name = 'room_options/cleats/standard.html'
        return template_name

    def get_success_url(self, *args, **kwargs):
        ret_url = reverse_lazy('room_options:cleat', kwargs={'room_id': self.kwargs['room_id']})
        if self.req_type != "STANDARD":
            ret_url = ret_url + "?type={}".format(self.req_type)
        return ret_url

    def get_context_data(self, **kwargs):
        context = super(BaseCleatView, self).get_context_data(**kwargs)
        context['cleats'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.CLEAT)
        context['form_type'] = self.req_type
        return context

    def get_form_kwargs(self):
        data = super(BaseCleatView, self).get_form_kwargs()
        data.update({'form_type': self.req_type})
        return data

    def form_invalid(self, form):
        return super(BaseCleatView, self).form_invalid(form)

    def form_valid(self, form):
        id = self.kwargs.get('room_id')
        mat_type = RoomModel.objects.get(id=id).dd_mat_type
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.CLEAT
        obj.part_sub_category = self.req_type
        if mat_type:
            obj.depth = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        obj.save()
        messages.success(self.request, 'Partition has been added')
        return super(BaseCleatView, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class CleatView(BaseCleatView):

    def get_initial(self):
        initial = super(CleatView, self).get_initial()
        initial ['mat_type'] = 1
        if self.req_type == "STANDARD":
            initial['width'] = 0
            initial['height'] = 3.64
        elif self.req_type == "CUSTOM":
            initial['height'] = 3.64
        elif self.req_type == "COVER":
            initial['width'] = 97
            initial['height'] = 3.68
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.req_type = self.request.GET.get('type', "STANDARD")
        return super(CleatView, self).dispatch(request, *args, **kwargs)


class CleatEditView(UpdateView, BaseCleatView):
    model = RoomOptionsMasterModel

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        self.req_type = obj.part_sub_category
        return super(CleatEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(CleatEditView, self).get_context_data(**kwargs)
        context['cleat'] = self.get_object()
        context.update(kwargs)
        return context


