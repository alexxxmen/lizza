# -*- coding: utf-8 -*-

from magazine.cart import Cart


def cart(request):
    return {'cart': Cart(request)}