from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_no = models.CharField(max_length=20, unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, default='default_profile_photos/default_profile.jpg')

    # New field for wallet balance
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=100)


    # Specify related_name to avoid clashes
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='customuser_set')

    def __str__(self):
        return self.username




