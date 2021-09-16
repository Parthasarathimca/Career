import pickle
import os

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic.base import ContextMixin

from COS.settings import BASE_DIR
from franchise.models import RoomModel
from room_options.models import CustomMapMaterial, CustomMapCategory, CustomMapEdgeType


class RoomViewMixin(ContextMixin):
    room = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.room = RoomModel.objects.get(pk=self.kwargs['room_id'])
        except RoomModel.DoesNotExist:
            raise ObjectDoesNotExist
        if self.room.job.user != request.user and not request.user.is_superuser:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.room:
            context['room'] = self.room
        context['all_rooms'] = self.room.job.job_room.all()
        context.update(kwargs)
        return super().get_context_data(**context)


def create_lookup():
    custom_categories = CustomMapCategory.objects.all()
    lookup = dict()
    for category in custom_categories:
        default_list = [{"id": '', "text": "Select"}]
        lookup[category.cat_name] = {
            'mat_type': default_list + [
                {
                    "id": mat.id,
                    "text": mat.mat_name
                }
                for mat in category.materials.all()
            ],
            'drills': default_list + [
                {
                    "id": drill.id,
                    "text": drill.desc
                }
                for drill in category.drills.all()
            ],
            'width': category.width,
            'depth': category.depth,
            'height': category.height,
            'id': category.id,
            'text': category.cat_name
        }
    return lookup



def create_material_lookup():

    custom_mat = CustomMapMaterial.objects.all()
    mat_lookup = dict()

    for material in custom_mat:
        default_list = [{"id": '', "text": "Select"}]
        mat_lookup[material.mat_name] = {
            'bd_color': default_list + [
                {
                    "id": color.id,
                    "text": color.color
                }
                for color in material.board_colors.all()
            ],
            'st_color': default_list + [
                {
                    "id": color.id,
                    "text": color.color
                }
                for color in material.stain_colors.all()
            ],
            'ed_type': default_list + [
                {
                    "id": ed_type.id,
                    "text": ed_type.edge_type
                }
                for ed_type in material.edge_types.all()
            ],
            'width': float(material.width_default) if material.width_default is not None else None,
            'depth': float(material.depth_default) if material.depth_default is not None else None,
            'height': float(material.height_default) if material.height_default is not None else None ,
            'long_side_1': material.long_side_1,
            'long_side_2': material.long_side_2,
            'short_side_1': material.short_side_1,
            'short_side_2': material.short_side_2,
            'id': material.id,
            'text': material.mat_name
        }
    return mat_lookup


def create_color_lookup():
    edge_types = CustomMapEdgeType.objects.all()
    color_lookup = dict()
    for edge_type in edge_types:
        default_list = [{"id": '', "text": "Select"}]
        color_lookup[edge_type.edge_type] = {
            'edge_colors': default_list + [
                {
                    "id": color.id,
                    "text": color.edge_color
                }
                for color in edge_type.edge_colors.all()
            ],
            'id': edge_type.id,
            'text': edge_type.edge_type
        }
    return color_lookup


