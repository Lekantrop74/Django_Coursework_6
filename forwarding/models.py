from config import settings
import django as django
from django.db import models


# Create your models here.
class Clients(models.Model):
    """Model of client for sending"""
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
        """Return client mail for fast sending"""
        return self.email


class Transmission(models.Model):
    """Model transmission for sending"""

    class TransmissionStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'
        Running = 'READY'
        Finished_error = 'FINISHED_WITH_ERROR'

    class TransmissionFrequency(models.TextChoices):
        Daily = 'DAILY'
        Weekly = 'WEEKLY'
        Monthly = 'MONTHLY'

    title = models.CharField(max_length=100, verbose_name="transmission name", null=False, blank=False, unique=True)
    time = models.TimeField(verbose_name="start time for sending", default=django.utils.timezone.now)
    frequency = models.CharField(choices=TransmissionFrequency.choices)
    status = models.CharField(choices=TransmissionStatus.choices, default=TransmissionStatus.Created)
    message = models.ForeignKey("Messages", on_delete=models.SET_NULL, null=True, blank=True)
    clients = models.ManyToManyField("Clients")
    slug = models.SlugField(max_length=255, verbose_name="transmission slug", null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Transmission"
        verbose_name_plural = "Transmission Templates"

    def __str__(self):
        return f"Transmission: {self.title}"

    def get_statistic(self):
        """Get statistic of send. Use Related name in Statistic"""
        return self.statistic_of_transmission.all()

    def get_messages(self):
        """Get message for transmission when used scheduler"""
        messages = self.message
        return messages

    def get_clients(self):
        """Get clients for transmission when used scheduler"""
        clients = self.clients.all()
        return clients


class Messages(models.Model):
    """Model message for clients for sending"""
    theme = models.CharField(max_length=50, verbose_name="message theme", null=False, blank=False, unique=True)
    body = models.TextField(max_length=500, verbose_name="message body", null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=255, verbose_name="message slug", null=False, unique=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.theme

    def get_info(self):
        """Return information about message for fast sending"""
        return self.theme, self.body


class Statistic(models.Model):
    """Model for statistic of transmissions"""

    class AttemptStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'

    transmission = models.ForeignKey("Transmission", on_delete=models.CASCADE, related_name="statistic_of_transmission")
    time = models.DateTimeField(verbose_name="last time for send", default=None, null=True, blank=True)
    status = models.CharField(choices=AttemptStatus.choices, default=AttemptStatus.Created)
    mail_answer = models.CharField(verbose_name="answer from mailserver", default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"

    def __str__(self):
        return f"Status: {self.status} Time: {self.time} Mail answer: {self.mail_answer}"
