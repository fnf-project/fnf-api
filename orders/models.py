from django.db import models
from django.utils.translation import gettext as _

from products.models import Product
from authentication.models import User

ORDER_STATUS = (
    ("pending", "Pending"),
    ("received", "Received"),
    ("processed", "Processed"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled")
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(_('Total'), max_digits=8, decimal_places=2, null=True, blank=True, help_text='Total')
    discount = models.DecimalField(_('Discount'), max_digits=8, decimal_places=2, null=True, blank=True, help_text='Discount')
    subTotal = models.DecimalField(_('Sub Total'), max_digits=8, decimal_places=2, null=True, blank=True, help_text='Sub Total')
    status = models.CharField(_('Status'), max_length=15, default="pending", help_text='Status', choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return '%s' % self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id
