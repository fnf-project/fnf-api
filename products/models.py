from django.db import models
from django.utils.translation import gettext as _


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=255, help_text='Name')
    uom = models.CharField(_('Unit of Measure'), max_length=10, help_text='Unit of Measure')
    weight = models.DecimalField(_('Weight'), max_digits=6, decimal_places=3, help_text='Weight')
    price = models.DecimalField(_('Price'), max_digits=6, decimal_places=2, help_text='Price')
    expiry_date = models.DateField(_('Expiry Date'), blank=True, null=True)
