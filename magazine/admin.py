# -*- coding:utf-8 -*-
from django.contrib import admin
from magazine.models import Order, Category, Product, Feedback
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    short_desc = forms.CharField(label='Краткое описание', widget=CKEditorWidget())
    # short_desc = forms.CharField(widget=CKEditorUploadingWidget())
    full_desc = forms.CharField(label='Полное описание', widget=CKEditorWidget())
    full_desc = forms.CharField(label='Полное описание' ,widget=CKEditorUploadingWidget())


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    desc = forms.CharField(label='Описание', widget=CKEditorWidget())
    desc = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())


class FeedbackAdminForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    text = forms.CharField(label='Текст письма', widget=CKEditorWidget())
    # text = forms.CharField(widget=CKEditorUploadingWidget())


class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'product_code', 'count',
                    'create_date', 'category', 'modified', 'status')
    list_display_links = ('name',)
    search_fields = ['name', 'product_code', 'create_date',
                     'modified', 'status', 'category__title']
    list_filter = ['create_date', 'category__title', 'modified',
                   'status', 'count']
    readonly_fields = ('create_date', 'modified')
    fieldsets = [
        ('Главное', {'fields': [('name', 'img'), ('product_code',)]}),
        ('Детально', {'fields': [('category', 'status'), ('count',),
                                 ('short_desc',), ('full_desc',),
                                 ]}),
        ('Дополнительно', {'fields': [('slug',), ('create_date', 'modified')], 'classes': ['collapse']}),
    ]

    form = ProductAdminForm

    def make_instock(self, request, queryset):
        updated = queryset.update(status=Product.IN_STOCK)
        if updated == 1:
            message_b = '1-й записи был'
        else:
            message_b = '%s записей был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Есть в наличии\'' % message_b)
    make_instock.short_description = 'Товар есть в наличии'

    def make_not_available(self, request, queryset):
        updated = queryset.update(status=Product.NOT_AVAILABLE)
        if updated == 1:
            message_b = '1-й записи был'
        else:
            message_b = '%s записей был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Нет в продаже\'' % message_b)
    make_not_available.short_description = 'Товара нет в продаже'

    def make_on_order(self, request, queryset):
        updated = queryset.update(status=Product.ORDER)
        if updated == 1:
            message_b = '1-й записи был'
        else:
            message_b = '%s записей был' %updated
        self.message_user(request, 'Статус %s успешно изменен на \'Под заказ\'' % message_b)
    make_on_order.short_description = 'Товар под заказ'

    actions = ['make_instock', 'make_not_available', 'make_on_order']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'desc',)
    list_display_links = ('title',)
    search_fields = ['title', 'desc']
    form = CategoryAdminForm


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'short_text', 'create_date', 'modified', 'status')
    list_display_links = ('subject',)
    search_fields = ['subject', 'name', 'text', 'status', 'create_date', 'modified']
    list_filter = ['create_date', 'modified', 'status']
    readonly_fields = ('create_date', 'modified')
    fieldsets = [
        ('Данные для ответа', {'fields': [('name',), ('email', 'phone')]}),
        ('Письмо', {'fields': [('subject',), ('text',)]}),
        ('Дополнительно', {'fields': [('create_date', 'modified', 'status')]})
    ]

    form = FeedbackAdminForm

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


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'data', 'modified', 'status')
    list_display_links = ('order_id',)
    search_fields = ['name', 'modified']
    list_filter = ['status', 'modified']
    readonly_fields = ('create_date', 'modified')
    fieldsets = [
        ('Информация для связи', {'fields': [('name', 'phone'), ('email',)]}),
        ('Заказ', {'fields': [('product',), ('text',)]}),
        ('Дополнительно', {'fields': [('create_date', 'modified', 'status')],
                           'classes': ['collapse']})
    ]

    def make_new(self, request, queryset):
        updated = queryset.update(status=Order.NEW)
        if updated == 1:
            self.message_user(request, '1 заказ был успешно помечен как \'Новый\'')
        elif (str(updated)[1:] in ['2', '3', '4'] or updated in [2, 3, 4]) and (updated < 5 or updated > 20):
            self.message_user(request, '%s заказа были успешно помечены как \'Новые\'' % updated)
        else:
            self.message_user(request, '%s заказов было успешно помечено как \'Новые\'' % updated)
    make_new.short_description = 'Пометить как новый'

    def make_refuse(self, request, queryset):
        updated = queryset.update(status=Order.REFUSE)
        if updated == 1:
            self.message_user(request, 'По 1 заказу было успешно отказано')
        else:
            self.message_user(request, 'По %s заказам было успешно отказано' % updated)
    make_refuse.short_description = 'Пометить как отказ'

    def make_treated(self, request, queryset):
        updated = queryset.update(status=Order.TREATED)
        if updated == 1:
            self.message_user(request, '1 заказ был успешно помечен как \'Обработанный\'')
        elif (str(updated)[1:] in ['2', '3', '4'] or updated in [2, 3, 4]) and (updated < 5 or updated > 20):
            self.message_user(request, '%s заказа были успешно помечены как \'Обработанные\'' % updated)
        else:
            self.message_user(request, '%s заказов было успешно помечено как \'Обработанные\'' % updated)
    make_treated.short_description = 'Пометить как обработанный'

    actions = ['make_new', 'make_refuse', 'make_treated']

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
