from django import forms
from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from room_options.models import CustomMapMaterial, CustomMapBoardColor, CustomMapCategory
from COS.core.utils import DisableDeleteAdmin




# class ColorInline(admin.TabularInline):
#     model = CustomMapBoardColor.materials.through
#     extra = 1

class CategoryAdmin(DisableDeleteAdmin):
    fieldsets = (
        (None, {
            'fields': ('cat_name', 'height', 'width', 'depth', 'is_active')
        }),
        ('Materials', {
            'classes': ('wide', 'collapse'),
            'fields': ('materials',)
        }),
        ('Drills', {
            'classes': ('wide', 'collapse'),
            'fields': ('drills',)
        }),
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class MaterialAdmin(DisableDeleteAdmin):
    fieldsets = (
        (None, {
            'fields': ('mat_name', 'is_active')
        }),
        ('Defaults', {
            'fields': ('height_default', 'width_default', 'depth_default')
        }),
        ('Sides', {
            'fields': ('long_side_1', 'long_side_2', 'short_side_1', 'short_side_2')
        }),

        ('Board Color', {
            'classes': ('wide', 'collapse'),
            'fields': ('board_colors', )
        }),

        ('Edge Type', {
            'classes': ('wide', 'collapse'),
            'fields': ('edge_types',)
        }),

        ('Stain Color', {
            'classes': ('wide', 'collapse'),
            'fields': ('stain_colors',)
        }),

    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class EdgeTypeAdmin(DisableDeleteAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }