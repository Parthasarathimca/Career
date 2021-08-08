from django.views.generic import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from COS.core.decorators import logged_user_view
from room_options.models import RoomOptionsMasterModel
from room_options.conf import Description
# Create your views here.
from room_options.toe_kick_forms import ToeKickForm
from room_options.utils import RoomViewMixin


class BaseToeKickView(FormView, RoomViewMixin):
    form_class = ToeKickForm
    template_name = './room_options/toe kicks/toe-kicks.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:toe-kick', kwargs={'room_id': self.kwargs['room_id']})

    def get_context_data(self, **kwargs):
        context = super(BaseToeKickView, self).get_context_data(**kwargs)
        context['toe_kicks'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.TOE_KICK)
        return context

    def form_invalid(self, form):

        return super(BaseToeKickView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.TOE_KICK
        obj.save()

        messages.success(self.request, 'Toe Kick has been added')
        return super(BaseToeKickView, self).form_valid(form)


@logged_user_view()
class ToeKickView(BaseToeKickView):

    def dispatch(self, request, *args, **kwargs):
        return super(ToeKickView, self).dispatch(request, *args, **kwargs)


class ToeKickEditView(UpdateView, BaseToeKickView):
    model = RoomOptionsMasterModel

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        return super(ToeKickEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ToeKickEditView, self).get_context_data(**kwargs)
        context['toe_kick'] = self.get_object()
        context.update(kwargs)
        return context

