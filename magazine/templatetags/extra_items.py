# -*- coding: utf-8 -*-

from django import template
import random

from magazine.models import Product

register = template.Library()


@register.inclusion_tag('magazine/template_tags/_extra_items.html')
def extra_items():
    """
    :return: 5 random products
    """

    products = Product.objects.filter(status=Product.IN_STOCK)
    if len(products) < 5: return dict(products=products)
    else:
        lst = list(products)
        random.shuffle(lst)
    return dict(products=lst[:5])

