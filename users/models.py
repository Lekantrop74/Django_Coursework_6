from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Телефон', null=True, blank=True)
    country = models.CharField(max_length=150, verbose_name='Страна', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
