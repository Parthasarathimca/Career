from django import template
from django.forms import CheckboxInput

register = template.Library()

@register.filter(name='split_height')
def split_height(field):
  try:
    return float(field.split(' ')[0])
  except:
    return field