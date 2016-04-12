# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=100, verbose_name='Название')
    desc = models.TextField(max_length=300, blank=True, null=True, verbose_name='Описание')

    # возможные поля:
    # - картинка

    def __unicode__(self):
        return self.title


class Feedback(models.Model):
    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    NEW = 'N'
    TREATED = 'T'
    FEEDBACK_STATUS = (
        (NEW, 'Новое'),
        (TREATED, 'Обработанное'),
    )
    name = models.CharField(max_length=100, verbose_name='Имя')
    subject = models.CharField(max_length=150, verbose_name='Тема письма')
    email = models.EmailField(verbose_name='Почта')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='Номер телефона')
    text = models.TextField(max_length=1000, verbose_name='Текст письма')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изминения')
    status = models.CharField(max_length=1, choices=FEEDBACK_STATUS, default=NEW, verbose_name='Статус')

    def short_text(self):
        return self.text[:145]+'...'
    short_text.short_description = 'Содержимое письма'

    def __unicode__(self):
        return self.subject[:20]


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    IN_STOCK = 'S'
    NOT_AVAILABLE = 'N'
    ORDER = 'O'
    PRODUCT_STATUS = (
        (IN_STOCK, 'В наличии'),
        (NOT_AVAILABLE, 'Нет в продаже'),
        (ORDER, 'Под заказ'),
    )
    product_code = models.CharField(max_length=30, null=True, unique=True, verbose_name='Код')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    short_desc = models.TextField(max_length=150, blank=True, verbose_name='Краткое описание')
    full_desc = models.TextField(blank=True, verbose_name='Полное описание')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    count = models.IntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    img = models.ImageField(upload_to='media/images/product', blank=True, verbose_name='Картинка')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    status = models.CharField(max_length=1, choices=PRODUCT_STATUS, default=ORDER, verbose_name='Статус')

    def __unicode__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    NEW = 'N'
    REFUSE = 'R'
    TREATED = 'T'
    ORDER_STATUS = (
        (NEW, 'Новый'),
        (REFUSE, 'Отказ'),
        (TREATED, 'Обработанный'),
    )
    name = models.CharField(max_length=100, verbose_name='Имя заказчика')
    count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    phone = PhoneNumberField(null=True, verbose_name='Номер телефона')
    email = models.EmailField(blank=True, verbose_name='Почта')
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=NEW, verbose_name='Статус заказа')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    text = models.CharField(max_length=300, blank=True, verbose_name='Дополнение')
    product = models.ManyToManyField(Product,
                                     related_name='products',
                                     related_query_name='product',
                                     verbose_name='Товар(ы)')

    def short_text(self):
        return self.text[:145]+'...'
    short_text.short_description = 'Дополнение'

    def data(self):
        rez = ''
        if self.name:
            rez += self.name
            if self.email:
                rez += ' | ' + self.email
                if self.phone:
                    rez += ' | ' + str(self.phone)
        return rez
    data.short_description = 'Пользователь'

    def order_id(self):
        return 'Заказ № ' + str(self.id)
    order_id.short_description = 'Номер заказа'

    def __unicode__(self):
        return 'Order # %s' % self.id