import functools
import itertools

from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.models import RoomOptionsMasterModel, ToeKick
from room_options.conf import Description
# Create your views here.
from room_options.toe_kick_forms import ToeKickForm
from room_options.utils import RoomViewMixin

@is_classy_user_view()
class BaseToeKickView(FormView, RoomViewMixin):
    form_class = ToeKickForm
    template_name = './room_options/toe kicks/toe-kicks.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:toe-kick', kwargs={'room_id': self.kwargs['room_id']})

    def get_context_data(self, **kwargs):
        context = super(BaseToeKickView, self).get_context_data(**kwargs)
        context['toe_kicks'] = ToeKick.objects.filter(room=self.room)
        context['counter'] = functools.partial(next, itertools.count(1))
        return context

    def room_option_save(self, option, face):

        obj = option.toe_kick_form
        option.description = Description.TOE_KICK
        option.part_sub_category = "STANDARD"
        option.plywood = obj.plywood

        if face == 'Normal':
            option.height = obj.height
            option.width = float(obj.width) - 1.5

            option.depth = obj.depth if obj.depth > 0 else 1
            option.quantity = obj.quantity
            option.description2 = 'TKH-{}'.format(obj.height)

        if face == 'TK End Cap':
            option.height = obj.height
            option.width = 0.75
            option.depth = obj.depth
            option.quantity = obj.quantity
            option.description2 = 'TK End Cap'

        if face == 'TK Front/Back':
            option.height = obj.height
            option.width = float(obj.width) - 1.5
            option.depth = 0.75
            option.quantity = obj.quantity
            option.description2 = 'TK Front/Back'

        if face == 'Stringer':
            option.height = 0.75
            option.width = float(obj.width) - 1.5
            option.depth = 1.5
            option.quantity = obj.quantity
            option.description2 = 'Stringer'

        return option.save()

    def form_invalid(self, form):
        return super(BaseToeKickView, self).form_invalid(form)





@is_classy_user_view()
@logged_user_view()
class ToeKickView(BaseToeKickView):

    def dispatch(self, request, *args, **kwargs):
        return super(ToeKickView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.room = self.room
        obj.part_sub_category = "STANDARD"
        obj.save()

        self.room_option_save(RoomOptionsMasterModel(toe_kick_form=obj, room=self.room), 'Normal')

        if form.cleaned_data['end_caps']:
            self.room_option_save(RoomOptionsMasterModel(toe_kick_form=obj, room=self.room), 'TK End Cap')

        self.room_option_save(RoomOptionsMasterModel(toe_kick_form=obj, room=self.room), 'TK Front/Back')

        self.room_option_save(RoomOptionsMasterModel(toe_kick_form=obj, room=self.room), 'Stringer')

        return super(ToeKickView, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class ToeKickEditView(UpdateView, BaseToeKickView):
    model = ToeKick

    def dispatch(self, request, *args, **kwargs):

        return super(ToeKickEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ToeKickEditView, self).get_context_data(**kwargs)
        context['toe_kick'] = self.get_object()
        context.update(kwargs)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.room = self.room
        obj.part_sub_category = "STANDARD"
        obj.save()

        self.room_option_save(RoomOptionsMasterModel.objects.get(description2__contains="TKH-", toe_kick_form=obj,
                                                       room=self.room), 'Normal')

        if form.cleaned_data['end_caps']:
            try:
                end_cap = RoomOptionsMasterModel.objects.get(description2='TK End Cap', toe_kick_form=obj, room=self.room)
            except RoomOptionsMasterModel.DoesNotExist:
                end_cap = RoomOptionsMasterModel(toe_kick_form=obj, room=self.room)

            self.room_option_save(end_cap, 'TK End Cap')
        else:
            try:
                RoomOptionsMasterModel.objects.get(description2='TK End Cap', toe_kick_form=obj, room=self.room).delete()
            except RoomOptionsMasterModel.DoesNotExist:
                pass

        self.room_option_save(RoomOptionsMasterModel.objects.get(description2='TK Front/Back',
                                                     toe_kick_form=obj, room=self.room), 'TK Front/Back')

        self.room_option_save(RoomOptionsMasterModel.objects.get(description2='Stringer',
                                                     toe_kick_form=obj, room=self.room), 'Stringer')

        return super(ToeKickEditView, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class ToeKickDeleteView(RedirectView, RoomViewMixin):

    def get(self, *args, **kwargs):
        ToeKick.objects.get(id=self.kwargs['pk']).delete()
        RoomOptionsMasterModel.objects.filter(toe_kick_form__id=self.kwargs['pk']).delete()
        return HttpResponse(JsonResponse({'status': 200}))
