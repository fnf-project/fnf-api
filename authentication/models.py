from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from authentication.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=50, unique=True, help_text='Username')
    name = models.CharField(_('Name'), max_length=100, help_text='Name')
    password = models.CharField(_('Password'), max_length=255, help_text='Password')
    address = models.CharField(_('Address'), max_length=255, help_text='Address')
    phone_number = models.CharField(_('Phone Number'), max_length=25, help_text='Phone number')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
