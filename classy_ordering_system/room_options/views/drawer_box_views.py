from django.http import JsonResponse, HttpResponse
from django.views.generic import FormView, DeleteView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from COS.core.decorators import logged_user_view
from room_options.conf import Description
from room_options.models import RoomOptionsMasterModel, DrawerSizeMapModel
from room_options.forms import DrawerBoxForm
from room_options.utils import RoomViewMixin


@logged_user_view()
class DrawerBoxView(FormView, RoomViewMixin):

    form_class = DrawerBoxForm

    def get_template_names(self):
        template_name = 'room_options/drawer_box.html'
        return template_name

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(DrawerBoxView, self).get_context_data(**kwargs)
        context['drawer_size_std'] = DrawerSizeMapModel.objects.all()
        context['drawer_boxes'] = RoomOptionsMasterModel.objects.filter(room=self.room,
                                                                        description=Description.DRAWER_BOX)
        context.update(kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('room_options:drawer-boxes',
                            kwargs={'room_id': self.room.id}
                            )

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Problem saving Drawer Box')
        return super(DrawerBoxView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.description = Description.DRAWER_BOX
        obj.room = self.room
        obj.save()
        messages.success(self.request, 'Drawer box has been added')
        return super(DrawerBoxView, self).form_valid(form)


@logged_user_view()
class DrawerBoxEditView(UpdateView, RoomViewMixin):
    model = RoomOptionsMasterModel
    form_class = DrawerBoxForm

    def get_template_names(self):
        template_name = 'room_options/drawer_box.html'
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
        context['drawer_size_std'] = DrawerSizeMapModel.objects.all()
        context['drawer_box'] = self.get_object()
        context['drawer_boxes'] = RoomOptionsMasterModel.objects.filter(room=self.room,
                                                                        description=Description.DRAWER_BOX)
        context.update(kwargs)
        return context


@logged_user_view()
class DrawerBoxDeleteView(RedirectView, RoomViewMixin):

    def get(self, *args, **kwargs):
        RoomOptionsMasterModel.objects.get(id=self.kwargs['pk']).delete()
        return HttpResponse(JsonResponse({'status': 204}))
