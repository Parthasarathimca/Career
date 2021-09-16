from django.http import JsonResponse, HttpResponse, request
from django.views.generic import FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404,render
from django.contrib import messages
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.conf import Description
from room_options.models import RoomOptionsMasterModel
from room_options.models import RoomOptionsMasterModel
from room_options.models.LTI_doors_models.LTI_models import LTIDrawerSizeMapModel,DoorSizeMapModel
from room_options.forms import LTIDoorsForm
from room_options.utils import RoomViewMixin
from django.contrib.auth.decorators import login_required



@logged_user_view()
@is_classy_user_view()
class LTIDoorsView(FormView, RoomViewMixin):

    form_class = LTIDoorsForm

    def get_template_names(self):
        template_name='room_options/LTI_doors/LTI_doors.html'
        if self.request.GET.get('type') == "LTI_DOORS":
            template_name = 'room_options/LTI_doors/LTI_doors.html'
        elif self.request.GET.get('type') =="LTI_DRAWERS":
            template_name = 'room_options/LTI_doors/LTI_drawers.html'
        
        return template_name
    def get_form_kwargs(self):
        '''update form args '''
        data = super(LTIDoorsView, self).get_form_kwargs()
        room = self.room
        request = self.request
        data.update({'room': room,
                     'request': request,
                     'description':Description.LTI_DOORS})
        return data


    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        
        context = super(LTIDoorsView, self).get_context_data(**kwargs)
        context['lti_doors'] = RoomOptionsMasterModel.objects.filter(room=self.room,
                                                                               description=Description.LTI_DOORS)

        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            context['order_items']=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
            
        context['lti_door_size_custom']=DoorSizeMapModel.objects.get(description='Custom').id  if DoorSizeMapModel.objects.filter(description='Custom') else None                                     
        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            context['order_items']=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
        context.update(kwargs)
        return context

    def get_success_url(self):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:LTI-doors', kwargs={
            'room_id' : self.kwargs['room_id']}) + '?type=' + type 
        else:
            return reverse_lazy('room_options:LTI-doors', kwargs={
            'room_id' : self.kwargs['room_id']})
     
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Problem saving LTI-doors')
        return super(LTIDoorsView, self).form_invalid(form)

    def form_valid(self, form):
        # obj = form.save()
        # obj.description = Description.l_SHELF
        # obj.room = self.room
        form.save()
        #messages.success(self.request, 'Drawer box has been added')
        return super(LTIDoorsView, self).form_valid(form)


@logged_user_view()
@is_classy_user_view()
class LShelfDeleteView(RedirectView, RoomViewMixin):

    def get(self, *args, **kwargs):
        self.pk=self.request.GET.get('pk')
        RoomOptionsMasterModel.objects.get(id=self.pk).delete()
        return HttpResponse(JsonResponse({'status': 204}))



@login_required

def load_lti_dopdowns(request):
    context={}
    type=request.GET.get('type')
    if type=='DRAWER_SIZE':
        is_routed=request.GET.get('is_routed')
        is_routed= False if is_routed=='true' else True
        context['drawer_size'] = LTIDrawerSizeMapModel.objects.exclude(is_routed=is_routed)
    else:
        is_standard=request.GET.get('is_standrard')
        is_standard= True if is_standard =='true' else False
        context['door_size'] = DoorSizeMapModel.objects.filter(is_standard=is_standard)
        

    context['type']=type
    return  render(request,'room_options/LTI_doors/drawer_size_dropdowns.html',{"options": context})
