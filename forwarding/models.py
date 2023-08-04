from django.db import models
from django.utils import timezone
from django.conf import settings


class Clients(models.Model):
    """Модель клиента для отправки"""
    objects = None

    full_name = models.CharField(max_length=100, verbose_name="Имя клиента", null=False, blank=False, unique=True)
    comment = models.TextField(max_length=500, null=True, blank=True, verbose_name="Комментарии")
    email = models.EmailField(max_length=255, verbose_name="Почта", null=False, blank=False, unique=False)
    slug = models.SlugField(max_length=255, verbose_name="Slug", null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        """Вернуть почту клиента для быстрой рассылки"""
        return self.email


class Transmission(models.Model):
    """Модель передачи для рассылки"""

    objects = None

    class TransmissionStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'
        Running = 'READY'
        Finished_error = 'FINISHED_WITH_ERROR'

    class TransmissionFrequency(models.TextChoices):
        Daily = 'DAILY'
        Weekly = 'WEEKLY'
        Monthly = 'MONTHLY'

    title = models.CharField(max_length=100, verbose_name="Название рассылки", null=False, blank=False, unique=True)
    time = models.TimeField(verbose_name="Время начала отправки", default=timezone.now)
    frequency = models.CharField(choices=TransmissionFrequency.choices, verbose_name="Частота отправки")
    status = models.CharField(choices=TransmissionStatus.choices, default=TransmissionStatus.Created,
                              verbose_name="Статус")
    message = models.ForeignKey("Messages", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщение")
    clients = models.ManyToManyField("Clients", verbose_name="Клиенты")
    slug = models.SlugField(max_length=255, verbose_name="Slug рассылки", null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Шаблоны рассылок"

    def __str__(self):
        return f"Рассылка: {self.title}"

    def get_messages(self):
        """Получить сообщение для передачи, когда используется планировщик"""
        return self.message

    def get_clients(self):
        """Получить клиентов для передачи, когда используется планировщик"""
        return self.clients.all()


class Messages(models.Model):
    """Модель сообщения для клиентов для отправки"""
    objects = None

    theme = models.CharField(max_length=50, verbose_name="Тема сообщения", null=False, blank=False, unique=True)
    body = models.TextField(max_length=500, verbose_name="Тело сообщения", null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')
    slug = models.SlugField(max_length=255, verbose_name="Slug сообщения", null=False, unique=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.theme

    def get_info(self):
        """Вернуть информацию о сообщении для быстрой отправки"""
        return self.theme, self.body


class Statistic(models.Model):
    """Модель статистики передач"""

    class AttemptStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'

    transmission = models.ForeignKey("Transmission", on_delete=models.CASCADE, related_name="statistic_of_transmission",
                                     verbose_name="Передача")
    time = models.DateTimeField(verbose_name="Последнее время отправки", default=None, null=True, blank=True)
    status = models.CharField(choices=AttemptStatus.choices, default=AttemptStatus.Created, verbose_name="Статус")
    mail_answer = models.CharField(verbose_name="Ответ от почтового сервера", default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return f"Статус: {self.status} Время: {self.time} Ответ почты: {self.mail_answer}"
