from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'uom', 'price', 'expiry_date', 'created_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
