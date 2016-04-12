# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    desc = models.TextField(max_length=300, blank=True, null=True, verbose_name='Описание категории')

    # возможные поля:
    # - картинка

    def __unicode__(self):
        return self.title


class Feedback(models.Model):
    FEEDBACK_STATUS = (
        ('N', 'Новый'),
        ('F', 'Обработанный'),
    )
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    subject = models.CharField(max_length=150, verbose_name='Тема отзыва')
    email = models.EmailField(verbose_name='Почта пользователя')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='Номер телефона')
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания отзыва')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изминения отзыва')
    status = models.CharField(max_length=1, choices=FEEDBACK_STATUS, default='F', verbose_name='Статус отзыва')

    def __unicode__(self):
        return self.subject[:20]


class Product(models.Model):
    PRODUCT_STATUS = (
        ('S', 'В наличии'),
        ('N', 'Нет в продаже'),
        ('O', 'Под заказ'),
    )
    product_code = models.CharField(max_length=30, null=True, unique=True, verbose_name='product_id')
    name = models.CharField(max_length=100, verbose_name='Название товара')
    short_desc = models.TextField(max_length=300, blank=True, verbose_name='Краткое описание товара')
    full_desc = models.TextField(blank=True, verbose_name='Полное описание товара')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    count = models.IntegerField(default=0, verbose_name='Количество товара')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='category')
    img = models.ImageField(upload_to='media/images/product', blank=True, verbose_name='Картинка товара')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    status = models.CharField(max_length=1, choices=PRODUCT_STATUS, default='O', verbose_name='Статус товара')

    def __unicode__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = (
        ('N', 'Новый'),
        ('R', 'Отказ'),
        ('F', 'Обработанный'),
    )
    name = models.CharField(max_length=100, verbose_name='Имя заказчика')
    count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    phone = PhoneNumberField(null=True, verbose_name='Номер телефона')
    email = models.EmailField(blank=True, verbose_name='Почта')
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='N', verbose_name='Статус заказа')
    text = models.CharField(max_length=300, blank=True, verbose_name='Дополнение')
    product = models.ManyToManyField(Product,
                                     related_name='products',
                                     related_query_name='product')

    def __unicode__(self):
        return 'Order # %s' % self.pk
