from django.contrib import admin
from todo.models import Order, Category, Product, Feedback

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
