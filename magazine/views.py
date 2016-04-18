# -*- coding: utf-8 -*-
from lizza import settings
from django.shortcuts import render


def home(request):
    context = {
        'title': 'Магазин - ' + settings.SITE_NAME
    }
    return render(request, 'magazine/index.html', context)
