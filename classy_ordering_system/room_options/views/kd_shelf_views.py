from django.views.generic import FormView 
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.views.generic import RedirectView, UpdateView
from room_options.forms import RoomKdShelfForm
from room_options.models import RoomOptionsMasterModel
from franchise.models import RoomModel
from room_options.conf import Description
from room_options.utils import RoomViewMixin
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.models import *

@is_classy_user_view()
class RoomKdShelf(FormView, RoomViewMixin):
    form_class = RoomKdShelfForm
    def get_initial(self):
        initial = super(RoomKdShelf, self).get_initial()
        details = {'mat_type':1}
        initial.update(details)
        return initial

    
    def get_template_for_display(self, kd_shelf_type):
        if kd_shelf_type == 'CUSTOM':
            template_name = "room_options/kd_shelf/custom_kd_shelf.html"
        elif kd_shelf_type == '1_IN_KD':
            template_name = "room_options/kd_shelf/1_in_kd_shelf.html"
        else:
            template_name = "room_options/kd_shelf/create_kd_shelf.html"

        return template_name

    def get_form_kwargs(self):
        '''update form args '''
        data = super(RoomKdShelf, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': Description.KD_SHELF})
        return data

    def get_context_data(self, **kwargs):
        context = super(RoomKdShelf, self).get_context_data(**kwargs)
        context['kd_shelves'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.KD_SHELF)
        context['rooms'] = RoomModel.objects.filter(job=self.kwargs['room_id'])
        return context

    def get_success_url(self, *args, **kwargs):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:room-kd-shelf', kwargs={
            'room_id' : self.kwargs['room_id']}) + '?type=' + type 
        else:
            return reverse_lazy('room_options:room-kd-shelf', kwargs={
            'room_id' : self.kwargs['room_id']})
       
    def form_valid(self, form):
        return super(RoomKdShelf, self).form_valid(form)

    def form_valid_save(self, form, type):
        id = self.kwargs.get('room_id')
        mat_type = RoomModel.objects.get(id=id).dd_mat_type
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.KD_SHELF
        if mat_type:
            if type == "1_IN_KD":
                obj.height = 1
            else:
                obj.height = RoomMatTypeModelMap.objects.get(id=mat_type.id).size
        obj.category = type
        obj.save()
        return super(RoomKdShelf, self).form_valid(form)

    def form_invalid(self, form):
        print(form.data, "form")
        print(form.errors, "caught errors in form")
        return super(RoomKdShelf, self).form_invalid(form)


@is_classy_user_view()
@logged_user_view()
class RoomKdShelfView(RoomKdShelf):
    
    form_class = RoomKdShelfForm

    def get_template_names(self):
        return self.get_template_for_display(self.request.GET.get('type'))

    def get_initial(self):
        initial = super(RoomKdShelfView, self).get_initial()
        details = {}
        try:
            option = RoomOptionsMasterModel.objects.get(room__job__user=self.request.user, pk=self.kwargs['id'])
            print(option)
            details={
                'part_sub_category' : option.part_sub_category,
                'mat_type': option.mat_type,
                'insert_backing': option.insert_backing,
                'depth': option.depth,
                'width': option.width,
                'kd_shelf_edge': option.kd_shelf_edge,
                'insert_backing': option.insert_backing,
                'mat_type' : option.mat_type,
                'part_sub_category' : option.part_sub_category,
                'notes': option.notes,
                
        }        
        except:
            pass

        initial.update(details)
        return initial

    def form_valid(self, form):
        return self.form_valid_save(form, self.request.GET.get('type'))

@is_classy_user_view()
class RoomKdShelfEditView(UpdateView, RoomKdShelf):

    model = RoomOptionsMasterModel

    def get_template_names(self):
        obj = self.get_object()
        return self.get_template_for_display(obj.part_sub_category)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(RoomKdShelfEditView, self).get_context_data(**kwargs)
        context['room_kd'] = self.get_object()
        context.update(kwargs)

        return context

@is_classy_user_view()    
class DeleteRoomOptionView(RedirectView):
    
    def get(self, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        try:
            user = self.request.user
            RoomOptionsMasterModel.objects.get(room__job__user=user, id=kwargs['pk']).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':200}))
