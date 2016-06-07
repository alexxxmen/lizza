# -*- coding: utf-8 -*-
from django.conf.urls import url
from magazine import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    # url(r'^feedback/add/$', views.add_feedback, name='add_feedback'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/(?P<slug>[\w-]+)/$', views.category_slug, name='category_slug'),
    url(r'^item/(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.product_detail, name='product_detail'),
    url(r'^cart/$', views.cart_detail, name="cart_detail"),
    url(r'^cart/add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^cart/remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^create/$', views.order_create, name='order_create'),

]
