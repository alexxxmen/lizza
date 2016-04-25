# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=100, verbose_name=_('Название категории'))
    title_bg = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Название категории(Bulgarian)'))
    desc = models.TextField(max_length=300, blank=True, null=True, verbose_name=_('Описание'))
    desc_bg = models.TextField(max_length=300, blank=True, null=True, verbose_name=_('Описание(Bulgarian)'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def __unicode__(self):
        return self.title


class Feedback(models.Model):
    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    NEW = 'N'
    TREATED = 'T'
    FEEDBACK_STATUS = (
        (NEW, _('Новое')),
        (TREATED, _('Обработанное')),
    )
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    subject = models.CharField(max_length=150, verbose_name=_('Тема письма'))
    email = models.EmailField(verbose_name=_('Почта'))
    phone = models.CharField(max_length=14, blank=True, null=True, verbose_name=_('Номер телефона'))
    text = models.TextField(max_length=1000, verbose_name=_('Текст письма'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изминения')
    status = models.CharField(max_length=1, choices=FEEDBACK_STATUS, default=NEW, verbose_name=_('Статус'))

    def short_text(self):
        if len(self.text) > 145:
            return self.text[:145]+'...'
        else:
            return self.text
    short_text.short_description = _('Содержимое письма')

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
        (IN_STOCK, _('В наличии')),
        (NOT_AVAILABLE, _('Нет в продаже')),
        (ORDER, _('Под заказ')),
    )
    product_code = models.CharField(max_length=30, null=True, unique=True, verbose_name=_('Код'))
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Название'))
    name_bg = models.CharField(max_length=100, unique=True, verbose_name=_('Название(Bulgarian)'))
    short_desc = models.TextField(max_length=150, blank=True, verbose_name=_('Краткое описание'))
    short_desc_bg = models.TextField(max_length=150, blank=True, verbose_name=_('Краткое описание(Bulgarian)'))
    full_desc = models.TextField(blank=True, verbose_name=_('Полное описание'))
    full_desc_bg = models.TextField(blank=True, verbose_name=_('Полное описание(Bulgarian)'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    count = models.IntegerField(default=0, verbose_name=_('Количество'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('Категория'))
    img = models.ImageField(upload_to='media/images/product', blank=True, verbose_name=_('Картинка'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    status = models.CharField(max_length=1, choices=PRODUCT_STATUS, default=ORDER, verbose_name=_('Статус'))

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
        (NEW, _('Новый')),
        (REFUSE, _('Отказ')),
        (TREATED, _('Обработанный')),
    )
    name = models.CharField(max_length=100, verbose_name=_('Имя заказчика'))
    phone = models.CharField(max_length=14, null=True, verbose_name=_('Номер телефона'))
    email = models.EmailField(blank=True, verbose_name=_('Почта'))
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=NEW, verbose_name=_('Статус заказа'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    text = models.CharField(max_length=300, blank=True, verbose_name=_('Дополнение'))
    product = models.ManyToManyField(Product,
                                     related_name='products',
                                     related_query_name='product',
                                     verbose_name='Товар(ы)')

    def short_text(self):
        return self.text[:145]+'...'
    short_text.short_description = _('Дополнение')

    def data(self):
        rez = ''
        if self.name:
            rez += self.name
        if self.email:
            rez += ' | ' + self.email
        if self.phone:
            rez += ' | ' + str(self.phone)
        return rez

    data.short_description = _('Пользователь')

    def order_id(self):
        return 'Заказ № ' + str(self.id)
    order_id.short_description = _('Номер заказа')

    def __unicode__(self):
        return 'Order # %s' % self.id
