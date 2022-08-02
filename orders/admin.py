from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')

class OrderItemAdmin(admin.ModelAdmin):
    def product_weight(self, obj):
        return obj.product.weight

    def product_uom(self, obj):
        return obj.product.uom

    def product_price(self, obj):
        return obj.product.price

    list_display = ('order', 'product', 'product_weight', 'product_uom', 'product_price', 'quantity')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
