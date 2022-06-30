from unicodedata import name
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from authentication.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=50, unique=True, help_text='Username')
    name = models.CharField(_('Name'), max_length=100, help_text='Name')
    password = models.CharField(_('Password'), max_length=255, help_text='Password')
    address = models.CharField(_('Address'), max_length=500, help_text='Address')
    family_members = models.IntegerField(_('Family Members'), help_text='Family Members')
    phone_number = models.CharField(_('Phone Number'), max_length=25, help_text='Phone number')
    subsidy_amount = models.IntegerField(_('Subsidy Amount'), help_text='Subsidy Amount')
    subsidy_percentage = models.IntegerField(_('Subsidy Percentage'), help_text='Subsidy Percentage')
    starting_date = models.DateTimeField(_('Starting Date'), help_text='Subsidy Percentage')
    subsidy_date = models.DateTimeField(_('Starting Date'), help_text='Subsidy Percentage')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
