# -*- coding:utf-8 -*-
from django.contrib import admin
from todo.models import Order, Category, Product, Feedback


class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'product_code', 'count',
                    'create_date', 'category', 'modified', 'status')
    list_display_links = ('name',)
    search_fields = ['name', 'product_code', 'create_date',
                     'modified', 'status', 'category']
    list_filter = ['create_date', 'category', 'modified',
                   'status', 'count']
    readonly_fields = ('create_date', 'modified')
    fieldsets = [
        ('Главное', {'fields': [('name', 'slug'), ('product_code','img')]}),
        ('Детально', {'fields': [('category', 'status'), ('count',)]}),
        ('Дополнительно', {'fields': [('short_desc', 'full_desc'), ('create_date', 'modified')]})
    ]

    def make_instock(self, request, queryset):
        updated = queryset.update(status='S')
        if updated == 1:
            message_b = '1-й записи был'
        else:
            message_b = '%s записей был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Есть в наличии\'' % message_b)
    make_instock.short_description = 'Товар есть в наличии'

    def make_not_available(self, request, queryset):
        updated = queryset.update(status='N')
        if updated == 1:
            message_b = '1-й записи был'
        else:
            message_b = '%s записей был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Нет в продаже\'' % message_b)
    make_not_available.short_description = 'Товара нет в продаже'

    def make_on_order(self, request, queryset):
        updated = queryset.update(status='O')
        if updated == 1:
            message_b = '1-й записи был'
        else:
            message_b = '%s записей был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Под заказ\'' % message_b)
    make_on_order.short_description = 'Товар под заказ'

    actions = ['make_instock', 'make_not_available', 'make_on_order']

admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)