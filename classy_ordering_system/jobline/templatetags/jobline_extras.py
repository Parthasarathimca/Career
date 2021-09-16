from django import template
register = template.Library()


@register.simple_tag()
def get_material_id(material_list, val):
    for count, ele in enumerate(material_list):
        if str(val) == str(ele.mat_code):
            return count




