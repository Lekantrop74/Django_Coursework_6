from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from config import settings


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.CharField(max_length=255, unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to='blog_previews/', verbose_name="Превью", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        # Генерировать slug на основе email перед сохранением объекта
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
