from django.forms import formsets
from django.forms.formsets import formset_factory
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404,render
from django.views.generic import FormView ,RedirectView
from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from room_options.forms import SingleDoorForm
from COS.core.decorators import logged_user_view
from franchise.models import RoomModel
from room_options.models import RoomOptionsMasterModel,DoorSingleOpeningheightWidthMapModel
from room_options.conf import Description


@logged_user_view()
class SingleDoorView(FormView):
    
    form_class = SingleDoorForm
    
    def get_template_names(self):
        template_name = 'room_options/single_door.html'  
        return template_name

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(RoomModel, id=self.kwargs['room_id'], job__user=self.request.user)
        return super(SingleDoorView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:single-door',
                                                  kwargs={'room_id': self.room.id}
                                                )

    def get_context_data(self, **kwargs):
        
        context = super(SingleDoorView, self).get_context_data(**kwargs)
        context['room'] = self.room
        context['all_rooms'] = RoomModel.objects.filter(job__user=self.request.user).order_by('create_date')
        context['single_door'] = RoomOptionsMasterModel.objects.filter(room=self.room,description=Description.SINGLE_DOOR)
        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            context['order_items']=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
        return context

    def get_form_kwargs(self):
        '''update form args '''
        room = self.room
        data = super(SingleDoorView, self).get_form_kwargs()
        request = self.request
        data.update({'room': room,
                     'category': "STANDARD",
                     'description':Description.SINGLE_DOOR,
                     'request': request})
        return data

    def form_valid(self, form):
       
        form.save()
        messages.success(self.request, 'Single Door has been added')  
        return super(SingleDoorView, self).form_valid(form) 

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
def room_single_opening_data(request):
    context={}
    id=request.GET.get('opening_size_id')
    room_item=request.GET.get('room_item')
    if room_item:
      room_option_master=RoomOptionsMasterModel.objects.get(id=room_item)
      context['order_items']=DoorSingleOpeningheightWidthMapModel.objects.filter(height=room_option_master.height,width=room_option_master.width).first()
    
    context['openings'] = DoorSingleOpeningheightWidthMapModel.objects.filter(opening_size_id=id)
    return  render(request,'room_options/door_single_openings_dropdown.html',{"options": context})
                                         