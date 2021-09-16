from django.http import JsonResponse, HttpResponse, request
from django.views.generic import FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.conf import Description
from room_options.models import RoomOptionsMasterModel
from room_options.forms import TopSelfForm
from room_options.utils import RoomViewMixin

@is_classy_user_view()
@logged_user_view()
class TopShelfView(FormView, RoomViewMixin):

    form_class =TopSelfForm

    def get_template_names(self):
        if self.request.GET.get('type') == "STANDARD":
            template_name = 'room_options/top_shelf/top_shelf.html'
        elif self.request.GET.get('type') =="CUSTOM":
            template_name = 'room_options/top_shelf/custom_top_shelf.html'
        elif self.request.GET.get('type')=="CUSTOM_COUNTER_TOP":
            template_name = 'room_options/top_shelf/custom_counter_top.html'
        elif self.request.GET.get('type')=="COUNTER_TOP":
            template_name = 'room_options/top_shelf/counter_top.html'   
        else: template_name = 'room_options/top_shelf/top_shelf.html'
        return template_name

    def get_form_kwargs(self):
        '''update form args '''
        data = super().get_form_kwargs()
        room = self.room
        request = self.request
        data.update({'room': room,
                     'request': request,
                     'description':Description.TOP_SHELF})

        return data


    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        
        context = super().get_context_data(**kwargs)
        context['top_shelf'] = RoomOptionsMasterModel.objects.filter(room=self.room,
                                                                               description=Description.TOP_SHELF)
                                                      
        if self.request.GET.get('room_item'):
            self.room_item_id=self.request.GET.get('room_item')
            context['order_items']=RoomOptionsMasterModel.objects.get(id=self.room_item_id)
        if self.request.GET.get('type')=='COUNTER_TOP' and self.request.GET.get('room_item'):
            width=str(context['order_items'].width)
            str_width=width.split('.')[0]
            context['order_items'].width=str_width+' X '+str(context['order_items'].depth)
        context.update(kwargs)
        return context
       
        
    def get_success_url(self):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:top-shelf', kwargs={
            'room_id' : self.kwargs['room_id']}) + '?type=' + type 
        else:
            return reverse_lazy('room_options:top-shelf', kwargs={
            'room_id' : self.kwargs['room_id']})
     
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Problem saving Top-Shelf')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@is_classy_user_view()
@logged_user_view()
class TopShelfDeleteView(RedirectView, RoomViewMixin):

    def get(self, *args, **kwargs):
        self.pk=self.request.GET.get('pk')
        RoomOptionsMasterModel.objects.get(id=self.pk).delete()
        return HttpResponse(JsonResponse({'status': 204}))
