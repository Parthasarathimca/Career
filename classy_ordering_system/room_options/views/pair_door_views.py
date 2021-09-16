from room_options.models.partition_models.room_map_models import DoorOpeningSizeMapModel
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404,render
from django.views.generic import FormView ,RedirectView
from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from room_options.forms import PairDoorsForm
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.models import RoomOptionsMasterModel,DoorOpeningheightWidthMapModel
from room_options.conf import Description

from room_options.utils import RoomViewMixin

@is_classy_user_view()
@logged_user_view()
class PairDoorsView(FormView, RoomViewMixin):
    
    form_class = PairDoorsForm
    
    def get_template_names(self):
        type= self.request.GET.get('type')
        if type == 'CUSTOM':
            template_name = 'room_options/doors/pair_door_custom.html'  
        else:template_name = 'room_options/doors/pair_doors.html'  
        return template_name

    def get_success_url(self, *args, **kwargs):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:pair-doors',
                                    kwargs={'room_id': self.room.id})+ '?type=' + type 
                            
        else:
            return reverse_lazy('room_options:pair-doors',
                                    kwargs={'room_id': self.room.id}
                            )

    def get_context_data(self, **kwargs):
        
        context = super(PairDoorsView, self).get_context_data(**kwargs)
        context['pair_doors'] = RoomOptionsMasterModel.objects.filter(room=self.room,description=Description.PAIR_DOOR)
        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            order_items=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
            context['order_items']=order_items
            context['is_18_hole_doors_obj']=DoorOpeningheightWidthMapModel.objects.filter(height=order_items.height,
                                                                           width=order_items.width).first()
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

@is_classy_user_view()
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
    type=request.GET.get('type')
    is_18_hole_doors=request.GET.get('is_18_hole_doors')
    is_18_hole_doors= True if is_18_hole_doors=='true' else False 
    room_item=request.GET.get('room_item')
    if room_item:
      room_option_master=RoomOptionsMasterModel.objects.get(id=room_item)
      
      if type=='HEIGHT':
          context['order_items'] = DoorOpeningheightWidthMapModel.objects.filter(height=room_option_master.height,
                                                                        width=room_option_master.width).first()
      else:
           context['order_items'] = DoorOpeningSizeMapModel.objects.filter(id=room_option_master.door_opening_size_id).first()
           
    if type=='HEIGHT':
        context['openings'] = DoorOpeningheightWidthMapModel.objects.filter(opening_size_id=id,is_18_hole_doors=is_18_hole_doors)
    else:
        context['opeing_sizes'] = DoorOpeningSizeMapModel.objects.filter(is_18_hole_doors=is_18_hole_doors)
                
    context['type']=type
    return  render(request,'room_options/doors/door_openigs_dropdown.html',{"options": context})
