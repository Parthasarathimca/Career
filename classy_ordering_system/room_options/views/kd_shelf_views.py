from django.views.generic import FormView 
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.views.generic import RedirectView, UpdateView
from room_options.forms import RoomPartitionForm, RoomKdShelfForm
from room_options.models import RoomOptionsMasterModel
from franchise.models import RoomModel, JobModel
from room_options.conf import Description
from room_options.utils import RoomViewMixin



class RoomKDShelfView(FormView, RoomViewMixin):
    form_class = RoomKdShelfForm

    def get_template_names(self):
        type = self.request.GET.get('type')
        if type == 'CUSTOM':
            template_name = "room_options/kd_shelf/custom_kd_shelf.html"
        elif type == '1_IN_KD':
            template_name = "room_options/kd_shelf/1_in_kd_shelf.html"
        else:
            template_name = "room_options/kd_shelf/create_kd_shelf.html"

        return template_name

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == "POST":
            self.selected_room = self.kwargs['room_id']
        else:
            self.selected_room = None
        return super(RoomKDShelfView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RoomKDShelfView, self).get_initial()
        self.room = self.room
        details = {}
        try:
            if self.kwargs.get('id'):
                option = RoomOptionsMasterModel.objects.get(room__job__user=self.request.user, pk=self.kwargs['id'])
                self.description = option.description
                details={
                    'id': option.id,
                    'room' : self.selected_room,
                    'notes'  : option.notes,
                    'description': option.description,
                    'part_sub_category' : option.part_sub_category,
                    'quantity' : option.quantity,
                    'kd_shelf_edge' : option.kd_shelf_edge,
                    'part_sub_category' : option.part_sub_category,
                    'mat_type': option.mat_type,
                    'insert_backing': option.insert_backing,
                    'depth': option.depth,
                    'width': option.width
                } 

            else:
                pass
        except Exception as e:
            print(str(e), "exception in initial data")

        initial.update(details)
        return initial

    def get_form_kwargs(self):
        '''update form args '''
        data = super(RoomKDShelfView, self).get_form_kwargs()
        type = self.request.GET.get('type')
        print(self.request.POST,"request data--------------")
        request = self.request
        if type == "1_IN_KD":
            option_description = Description.IN_KD_SHELF
        elif type == "CUSTOM":
            option_description = Description.CUSTOM_SHELF
        else:
            option_description = Description.KD_SHELF
        if type: 
            category = self.request.GET.get('type')
        else:
            category = 'STANDARD'

        data.update({
            'room': self.room,
            'category': category,
            'request': request,
            'description': option_description,
        })
        return data

    def get_context_data(self, **kwargs):
        context = super(RoomKDShelfView, self).get_context_data(**kwargs)
        shelves = RoomOptionsMasterModel.objects.filter(room=self.room)
        try:
            id = self.room.id
            context['room_detail'] = RoomOptionsMasterModel.objects.get(id=id).room
        except:
            id = None

        context['rooms'] = RoomModel.objects.filter(job=self.kwargs['room_id'])
        context['kd_shelves_standard'] = shelves.filter(description=Description.KD_SHELF, part_sub_category="STANDARD").order_by('create_date')
        context['kd_shelves_custom'] = shelves.filter(description=Description.CUSTOM_SHELF, part_sub_category="CUSTOM").order_by('create_date')
        context['kd_shelves_1_in_Kd'] = shelves.filter(description=Description.IN_KD_SHELF).order_by('create_date')
        return context

    def get_success_url(self, *args, **kwargs):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:room-kd-shelf', kwargs={
                'room_id': self.kwargs['room_id']
                }) + '?type=' + type 
        else:
            return reverse_lazy('room_options:room-kd-shelf', kwargs={
                'room_id': self.kwargs['room_id']
                }) + '?type=' + 'STANDARD' 


    def form_valid(self, form):
        form.save()
        return super(RoomKDShelfView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors, "errors-----------------")
        form.save()
        return super(RoomKDShelfView, self).form_invalid(form)

    
class DeleteRoomOptionView(RedirectView):
    
    def get(self, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        try:
            user = self.request.user
            RoomOptionsMasterModel.objects.get(room__job__user=user, id=kwargs['pk']).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':200}))
