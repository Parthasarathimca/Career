from django.db import models
from django.db.models.deletion import CASCADE
from COS.core.utils import TimestampedModel, SortingModel, SortingManager

# Create your models here.

class InventoryExtra(TimestampedModel, SortingModel):
	""" This model will hold inventory data """
	list_name = models.CharField(max_length=255, null=True, blank=True)
	description = models.CharField(max_length=255, null=True, blank=True)
	order_multiple = models.IntegerField()
	min_order = models.BigIntegerField(null=True, blank=True)
	left_ed_type = models.CharField(default='flat', max_length=60)
	height = models.CharField(max_length=55, null=True, blank=True)
	width = models.CharField(max_length=55, null=True, blank=True)
	depth = models.CharField(max_length=55, null=True, blank=True)
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()

	def __str__(self):
		return str(self.list_name)

	class Meta:
		db_table = "inventory_extra_map"
		verbose_name = "Inventory Extra Map"
		verbose_name_plural = "Inventory Extra Map"


class BoardColor(TimestampedModel, SortingModel):
	""" This model will hold multiple board colour with respect to inventory extra item """
	color_inventory = models.ForeignKey(InventoryExtra, on_delete=CASCADE, related_name="board_color")
	color = models.CharField(max_length=400)
	color_code = models.BigIntegerField()
	picture = models.ImageField(upload_to='color_pics', null=True, blank=True)
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()
	
	def __str___(self):
		return str(self.color)

	class Meta:
		db_table = 'inventory_bd_color_map'
		verbose_name = "Inventory Board Type Map"
		verbose_name_plural = "Inventory Board Types Map"


class EdgeType(TimestampedModel, SortingModel):	
	""" This model will hold multiple edge type with respect to board colour """
	edge_inventory = models.ForeignKey(InventoryExtra, on_delete=CASCADE, related_name="edge_type", null=True, blank=True)
	title = models.CharField(max_length=225)
	edge_type_code = models.BigIntegerField()
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()

	def __str__(self):
		return str(self.title)

	class Meta:
		db_table = "inventory_edge_type_map"
		verbose_name = "Inventory Edge Type Map"
		verbose_name_plural = "Inventory Edge Types Map"


class MaterialType(TimestampedModel, SortingModel):	
	""" This model will hold material type with respect to inventory extra """
	mat_inventory = models.ForeignKey(InventoryExtra, on_delete=CASCADE, related_name="mat_type")
	title = models.CharField(max_length=255)
	code = models.CharField(max_length=255)
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()

	def __str__(self):
		return str(self.title)

	class Meta:
		db_table = "inventory_material_type_map"
		verbose_name = "Inventory Material Type Map"
		verbose_name_plural = "Inventory Material Types Map"


class HardwareInventory(TimestampedModel, SortingModel):
	""" This model will hold all the hardware category types """
	category_description = models.CharField(max_length=255)
	cat_code = models.BigIntegerField(null=True, blank=True)
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()

	def __str__(self):
		return str(self.category_description)

	class Meta:
		db_table = "hardware_inventory_map"
		verbose_name = "Hardware Inventory Map"
		verbose_name_plural = "Hardware Inventories Map"


class HardwareCategory(TimestampedModel, SortingModel):
	""" This model will hold category item description with respect to hardware inventory """
	category = models.ForeignKey(HardwareInventory, on_delete=CASCADE)
	item_no = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	order_multiple = models.BigIntegerField()
	min_order = models.BigIntegerField(null=True, blank=True)
	image_url = models.ImageField(upload_to='inventory_pics', default="top-shelf.png")
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()

	def __str__(self):
		return str(self.description)

	class Meta:
		db_table = "hardware_category_map"
		verbose_name = "Hardware Category Map"
		verbose_name_plural = "Hardware Categories Map"


class MarketingInventory(TimestampedModel, SortingModel):
	""" This model will hold the item description for marketing material inventory """
	item = models.CharField(max_length=255)
	order_multiple = models.BigIntegerField()
	min_order = models.BigIntegerField()
	image_url = models.ImageField(upload_to="inventory_pics", default="top-shelf.png")
	is_active = models.BooleanField(null=True, blank=True)
	objects = SortingManager()

	def __str__(self):
		return str(self.item)

	class Meta:
		db_table = "marketing_inventory_map"
		verbose_name = "Marketing Inventory Map"
		verbose_name_plural = "Marketing Inventories Map"


class Inventory(TimestampedModel):
	""" This model will store all the inventory related values """
	item = models.ForeignKey(InventoryExtra, on_delete=CASCADE, null=True, blank=True)
	bd_color = models.ForeignKey(BoardColor, on_delete=CASCADE, null=True, blank=True)
	ed_type = models.ForeignKey(EdgeType, on_delete=CASCADE, null=True, blank=True)
	mat_type = models.ForeignKey(MaterialType, on_delete=CASCADE, null=True, blank=True)
	hd_category = models.ForeignKey(HardwareInventory, on_delete=CASCADE, null=True, blank=True)
	hd_desciption = models.ForeignKey(HardwareCategory, on_delete=CASCADE, null=True, blank=True)
	mkt_description = models.ForeignKey(MarketingInventory, on_delete=CASCADE, null=True, blank=True)

	def __str__(self):
		return str(self.item)

	class Meta:
		db_table = "inventory_master"
		verbose_name = "Inventory Master"
		verbose_name_plural = "Inventories Master"
	