from django.views.generic import FormView 
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.views.generic import RedirectView, UpdateView
from room_options.forms import AdjShelveForm
from room_options.models import RoomOptionsMasterModel
from franchise.models import RoomModel, JobModel
from room_options.conf import Description
from COS.core.decorators import logged_user_view
from room_options.utils import RoomViewMixin


@logged_user_view()
class RoomADJShelfView(FormView, RoomViewMixin):

    form_class = AdjShelveForm

    def get_template_names(self):
        type = self.request.GET.get('type')
        if  type == 'CUSTOM':
            template_name = "room_options/adj_shelf/custom_adj_shelf.html"
        elif type == '1_IN_KD':
            template_name = "room_options/adj_shelf/1_in_adj_shelf.html"
        elif type == 'SHOE_SHELF':
            template_name = "room_options/adj_shelf/shoe_shelf.html"            
        else:
            template_name = "room_options/adj_shelf/create_adj_shelf.html"

        return template_name

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == "POST":
            self.selected_room = self.request.POST.get('room_id')
        else:
            self.selected_room = None        
        return super(RoomADJShelfView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RoomADJShelfView, self).get_initial()
        details = {}
        try:
            option = RoomOptionsMasterModel.objects.get(room__job__user=self.request.user, pk=self.kwargs['id'])
            details={
                'id': option.id,
                'room' : self.selected_room,
                'notes'  : option.notes,
                'adj_shelf_edge': option.adj_shelf_edge,
                'adj_insert_backing': option.adj_insert_backing,
                'mat_type' : option.mat_type,
                'part_sub_category' : option.part_sub_category,
                'quantity' : option.quantity,
                'depth': option.depth,
                'width': option.width,
                'adj_exposed_end': option.adj_exposed_end
            }  
            print(details, "detailsdetailsdetailsdetailsdetails")      
        except:
            pass

        initial.update(details)
        return initial

    def get_form_kwargs(self):
        '''update form args '''
        data = super(RoomADJShelfView, self).get_form_kwargs()
        type = self.request.GET.get('type')
        request = self.request
        if type == "1_IN_KD":
            option_description = Description.IN_ADJ_SHELF
        elif type == "SHOE_SHELF":
            option_description = Description.SHOE_SHELF            
        else:
            option_description = Description.ADJ_SHELF

        category = self.request.GET.get('type')


        # try:
        #     id = self.kwargs['id']
        # except:
        #     id = None

        data.update({
                     'room': self.room,
                     'category': category,
                     'request': request,
                     'description': option_description,
                    })
        return data

    def get_context_data(self, **kwargs):
        context = super(RoomADJShelfView, self).get_context_data(**kwargs)

        shelves = RoomOptionsMasterModel.objects.filter(room__job=self.kwargs['room_id'])
        try:
            id = self.room.id
            context['room_detail'] = RoomOptionsMasterModel.objects.get(id=id).room
        except:
            id = None
        try:
            id = self.kwargs['id']
            context['room_detail'] = RoomOptionsMasterModel.objects.get(id=id).room
        except:
            id = None
        # context['rooms'] = RoomModel.objects.filter(job=self.kwargs['room_id'])

        # if self.selected_room:
        #     context['selected_room'] = RoomModel.objects.get(id = self.selected_room)
        # else:
        #     context['selected_room'] = context['rooms'].last()
        context['adj_shelves_standard'] = shelves.filter(description=Description.ADJ_SHELF, part_sub_category="STANDARD").order_by('create_date')
        context['adj_shelves_custom'] = shelves.filter(description=Description.ADJ_SHELF, part_sub_category="CUSTOM").order_by('create_date')
        context['adj_shelves_1_in_Kd'] = shelves.filter(description=Description.IN_ADJ_SHELF).order_by('create_date')
        context['adj_shelves_shoe'] = shelves.filter(description=Description.SHOE_SHELF).order_by('create_date')
        # context['job'] = JobModel.objects.get(id=self.kwargs['room_id'])
        return context

    def get_success_url(self, *args, **kwargs):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:room-adj-shelf', kwargs={
            'room_id' : self.kwargs['room_id']
            } ) + '?type=' + type 
        else:
            return reverse_lazy('room_options:room-adj-shelf', kwargs={
            'room_id' : self.kwargs['room_id']
            } )

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Partition has been added')
        return super(RoomADJShelfView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors, "errors=============")
        messages.success(self.request, 'Partition has been added')
        return super(RoomADJShelfView, self).form_invalid(form)