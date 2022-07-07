from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True, help_text='Name')
    slug = models.SlugField(_('Slug'), unique=True, help_text='Slug')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(_('Name'), max_length=255, help_text='Name')
    slug = models.SlugField(_('Slug'), unique=True, help_text='Slug')
    uom = models.CharField(_('Unit of Measure'), max_length=10, help_text='Unit of Measure')
    weight = models.DecimalField(_('Weight'), max_digits=6, decimal_places=3, help_text='Weight')
    price = models.DecimalField(_('Price'), max_digits=6, decimal_places=2, help_text='Price')
    expiry_date = models.DateField(_('Expiry Date'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
