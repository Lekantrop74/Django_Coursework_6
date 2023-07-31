from django.db import models

from config import settings


# Create your models here.
class Clients(models.Model):
    """Model of client for sending"""
    full_name = models.CharField(max_length=100, verbose_name="Имя клиента", null=False, blank=False, unique=True)
    comment = models.TextField(max_length=500, null=True, blank=True, verbose_name="Комментарии")
    email = models.EmailField(max_length=255,  verbose_name="Почта", null=False, blank=False, unique=False)
    slug = models.SlugField(max_length=255, verbose_name="Slug", null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        """Return client mail for fast sending"""
        return self.email
