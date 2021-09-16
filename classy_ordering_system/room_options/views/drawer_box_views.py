import functools
import itertools
import uuid
from time import sleep

from django.http import JsonResponse, HttpResponse
from django.views.generic import FormView, DeleteView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options.conf import Description, drawer_size_height, DrawerBoxType
from room_options.models import RoomOptionsMasterModel, DrawerSizeMapModel, DrawerBox
from room_options.drawer_box_forms import DrawerBoxForm
from room_options.utils import RoomViewMixin

@is_classy_user_view()
class DrawerBoxBase(RoomViewMixin):

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(DrawerBoxBase, self).get_context_data(**kwargs)
        context['drawer_boxes'] = DrawerBox.objects.filter(room_id=self.kwargs['room_id'])
        context['height_map'] = drawer_size_height
        context['counter'] = functools.partial(next, itertools.count(1))

        context.update(kwargs)
        return context

    def room_option_save(self, option, face):

        obj = option.drawer_box_form
        option.height = obj.height
        option.quantity = obj.quantity
        option.mat_type = obj.standard_melamine
        option.description2 = 'Drawer {} ({})'.format(face, obj.size)
        option.description = Description.DRAWER_BOX
        option.depth = obj.depth
        option.part_sub_category = "STANDARD"
        if obj.size == "CUSTOM":
            option.part_sub_category = "CUSTOM"

        if  face == 'Bottom':
            option.height = 0.375
            option.quantity = obj.quantity
            option.width = float(obj.opening) - 1.00

        if face == 'Sides':
            option.quantity = obj.quantity * 2
            option.width = 0.5

        if face == 'Back':
            option.width = float(obj.opening) - 2.05
            option.depth = 0.5

        if face == 'Front':
            option.width = float(obj.opening) - 2.05
            option.depth = 0.5

        return option.save()


@is_classy_user_view()
@logged_user_view()
class DrawerBoxView(FormView, DrawerBoxBase):

    form_class = DrawerBoxForm

    def get_template_names(self):
        template_name = 'room_options/drawer_box/drawer-box.html'
        return template_name

    def get_initial(self):
        initial = super(DrawerBoxView, self).get_initial()
        details = {'standard_melamine': DrawerBoxType.STANDARD_MELAMINE}
        initial.update(details)
        return initial

    def get_success_url(self):
        return reverse_lazy('room_options:drawer-boxes',
                            kwargs={'room_id': self.room.id}
                            )

    def form_invalid(self, form):
        print(form.errors)
        return super(DrawerBoxView, self).form_invalid(form)



    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.room = self.room
        obj.size_type = 'Standard'
        obj.save()
        self.room_option_save(RoomOptionsMasterModel(drawer_box_form=obj, room=self.room), 'Bottom')
        self.room_option_save(RoomOptionsMasterModel(drawer_box_form=obj, room=self.room), 'Sides')
        self.room_option_save(RoomOptionsMasterModel(drawer_box_form=obj, room=self.room), 'Back')
        self.room_option_save(RoomOptionsMasterModel(drawer_box_form=obj, room=self.room), 'Front')

        return super(DrawerBoxView, self).form_valid(form)

@is_classy_user_view()
@logged_user_view()
class DrawerBoxEditView(UpdateView, DrawerBoxBase):
    model = DrawerBox
    form_class = DrawerBoxForm

    def get_template_names(self):
        template_name = 'room_options/drawer_box/drawer-box.html'
        return template_name

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('room_options:drawer-boxes',
                            kwargs={'room_id': self.kwargs['room_id']})

    def form_invalid(self, form):
        messages.error(self.request, 'Problem saving Drawer Box')
        return super(DrawerBoxEditView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(DrawerBoxEditView, self).get_context_data(**kwargs)
        context['drawer_box'] = self.get_object()
        context.update(kwargs)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.room = self.room
        obj.save()
        self.room_option_save(RoomOptionsMasterModel.objects.get(description2__contains='Bottom', drawer_box_form=obj), 'Bottom')
        self.room_option_save(RoomOptionsMasterModel.objects.get(description2__contains='Sides', drawer_box_form=obj), 'Sides')
        self.room_option_save(RoomOptionsMasterModel.objects.get(description2__contains='Back', drawer_box_form=obj), 'Back')
        self.room_option_save(RoomOptionsMasterModel.objects.get(description2__contains='Front',drawer_box_form=obj), 'Front')

        return super(DrawerBoxEditView, self).form_valid(form)


@is_classy_user_view()
@logged_user_view()
class DrawerBoxDeleteView(RedirectView, RoomViewMixin):

    def get(self, *args, **kwargs):
        DrawerBox.objects.get(id=self.kwargs['pk']).delete()
        RoomOptionsMasterModel.objects.filter(drawer_box_form__id=self.kwargs['pk']).delete()
        return HttpResponse(JsonResponse({'status': 200}))
