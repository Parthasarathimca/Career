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
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.utils import RoomViewMixin
from room_options.models import *

@is_classy_user_view()
class RoomADJShelf(FormView, RoomViewMixin):

    form_class = AdjShelveForm
    def get_initial(self):
        initial = super(RoomADJShelf, self).get_initial()
        details = {'mat_type':1}
        initial.update(details)
        return initial

    def get_template_for_display(self, adj_shelf_type):
        if  adj_shelf_type == 'CUSTOM':
            template_name = "room_options/adj_shelf/custom_adj_shelf.html"
        elif adj_shelf_type == '1_IN_ADJ':
            template_name = "room_options/adj_shelf/1_in_adj_shelf.html"
        elif adj_shelf_type == 'SHOE_SHELF':
            template_name = "room_options/adj_shelf/shoe_shelf.html"            
        else:
            template_name = "room_options/adj_shelf/create_adj_shelf.html"

        return template_name


    def get_form_kwargs(self):
        '''update form args '''
        data = super(RoomADJShelf, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': Description.ADJ_SHELF})
        return data

    def get_context_data(self, **kwargs):
        context = super(RoomADJShelf, self).get_context_data(**kwargs)
        context['adj_shelves'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.ADJ_SHELF)
        return context

    def get_success_url(self, *args, **kwargs):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:room-adj-shelf', kwargs={
            'room_id' : self.kwargs['room_id']}) + '?type=' + type 
        else:
            return reverse_lazy('room_options:room-adj-shelf', kwargs={
            'room_id' : self.kwargs['room_id']})
        
    def form_valid(self, form):
        return super(RoomADJShelf, self).form_valid(form)

    def form_valid_save(self, form, type):
        id = self.kwargs.get('room_id')
        mat_type = RoomModel.objects.get(id=id).dd_mat_type
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.ADJ_SHELF
        if mat_type:
            if type == "1_IN_ADJ":
                obj.height = 1
            else:
                obj.height = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        obj.category = type
        obj.save()
        return super(RoomADJShelf, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class RoomADJShelfView(RoomADJShelf):
    
    form_class = AdjShelveForm

    def get_template_names(self):
        return self.get_template_for_display(self.request.GET.get('type'))

    def get_initial(self):
        initial = super(RoomADJShelfView, self).get_initial()
        details = {}
        try:
            option = RoomOptionsMasterModel.objects.get(room__job__user=self.request.user, pk=self.kwargs['id'])
            print(option)
            details={
                'depth': option.depth,
                'width': option.width,
                'adj_shelf_edge': option.adj_shelf_edge,
                'adj_insert_backing': option.adj_insert_backing,
                'mat_type' : option.mat_type,
                'part_sub_category' : option.part_sub_category,
                'quantity' : option.quantity,
                'notes': option.notes,
                'adj_exposed_end': option.adj_exposed_end
            }        
        except:
            pass

        initial.update(details)
        return initial

    def form_valid(self, form):
        return self.form_valid_save(form, self.request.GET.get('type'))

@is_classy_user_view()
class RoomAdjShelfEditView(UpdateView, RoomADJShelf):

    model = RoomOptionsMasterModel

    def get_template_names(self):
        obj = self.get_object()
        return self.get_template_for_display(obj.part_sub_category)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(RoomAdjShelfEditView, self).get_context_data(**kwargs)
        context['room_adj'] = self.get_object()
        context.update(kwargs)

        return context


