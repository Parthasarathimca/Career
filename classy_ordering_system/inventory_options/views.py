from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,HttpResponse
from django.views.generic import TemplateView, FormView, View,RedirectView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse,Http404
from django.views.generic.edit import DeleteView
from franchise.models import JobModel, RoomMatTypeModelMap, RoomModel,RoomColorChoiceModelMap
from franchise.forms import CreateJobForm, CreateRoomForm
from COS.core.decorators import logged_user_view,is_classy_user_view
from room_options import models
from room_options.models import RoomOptionsMasterModel
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .forms import CreateWoodInventory, CreateHardwareInventory, CreateMarketingMaterialInventory
from room_options.utils import RoomViewMixin
from inventory_options.models import HardwareCategory, InventoryExtra, BoardColor, EdgeType, MarketingInventory, MaterialType, Inventory, HardwareInventory
import json
# Create your views here.


# ===========Wood inventory View ===================
@is_classy_user_view()
class WoodInventory(FormView):

    form_class = CreateWoodInventory
    template_name = 'inventory/wood_inventory.html'

    def get_template_for_display(self):
        return self.template_name

    def get_form_kwargs(self):
        '''update form args '''
        data = super(WoodInventory, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': request.GET.get('part_sub_category')})
        
        return data

    def get_context_data(self, **kwargs):
        context = super(WoodInventory, self).get_context_data(**kwargs)
        context['wood_inventory'] = RoomOptionsMasterModel.objects.filter(description='WOODEN_INVENTORY')
        return context

    def get_success_url(self):
        return reverse_lazy('inventory_options:wood-inventory')

    def form_valid(self, form):
        return super(WoodInventory, self).form_valid(form)

    def form_valid_save(self, form):
        item = form.cleaned_data['description2']
        board_color = self.request.POST.get('board_color')
        edge_type = form.cleaned_data.get('edge_type')
        item_obj = InventoryExtra.objects.filter(list_name=item).first()
        if board_color:
            inventry = Inventory.objects.create(item=item_obj,
                   bd_color=BoardColor.objects.filter(id=board_color).first(), ed_type=EdgeType.objects.filter(title=edge_type).first(), mat_type=MaterialType.objects.filter(mat_inventory_id=item_obj.id).first())
        else:
            inventry = Inventory.objects.create(item=item_obj,
                ed_type=EdgeType.objects.filter(title=edge_type).first(), mat_type=MaterialType.objects.filter(mat_inventory_id=item_obj.id).first())

        obj = form.save(commit=False)
        obj.inventory = inventry
        obj.save()
        return super(WoodInventory, self).form_valid(form)
@is_classy_user_view()
@logged_user_view()
class WoodInventoryView(WoodInventory):
    
    form_class = CreateWoodInventory

    def form_valid(self, form):
        return self.form_valid_save(form)
    
@is_classy_user_view()
@logged_user_view()
class WoodInventoryEditView(UpdateView, WoodInventory):

    model = RoomOptionsMasterModel

    def get_template_names(self):
        return self.get_template_for_display()

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(WoodInventoryEditView, self).get_context_data(**kwargs)
        context['wood'] = self.get_object()
        context.update(kwargs)

        return context

    def form_valid(self, form):
        return self.form_valid_save(form)


class WoodInventoryDeleteView(RedirectView):
    def get(self, *args, **kwargs):
        try:
            RoomOptionsMasterModel.objects.get(id=kwargs['pk']).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':200}))


# ===========Hardware inventory View ===================
class HardwareInventoryClass(FormView):

    form_class = CreateHardwareInventory
    template_name = "inventory/hardware-inventory.html"

    def get_template_for_display(self):
        return self.template_name

    def get_success_url(self):
        return reverse_lazy('inventory_options:hardware-inventory')

    def get_form_kwargs(self):
        '''update form args '''
        data = super(HardwareInventoryClass, self).get_form_kwargs()
        request = self.request
        data.update({'request': request, 'description': request.POST.get('description')})
        return data

    def get_context_data(self, **kwargs):
        context = super(HardwareInventoryClass, self).get_context_data(**kwargs)
        context['hardware'] = RoomOptionsMasterModel.objects.filter(description='HARDWARE_INVENTORY')
        return context


    def form_valid(self, form):
        return super(HardwareInventoryClass, self).form_valid(form)

    def form_valid_save(self, form):
        category_description = form.cleaned_data['category_description']
        item_category = form.cleaned_data['category']
        category = HardwareInventory.objects.filter(category_description=category_description).first()
        inventry = Inventory.objects.create(hd_category=category, hd_desciption=HardwareCategory.objects.filter(id=item_category).first())
        obj = form.save(commit=False)
        obj.inventory = inventry
        obj.save()
        return super(HardwareInventoryClass, self).form_valid(form)


@logged_user_view()
@is_classy_user_view()
class HardwareInventoryView(HardwareInventoryClass):
    
    form_class = CreateHardwareInventory

    def form_valid(self, form):
        return self.form_valid_save(form)

 
@logged_user_view()
@is_classy_user_view()
class HardwareInventoryEditView(UpdateView, HardwareInventoryClass):

    model = RoomOptionsMasterModel

    def get_template_names(self):
        return self.get_template_for_display()

    def get_context_data(self, **kwargs):
        context = super(HardwareInventoryEditView, self).get_context_data(**kwargs)
        context['hardware_data'] = self.get_object()
        context.update(kwargs)
        return context

    def form_valid(self, form):
        return self.form_valid_save(form)


class HardwareInventoryDeleteView(RedirectView):
    def get(self, *args, **kwargs):
        try:
            RoomOptionsMasterModel.objects.get(id=kwargs['pk']).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':200}))


# =========Marketing View=====================
class MarketingMaterial(FormView):

    form_class = CreateMarketingMaterialInventory
    template_name = "inventory/marketing-material-inventory.html"

    def get_template_for_display(self):
        return self.template_name

    def get_success_url(self):
        return reverse_lazy('inventory_options:marketing-material-inventory')

    def get_form_kwargs(self):
        '''update form args '''
        data = super(MarketingMaterial, self).get_form_kwargs()
        request = self.request
        # data.update({'request': request, 'part_sub_category': request.POST.get('description')})
        return data

    def get_context_data(self, **kwargs):
        context = super(MarketingMaterial, self).get_context_data(**kwargs)
        context['marketing_inventory'] = RoomOptionsMasterModel.objects.filter(part_sub_category='MARKETING_INVENTORY')
        return context

    def form_valid(self, form):
        return super(MarketingMaterial, self).form_valid(form)

    def form_valid_save(self, form):
        description = form.cleaned_data['description']
        description2 = form.cleaned_data['description2']
        inventry = Inventory.objects.create(mkt_description=MarketingInventory.objects.filter(item=description2).first())
        obj = form.save(commit=False)
        obj.inventory = inventry
        obj.part_sub_category = description
        obj.save()
        return super(MarketingMaterial, self).form_valid(form)

    def form_invalid(self, form):
        return super(MarketingMaterial, self).form_invalid(form)


@logged_user_view()
@is_classy_user_view()
class MarketingMaterialInventory(MarketingMaterial):
    
    form_class = CreateMarketingMaterialInventory

    def form_valid(self, form):
        return self.form_valid_save(form)


@logged_user_view()
@is_classy_user_view()
class MarketingInventoryEditView(UpdateView, MarketingMaterial):

    model = RoomOptionsMasterModel

    def get_template_names(self):
        return self.get_template_for_display()

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(MarketingInventoryEditView, self).get_context_data(**kwargs)
        context['marketing'] = self.get_object()
        context.update(kwargs)

        return context

    def form_valid(self, form):
        return self.form_valid_save(form)


class MarketingInventoryDeleteView(RedirectView):
    def get(self, *args, **kwargs):
        try:
            RoomOptionsMasterModel.objects.get(id=kwargs['pk']).delete()
        except:
            raise Http404
        return HttpResponse(JsonResponse({'status':200}))


# class WoodItemDEscriptionsAjaxView(View):
#     def get(self, request):
#         value = request.GET.get('value')
#         name = request.GET.get('name')
#         if name == "description2":
#             dropdown_obj = BoardColor.objects.filter(item_description__id=value)
#             data_dict = {obj.pk: obj.color for obj in dropdown_obj}
#         else:
#             dropdown_obj = EdgeType.objects.filter(color__id=value)
#             data_dict = {obj.pk: obj.title for obj in dropdown_obj}
#         print(data_dict,'===')
#         return HttpResponse(json.dumps(data_dict), content_type='application/json')


class WoodItemDEscriptionsAjaxView(View):
    def get(self, request):
        data_dict = {}
        try:
            value = request.GET.get('value')
            name = request.GET.get('name')

            if name == "description2":
                dropdown_obj = BoardColor.objects.filter(color_inventory__id=value, is_active=True)
                data_color = {obj.pk: obj.color for obj in dropdown_obj}
                order_multiple = InventoryExtra.objects.filter(id=value, is_active=True)
                min_order = {obj.pk: obj.order_multiple for obj in order_multiple}
                edge_obj = EdgeType.objects.filter(edge_inventory__id=value, is_active=True)
                edge_type = {obj.pk: obj.title for obj in edge_obj}
                minimum_order = InventoryExtra.objects.filter(id=value, is_active=True)
                minimum = {obj.pk: obj.min_order for obj in minimum_order}
                data_dict['color'] = data_color
                data_dict['min_order'] = min_order
                data_dict['edge'] = edge_type
                data_dict['minimum'] = minimum

            elif name == "description":
                order_multiple = InventoryExtra.objects.filter(id=value, is_active=True)
                data_dict = {obj.pk: obj.order_multiple for obj in order_multiple}

            elif name == "category_description":
                description = HardwareCategory.objects.filter(category__id=value, is_active=True)
                desc = {obj.pk: obj.description for obj in description}
                min_order = {obj.pk: obj.min_order for obj in description}
                data_dict['desc'] = desc
                data_dict['min_order'] = min_order

            elif name == "item":
                minimum_order = MarketingInventory.objects.filter(id=value, is_active=True)
                data_dict = {obj.pk: obj.min_order for obj in minimum_order}
            print(data_dict,'============data dict============')
            return HttpResponse(json.dumps(data_dict), content_type='application/json')
        except Exception as e:
            print(str(e))
        return HttpResponse(json.dumps(data_dict), content_type='application/json')
    