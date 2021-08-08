from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404,render
from django.views.generic import FormView ,RedirectView
from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from room_options.forms import PairDoorsForm
from COS.core.decorators import logged_user_view
from room_options.models import RoomOptionsMasterModel,DoorOpeningheightWidthMapModel
from room_options.conf import Description

from room_options.utils import RoomViewMixin


@logged_user_view()
class PairDoorsView(FormView, RoomViewMixin):
    
    form_class = PairDoorsForm
    
    def get_template_names(self):
        template_name = 'room_options/pair_doors.html'  
        return template_name

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:pair-doors',
                                    kwargs={'room_id': self.room.id}
                            )

    def get_context_data(self, **kwargs):
        
        context = super(PairDoorsView, self).get_context_data(**kwargs)
        context['pair_doors'] = RoomOptionsMasterModel.objects.filter(room=self.room,description=Description.PAIR_DOOR)
        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            context['order_items']=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
        return context

    def get_form_kwargs(self):
        '''update form args '''
        data = super(PairDoorsView, self).get_form_kwargs()
        room = self.room
        request = self.request
        data.update({'room': room,
                     'category': "STANDARD",
                     'description':Description.PAIR_DOOR,
                     'request': request})
        return data

    def form_valid(self, form):
       
        form.save()
        messages.success(self.request, 'Pair Door has been added')  
        return super(PairDoorsView, self).form_valid(form) 


class DoorsDeleteView(RedirectView):

    def get(self, *args, **kwargs):
        self.pk=self.request.GET.get('pk')
        try:
            user = self.request.user
            RoomOptionsMasterModel.objects.get(room__job__user=user, id=self.pk).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':204}))


@login_required
def room_opening_data(request):
    context={}
    id=request.GET.get('opening_size_id')
    room_item=request.GET.get('room_item')
    if room_item:
      room_option_master=RoomOptionsMasterModel.objects.get(id=room_item)
      context['order_items'] = DoorOpeningheightWidthMapModel.objects.filter(height=room_option_master.height,
                                                                           width=room_option_master.width).first()
    
    context['openings'] = DoorOpeningheightWidthMapModel.objects.filter(opening_size_id=id)
    return  render(request,'room_options/door_openigs_dropdown.html',{"options": context})
