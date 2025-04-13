from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_regex = RegexValidator(regex=r'09(\d{9})$', message="Phone number must be entered in the format: '091234567899'. Up to 11 digits allowed.")
    phone_number = models.CharField(_('Phone Number'), unique=True, max_length=15, validators=[phone_regex])

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name