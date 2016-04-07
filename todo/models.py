# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    desc = models.CharField(max_length=300, verbose_name='Описание категории')

    # возможные поля:
    # - картинка

    def __str__(self):
        return self.title


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    subject = models.CharField(max_length=150, verbose_name='Тема отзыва')
    email = models.EmailField(verbose_name='Почта пользователя')
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')

    def __str__(self):
        return self.subject[:50]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    desc = models.CharField(max_length=500, blank=True, verbose_name='Описание товара')
    count = models.IntegerField(default=0, verbose_name='Количество товара')
    category = models.ForeignKey(Category, verbose_name='Категория товара')
    img = models.ImageField(upload_to='images', verbose_name='Картинка товара')

    def __str__(self):
        return self.name
