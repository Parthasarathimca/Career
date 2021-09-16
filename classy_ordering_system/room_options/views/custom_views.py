import json

from django.views.generic import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from COS.core.decorators import logged_user_view
from inventory_options.models import BoardColor
from room_options.custom_forms import CustomForm
from room_options.models import RoomOptionsMasterModel
from room_options.conf import Description
# Create your views here.
from room_options.toe_kick_forms import ToeKickForm
from room_options.utils import RoomViewMixin, create_lookup, create_material_lookup, create_color_lookup
from room_options.conf import Description


class CustomBaseView(FormView, RoomViewMixin):
    form_class = CustomForm
    template_name = './room_options/custom/custom.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:custom', kwargs={'room_id': self.kwargs['room_id']})

    def get_context_data(self, **kwargs):

        context = super(CustomBaseView, self).get_context_data(**kwargs)
        context['customs'] = RoomOptionsMasterModel.objects.filter(room_id=self.kwargs['room_id'], description=Description.CUSTOM)
        context['lookup'] = json.dumps(create_lookup(), indent=4)
        context['mat_lookup'] = json.dumps(create_material_lookup(), indent=4)
        context['color_lookup'] = json.dumps(create_color_lookup(), indent=4)

        return context

    def form_invalid(self, form):
        print(form.errors)
        return super(CustomBaseView, self).form_invalid(form)

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.description2 = "Cx-{0}".format(form.cleaned_data['category'].cat_name)
        obj.description = Description.CUSTOM
        obj.room = self.room
        obj.part_sub_category = "CUSTOM"
        print(obj)
        obj.save()
        return super(CustomBaseView, self).form_valid(form)


@logged_user_view()
class CustomView(CustomBaseView):

    def get_initial(self):
        initial = super(CustomView, self).get_initial()
        initial ['quantity'] = 0
        return initial

    def dispatch(self, request, *args, **kwargs):
        return super(CustomView, self).dispatch(request, *args, **kwargs)


@logged_user_view()
class CustomEditView(UpdateView, CustomBaseView):
    model = RoomOptionsMasterModel

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        return super(CustomEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(CustomEditView, self).get_context_data(**kwargs)
        context['custom'] = self.get_object()
        context.update(kwargs)
        return context

