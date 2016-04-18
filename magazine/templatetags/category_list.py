# -*- coding: utf-8 -*-

from django import template
from magazine.models import Category

register = template.Library()


@register.inclusion_tag('magazine/template_tags/_category_list.html')
def category_list():
    categories = Category.objects.all()
    return locals()