# -*- coding:utf-8 -*-
from django.contrib import admin
from magazine.models import Order, Category, Product, Feedback


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
        ('Главное', {'fields': [('name', 'img'), ('product_code',)]}),
        ('Детально', {'fields': [('category', 'status'), ('count',),
                                 ('short_desc', 'full_desc')]}),
        ('Дополнительно', {'fields': [('slug',), ('create_date', 'modified')], 'classes': ['collapse']}),
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc',)
    list_display_links = ('title',)
    search_fields = ['title', 'desc']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'short_text', 'create_date', 'modified', 'status')
    list_display_links = ('subject',)
    search_fields = ['subject', 'name', 'text', 'status', 'create_date', 'modified']
    list_filter = ['create_date', 'modified', 'status']
    readonly_fields = ('create_date', 'modified')
    fieldsets = [
        ('Данные для ответа', {'fields': [('name',), ('email', 'phone')]}),
        ('Письмо', {'fields': [('subject',),('text',)]}),
        ('Дополнительно', {'fields': [('create_date', 'modified', 'status')]})
    ]

    def make_new(self, request, queryset):
        updated = queryset.update(status=Feedback.NEW)
        if updated == 1:
            message_b = '1-го письма был'
        else:
            message_b = '%s писем был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Новое\'' % message_b)
    make_new.short_description = 'Пометить как новое'

    def make_treated(self, request, queryset):
        updated = queryset.update(status=Feedback.TREATED)
        if updated == 1:
            message_b = '1-го письма был'
        else:
            message_b = '%s писем был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Обработанное\'' % message_b)
    make_treated.short_description = 'Пометить как Обработанное'

    actions = ['make_new', 'make_treated']

admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
