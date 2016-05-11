# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


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
    address = models.CharField(max_length=256, null=True)

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


class OrderPosition(models.Model):
    class Meta:
        verbose_name = 'Order position'
        verbose_name_plural = 'Order Positions'
        ordering = ['-count']

    order = models.ForeignKey(Order, related_name='positions')
    product = models.ForeignKey('magazine.Product', related_name='product')
    count = models.PositiveIntegerField(default=0)
