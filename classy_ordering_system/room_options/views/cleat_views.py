from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import FormView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from room_options.cleat_forms import CleatForm
from room_options.forms import RoomPartitionForm
from COS.core.decorators import logged_user_view
from room_options.models import RoomOptionsMasterModel
from room_options.conf import Description
# Create your views here.
from room_options.utils import RoomViewMixin


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
        return reverse_lazy('room_options:cleat', kwargs={'room_id': self.kwargs['room_id']})

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
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.CLEAT
        obj.part_sub_category = self.req_type
        obj.save()
        messages.success(self.request, 'Partition has been added')
        return super(BaseCleatView, self).form_valid(form)


@logged_user_view()
class CleatView(BaseCleatView):

    def get_initial(self):
        if self.req_type == "STANDARD":
            return {'width': 0}
        elif self.req_type == "CUSTOM":
            return {'height': 3.64}
        elif self.req_type == "COVER":
            return {'width': 97, 'height': 3.68}
        return super(CleatView, self).get_initial()

    def dispatch(self, request, *args, **kwargs):
        self.req_type = self.request.GET.get('type', "STANDARD")
        return super(BaseCleatView, self).dispatch(request, *args, **kwargs)


class CleatEditView(UpdateView, BaseCleatView):
    model = RoomOptionsMasterModel

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        self.req_type = obj.part_sub_category
        return super(BaseCleatView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(CleatEditView, self).get_context_data(**kwargs)
        context['cleat'] = self.get_object()
        context.update(kwargs)
        return context


