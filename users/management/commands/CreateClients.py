from django.core.management.base import BaseCommand
from django.utils.text import slugify
from unidecode import unidecode
from forwarding.models import Clients
import random

from users.models import User

REAL_NAMES = ["Иван Петров", "Елена Смирнова", "Алексей Козлов", "Мария Васильева", "Павел Николаев",
              "Анна Иванова", "Дмитрий Федоров", "Светлана Морозова", "Александр Ковалев", "Ольга Соколова", ]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "example.com"]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for name in REAL_NAMES:
            full_name = name
            comment = "Осмысленный комментарий для " + full_name
            slug = slugify(full_name)
            owner = random.choice(User.objects.all())

            username = unidecode(full_name.lower().replace(" ", "_"))
            domain = random.choice(EMAIL_DOMAINS)
            email = f"{username}@{domain}"

            # Проверить, существует ли клиент с таким же full_name
            existing_client = Clients.objects.filter(full_name=full_name).first()
            if existing_client is None:
                # Создать нового клиента, только если его еще нет в базе данных
                Clients.objects.create(full_name=full_name, comment=comment, email=email, slug=slug, owner=owner)
        self.stdout.write(self.style.SUCCESS('Успешно созданы 10 объектов модели Clients.'))
