# -*- coding: utf-8 -*-
from django.conf.urls import url
from magazine import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

]
