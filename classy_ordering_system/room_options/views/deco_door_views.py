from django.views.generic import FormView, View,RedirectView, UpdateView
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.views.generic import RedirectView, UpdateView
from room_options.forms import WoodDoorsForm
from room_options.models import RoomOptionsMasterModel
from franchise.models import RoomModel, JobModel
from room_options.conf import Description
from COS.core.decorators import logged_user_view, is_classy_user_view
from room_options.utils import RoomViewMixin
from room_options.models.wood_door_models.main_models import *
import json
@is_classy_user_view()
class DecoDoor(FormView, RoomViewMixin):

    form_class = WoodDoorsForm

    def get_template_for_display(self, deco_door_type):
        if  deco_door_type == 'DRAWER':
            template_name = "room_options/wood_doors/custom_wood_doors.html"        
        else:
            template_name = "room_options/wood_doors/create_wood_doors.html"

        return template_name

    def get_form_kwargs(self):
        '''update form args '''
        data = super(DecoDoor, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': Description.WOOD_DOORS})
        return data

    def get_context_data(self, **kwargs):
        context = super(DecoDoor, self).get_context_data(**kwargs)
        context['wood_doors'] = RoomOptionsMasterModel.objects.filter(room=self.room, description=Description.WOOD_DOORS)
        return context

    def get_success_url(self, *args, **kwargs):
        type = self.request.GET.get('type')
        if type:
            return reverse_lazy('room_options:wood-doors', kwargs={
                'room_id' : self.kwargs['room_id']}) + '?type=' + type
        else:
            return reverse_lazy('room_options:wood-doors', kwargs={
            'room_id' : self.kwargs['room_id']})
        
    def form_valid(self, form):
        return super(DecoDoor, self).form_valid(form)

    def form_valid_save(self, form, type):
        obj = form.save(commit=False)
        obj.room = self.room
        obj.description = Description.WOOD_DOORS
        # obj.part_sub_category = type
        # obj.category = type
        obj.save()
        return super(DecoDoor, self).form_valid(form)

    
    def form_invalid(self, form):
        print(form.data, "dddddd")
        print(form.errors, 'errors')
        return super(DecoDoor, self).form_invalid(form)



@logged_user_view()
@is_classy_user_view()
class DecoDoorView(DecoDoor):
    
    form_class = WoodDoorsForm

    def get_template_names(self):
        return self.get_template_for_display(self.request.GET.get('type'))

    def get_initial(self):
        initial = super(DecoDoorView, self).get_initial()
        details = {}
        try:
            option = RoomOptionsMasterModel.objects.get(room__job__user=self.request.user, pk=self.kwargs['id'])
            print(option)
            details={
                'description':option.description,
                'description2':option.description2,
                'height':option.height,
                'width':option.width,
                'depth':option.depth,
                'part_sub_category':option.part_sub_category,
                'glazing':option.glazing,
                'wood_panel_type':option.wood_panel_type,
                'wood_door_style':option.wood_door_style,
                'wood_species':option.wood_species,
                'wood_door_size':option.wood_door_size,
                'wood_stain_color':option.wood_stain_color,
                'wood_door_french_lite':option.wood_door_french_lite,
                'lti_door_type':option.lti_door_type,
                'quantity':option.quantity,
                'overlay_options1':option.overlay_options1,
                'wood_door_custom_size':option.wood_door_custom_size,
                'notes':option.notes,
                'wood_door_material_type':option.wood_door_material_type,
            }
            
        except:
            pass

        initial.update(details)
        return initial

    def form_valid(self, form):
        return self.form_valid_save(form, self.request.GET.get('type'))


class DecoDoorEditView(UpdateView, DecoDoor):
   
    model = RoomOptionsMasterModel

    def get_template_names(self):
        obj = self.get_object()
        return self.get_template_for_display(obj.part_sub_category)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(DecoDoorEditView, self).get_context_data(**kwargs)
        context['deco_door'] = self.get_object()
        description_details = self.get_object().description2.split(',')
        context['description_details'] =description_details
        context.update(kwargs)

        return context


class WoodDoorItemDescriptionsAjaxView(View):
    def get(self, request):
        data_dict = {}
        try:
            value = request.GET.get('value')
            name = request.GET.get('name')

            if name == "wood_door_style":
                dropdown_obj = WoodSpeciesMapModel.objects.filter(wood_door_drawer_style_id=value, is_active=True)
                data_dict = {obj.pk: obj.description for obj in dropdown_obj}
            if name == "wood_drawer_size":
                height_obj = WoodDoorDrawerSizeMapModel.objects.filter(id=value, is_active=True).first()
                
                data_dict = {height_obj.pk: str(height_obj.height) }
               
            return HttpResponse(json.dumps(data_dict), content_type='application/json')
        except Exception as e:
            print(str(e))
        return HttpResponse(json.dumps(data_dict), content_type='application/json')


class DeleteWoodDoorRoomOptionView(RedirectView):
    
    def get(self, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        try:
            user = self.request.user
            RoomOptionsMasterModel.objects.get(room__job__user=user, id=kwargs['pk']).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':200}))
