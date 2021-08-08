from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic.base import ContextMixin

from franchise.models import RoomModel


class RoomViewMixin(ContextMixin):
    room = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.room = RoomModel.objects.get(pk=self.kwargs['room_id'])
        except RoomModel.DoesNotExist:
            raise ObjectDoesNotExist
        if self.room.job.user != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.room:
            context['room'] = self.room
        context['all_rooms'] = self.room.job.job_room.all()
        context.update(kwargs)
        return super().get_context_data(**context)
