# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ProcessedImageField
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit

from django.db import models


@python_2_unicode_compatible
class Category(MPTTModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, verbose_name=_('Название категории'))
    parent = TreeForeignKey('self',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,
                            related_name='children',
                            verbose_name=_('Родитель')
                        )

    desc = models.TextField(max_length=300, blank=True, null=True, verbose_name=_('Описание'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def get_absolute_url(self):
        return reverse('magazine:category_slug', args=[self.slug])

    def __str__(self):
        return self.name


@python_2_unicode_compatible
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

    def __str__(self):
        return self.subject[:20]


@python_2_unicode_compatible
class Product(models.Model):
    class Meta:
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    IN_STOCK = '1'
    NOT_AVAILABLE = '3'
    ORDER = '2'
    PRODUCT_STATUS = (
        (IN_STOCK, _('В наличии')),
        (NOT_AVAILABLE, _('Нет в продаже')),
        (ORDER, _('Под заказ')),
    )

    product_code = models.CharField(max_length=30, null=True, unique=True, verbose_name=_('Код товара'))
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Название'))
    full_desc = models.TextField(verbose_name=_('Полное описание'))

    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    count = models.IntegerField(default=0, verbose_name=_('Количество'))

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('Категория'))
    # img = models.ImageField(upload_to='images/products/%Y/%m/%d', blank=True, verbose_name=_('Картинка'))
    img = ProcessedImageField(upload_to='images/products/%Y/%m/%d',
                              processors=[ResizeToFit(800, 700)],
                              format='JPEG',
                              options={'quality': 90},
                              verbose_name=_('Картинка'))
    img_preview = ImageSpecField(source='img',
                                 processors=[ResizeToFit(500, 200)],
                                 format='JPEG',
                                 options={'quality': 90})
    img_medium = ImageSpecField(source='img',
                                processors=[ResizeToFit(350, 250)],
                                format='JPEG',
                                options={'quality': 90})

    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    status = models.CharField(max_length=1, choices=PRODUCT_STATUS, default=ORDER, verbose_name=_('Статус'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    discount = models.PositiveIntegerField(default=0, blank=True, verbose_name=_('Скидка'))

    @property
    def discount_price(self):
        if self.discount:
            return Decimal(self.price - ((self.price/100) * self.discount)).quantize(Decimal('.00'))
        else: return 0

    def get_absolute_url(self):
        return reverse('magazine:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    NEW = 'N'
    REFUSE = 'R'
    TREATED = 'T'
    ORDER_STATUS = (
        (NEW, _('Новый')),
        (REFUSE, _('Отказ')),
        (TREATED, _('Обработанный')),
    )
    first_name = models.CharField(max_length=50, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Фамилия'))

    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name=_('Номер телефона'))
    email = models.EmailField(blank=True, verbose_name=_('Почта'))

    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=NEW, verbose_name=_('Статус заказа'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    text = models.TextField(max_length=300, blank=True, verbose_name=_('Дополнение'))
    address = models.CharField(max_length=256, null=True, blank=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    def short_text(self):
        return self.text[:145]+'...'
    short_text.short_description = _('Дополнение')

    def data(self):
        rez = ''
        if self.first_name: rez += self.first_name
        if self.last_name: rez += ' %s' % self.last_name
        if self.email: rez += ' | %s' % self.email
        if self.phone: rez += ' | %s' % self.phone
        return rez

    data.short_description = _('Пользователь')

    def order_id(self):
        return 'Заказ № ' + str(self.id)
    order_id.short_description = _('Номер заказа')

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return 'Order # %s' % self.id


@python_2_unicode_compatible
class OrderPosition(models.Model):
    class Meta:
        verbose_name = 'Order position'
        verbose_name_plural = 'Order Positions'
        ordering = ['-count']

    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='positions')
    product = models.ForeignKey('magazine.Product', null=True, on_delete=models.SET_NULL, related_name='product',
                                verbose_name=_('Товар'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))

    discount = models.PositiveIntegerField(verbose_name=_('Скидка'))
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена со скидкой'))

    count = models.PositiveIntegerField(default=0, verbose_name=_('Количество'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Стоимость'))

    def __str__(self):
        return '%s' % self.id

    def get_cost(self):
        if self.discount:
            discount_price = self.price - ((self.price/100) * self.discount)
            return discount_price * self.count
        else: return self.price * self.count
