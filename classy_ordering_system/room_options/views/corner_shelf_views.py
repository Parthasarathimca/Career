from django.http import JsonResponse, HttpResponse
from django.views.generic import FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.conf import Description
from room_options.models import RoomOptionsMasterModel
from room_options.forms import CornerSelfForm
from room_options.utils import RoomViewMixin

@is_classy_user_view()
@logged_user_view()
class CornerShelfView(FormView, RoomViewMixin):

    form_class = CornerSelfForm

    def get_template_names(self):
        template_name = 'room_options/corner_shelf/corner_shelf.html'
        return template_name
    def get_form_kwargs(self):
        '''update form args '''
        data = super(CornerShelfView, self).get_form_kwargs()
        room = self.room
        request = self.request
        data.update({'room': room,
                     'request': request,
                     'description':Description.CORNER_SHELF})
        return data


    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        
        context = super(CornerShelfView, self).get_context_data(**kwargs)
        context['corner_shelf'] = RoomOptionsMasterModel.objects.filter(room=self.room,
                                                                               description=Description.CORNER_SHELF)
                                                      
        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            context['order_items']=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
        context.update(kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('room_options:corner-shelf',
                            kwargs={'room_id': self.room.id}
                            )

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Problem saving corner-Shelf')
        return super(CornerShelfView, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(CornerShelfView, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class CornorShelfDeleteView(RedirectView, RoomViewMixin):

    def get(self, *args, **kwargs):
        self.pk=self.request.GET.get('pk')
        RoomOptionsMasterModel.objects.get(id=self.pk).delete()
        return HttpResponse(JsonResponse({'status': 204}))
