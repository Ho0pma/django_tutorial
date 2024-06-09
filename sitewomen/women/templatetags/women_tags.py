# @register.simple_tag()
# def get_cat():
#     return views.cats_db

from django import template
from django.db.models import Count

import women.views_01 as views
from women.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    # показывает только те категории, кол-во которых больше 0
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    # показывает только те теги, кол-во которых больше 0
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}