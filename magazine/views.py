# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from magazine.models import Product, Category, OrderPosition
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

from magazine.forms import FeedbackForm, OrderCreateForm, CartAddProductForm
from magazine.cart import Cart

from datetime import datetime, timedelta


def home(request):
    products = Product.objects.order_by('status', '?')

    #  Add Paginator
    paginator = Paginator(products, 16, orphans=3)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        products = paginator.page(page)
    except (InvalidPage, EmptyPage):
        products = paginator.page(paginator.num_pages)

    #  Context
    context = pre_context()
    context['title'] = 'Интернет - магазин "'+settings.SITE_NAME+'": качественно, выгодно'
    context['active_menu'] = 'home'
    context['products'] = products
    context['cart_product_form'] = CartAddProductForm()

    return render(request, 'magazine/main/index.html', context)


def feedback(request):

    context = pre_context()
    context['title'] = 'Обратная связь'
    context['active_menu'] = 'feedback'

    form = FeedbackForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return render(request, 'magazine/feedback/success.html', context)

    context['form'] = form

    return render(request, 'magazine/feedback/index.html', context)


def contacts(request):
    context = pre_context()
    context['title'] = 'Контактная информация'
    context['active_menu'] = 'feedback'

    return render(request, 'magazine/contacts/index.html', context)


def categories(request):
    obj_list = Category.objects.all()
    context = pre_context()
    context['title'] = 'Категории | интернет - магазин "'+settings.SITE_NAME+'"'
    context['active_menu'] = 'categories'
    context['categories'] = obj_list

    return render(request, 'magazine/category/index.html', context)


def category_slug(request, slug):

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(Q(category__slug=slug) | Q(category__parent=category))

    #  Add Paginator
    paginator = Paginator(products, 16, orphans=3)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try:
        products = paginator.page(page)
    except (InvalidPage, EmptyPage):
        products = paginator.page(paginator.num_pages)

    context = pre_context()
    context['title'] = u'%s | интернет - магазин "%s"' % (category.name, settings.SITE_NAME)
    context['active_menu'] = 'categories'
    context['active_category'] = category.name
    context['products'] = products
    context['category'] = category

    return render(request, 'magazine/category/category_items.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)

    context = pre_context()
    context['title'] = u'%s | интернет - магазин "%s"' % (product.name, settings.SITE_NAME)
    context['active_category'] = product.category
    context['product'] = product
    context['cart_product_form'] = CartAddProductForm()

    return render(request, 'magazine/product/index.html', context)


#  ---------------------------CART-------------------------------

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    print 'product %s' % product
    print 'cart: %s' % cart
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 count=cd['count'],
                 update_count=cd['update'])
        print 'to cart add "product:"%s, "count:"%s, "update_count:"%s'%(product,cd['count'],cd['update'])
    else: print 'form is not valid'
    return redirect('magazine:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('magazine:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    context = pre_context()

    for item in cart:
        item['update_count_form'] = CartAddProductForm(initial={'count': item['count'],
                                                                   'update': True})

    context['cart'] = cart

    return render(request, 'magazine/cart/cart.html', context)


def order_create(request):
    cart = Cart(request)

    context = pre_context()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                discount_price = item['price'] - ((item['price']/100) * item['discount']) if item['discount'] > 0 \
                    else item['price']
                total_price = discount_price * item['count'] if item['discount'] > 0 \
                    else discount_price * item['count']

                OrderPosition.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             count=item['count'],
                                             discount=item['discount'],
                                             discount_price=discount_price,
                                             total_price=total_price)
            # clear the cart
            cart.clear()
            request.session[settings.CART_SESSION_CREATED] = datetime.now()
            context['order'] = order
            return render(request, 'magazine/cart/created.html', context)

    form = OrderCreateForm()
    context['cart'] = cart
    context['form'] = form
    return render(request, 'magazine/cart/create.html', context)

#  ---------------------------END CART---------------------------------


def pre_context():
    context = {
        'sitename': settings.SITE_NAME,
        'currency': settings.CURRENCY,
        'categories': Category.objects.all()
    }
    return context
