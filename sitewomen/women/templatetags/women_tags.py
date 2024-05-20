from django import template
from women import views

register = template.Library()

@register.simple_tag()
def get_cat():
    return views.cats_db