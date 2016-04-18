# -*- coding: utf-8 -*-
from lizza import settings
from django.shortcuts import render, get_object_or_404
from magazine.models import Product, Category


def home(request):
    products = Product.objects.all()
    context = {
        'title': 'Магазин - %s' % settings.SITE_NAME,
        'active_menu': 'home',
        'products': products,
    }
    return render(request, 'magazine/index.html', context)


def feedback(request):
    context = {
        'title': 'Обратная связь - %s' % settings.SITE_NAME,
        'active_menu': 'feedback',
    }
    return render(request, 'magazine/feedback.html', context)


def about(request):
    context = {
        'title': 'О нас - %s' % settings.SITE_NAME,
        'active_menu': 'about',
    }
    return render(request, 'magazine/about.html', context)


def contacts(request):
    context = {
        'title': 'Контакты - %s' % settings.SITE_NAME,
        'active_menu': 'contacts',
    }
    return render(request, 'magazine/contacts.html', context)


def categories(request):
    context = {
        'title': 'Категории - %s' % settings.SITE_NAME,
        'active_menu': 'categories',
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
