from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from account import ROLE_CHOICES
from django.db import models

# Create your models here.


class User(AbstractUser, PermissionsMixin):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_guest(self):
        return self.role == 'guest'
