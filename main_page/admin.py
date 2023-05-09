from django.contrib import admin
from .models import Category, Product, UserCart


# Показываем в админ панели

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserCart)
