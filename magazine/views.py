# -*- coding: utf-8 -*-

from lizza import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from magazine.models import Product, Category
from django.template.context_processors import csrf
from magazine.forms import FeedbackForm


def home(request):
    products = Product.objects.all()
    context = {
        'title': 'Магазин - %s' % settings.SITE_NAME,
        'active_menu': 'home',
        'products': products,
    }
    return render(request, 'magazine/index.html', context)


def feedback(request):
    form = {}
    errors = []

    form = FeedbackForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'title': 'Обратная связь - %s' % settings.SITE_NAME,
        'active_menu': 'feedback',
        'form': form,
    }
    context.update(csrf(request))

    return render(request, 'magazine/feedback.html', context)


def contacts(request):
    context = {
        'title': 'Контакты - %s' % settings.SITE_NAME,
        'active_menu': 'contacts',
    }
    return render(request, 'magazine/contacts.html', context)


def categories(request):
    obj_list = Category.objects.all()
    context = {
        'title': 'Категории - %s' % settings.SITE_NAME,
        'active_menu': 'categories',
        'obj_list': obj_list
    }
    return render(request, 'magazine/categories.html', context)


def category_slug(request, slug):

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category__slug=slug)
    context = {
        'title': '%s - %s' % (category.title, settings.SITE_NAME),
        'active_menu': 'categories',
        'active_category': category.title,
        'products': products,
        'category': category,
    }
    return render(request, 'magazine/category.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'title': '%s - %s' % (product.name, settings.SITE_NAME),
        'active_category': product.category,
        'product': product,
    }
    return render(request, 'magazine/product_detail.html', context)
