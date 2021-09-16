from django.db import models

from COS.core.utils import SortingModel, IsActiveManager


class CustomMapEdgeProfile(SortingModel):
    code = models.CharField(max_length=100,blank=True,null=True)
    edge_profile = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.edge_profile)

    class Meta:
        db_table = "custom_edge_profile_map"
        verbose_name = "Custom Edge Profile Map"
        verbose_name_plural = "Custom Edge Profile Maps"


class CustomMapEdgeColor(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    edge_color = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.edge_color)

    class Meta:
        db_table = "custom_edge_color_map"
        verbose_name = "Custom Edge Color Map"
        verbose_name_plural = "Custom Edge Color Maps"


class CustomMapEdgeType(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    edge_type = models.CharField(max_length=100)
    edge_colors = models.ManyToManyField(CustomMapEdgeColor, blank=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.edge_type)

    class Meta:
        db_table = "custom_edge_type_map"
        verbose_name = "Custom Edge Type Map"
        verbose_name_plural = "Custom Edge Type Maps"


class CustomMapBoardColor(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.color)

    class Meta:
        db_table = "custom_board_color_map"
        verbose_name = "Custom Board Color Map"
        verbose_name_plural = "Custom Board Color Maps"


class CustomStainColor(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.color)

    class Meta:
        db_table = "custom_strain_color_map"
        verbose_name = "Custom Stain Color Map"
        verbose_name_plural = "Custom Stain Color Maps"


class CustomMapMaterial(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    mat_name = models.CharField(max_length=100)
    height_default = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    width_default = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    depth_default = models.DecimalField(decimal_places=2, max_digits=20,blank=True,null=True)
    long_side_1 = models.BooleanField(default=False)
    long_side_2 = models.BooleanField(default=False)
    short_side_1 = models.BooleanField(default=False)
    short_side_2 = models.BooleanField(default=False)
    board_colors = models.ManyToManyField(CustomMapBoardColor, blank=True)
    stain_colors = models.ManyToManyField(CustomStainColor, blank=True)
    edge_types = models.ManyToManyField(CustomMapEdgeType, blank=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.mat_name)

    class Meta:
        db_table = "custom_material_map"
        verbose_name = "Custom Material Map"
        verbose_name_plural = "Custom Material Maps"


class CustomMapDrill(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=100, blank=True, null=True)
    rnd = models.BooleanField(default=False)
    flat = models.BooleanField(default=False)
    std = models.BooleanField(default=False)
    mm22 = models.BooleanField(default=False)
    corner = models.BooleanField(default=False)
    b2b = models.BooleanField(default=False)
    height = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    width = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    depth = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    cycle_time = models.PositiveIntegerField(blank=True, null=True)
    avg_load_time = models.PositiveIntegerField(blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    part_cat = models.CharField(max_length=20,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.desc)

    class Meta:
        db_table = "custom_drill_map"
        verbose_name = "Custom Drill Map"
        verbose_name_plural = "Custom Drill Maps"


class CustomMapCategory(SortingModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    cat_name = models.CharField(max_length=100)
    height = models.BooleanField(default=False)
    width = models.BooleanField(default=False)
    depth = models.BooleanField(default=False)
    materials = models.ManyToManyField(CustomMapMaterial, blank=True)
    drills = models.ManyToManyField(CustomMapDrill, blank=True)
    is_active = models.BooleanField(default=True)
    objects = IsActiveManager()

    def __str__(self):
        return str(self.cat_name)

    class Meta:
        db_table = "custom_category_map"
        verbose_name = "Custom Category Map"
        verbose_name_plural = "Custom Category Maps"


