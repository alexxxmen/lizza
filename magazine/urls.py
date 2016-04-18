# -*- coding: utf-8 -*-
from django.conf.urls import url
from magazine import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/(?P<slug>[\w-]+)/$', views.category_slug, name='category_slug'),
    url(r'^product/(?P<slug>[\w-]+)/$', views.product_detail, name='product_detail'),

]
