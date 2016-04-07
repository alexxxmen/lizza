# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)

    # возможные поля:
    # - картинка

    def __str__(self):
        return self.title

