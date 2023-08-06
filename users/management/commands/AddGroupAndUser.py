from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import BlogPost
from forwarding.models import Clients, Transmission, Messages
from users.models import User


def create_user(email, first_name, last_name, is_staff, is_superuser, password):
    """
    Создает пользователя или получает существующего по указанным параметрам.

    Args:
        email (str): Email пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        is_staff (bool): Признак доступа к административной части сайта.
        is_superuser (bool): Признак суперпользователя (администратора).
        password (str): Пароль пользователя.

    Returns:
        User: Созданный или полученный пользователь.
    """
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
        }
    )
    user.set_password(password)
    user.save()
    return user


class Command(BaseCommand):
    help = 'Создает пользователей, группы и разрешения для доступа к моделям.'

    def handle(self, *args, **options):
        # Создать или получить пользователя-модератора
        moderator_user = create_user(
            email='moderator@mail.com',
            first_name='Модератор',
            last_name='Почта',
            is_staff=True,
            is_superuser=False,
            password='12345',
        )

        # Создать или получить пользователя-администратора
        admin_user = create_user(
            email='admin@mail.com',
            first_name='Администратор',
            last_name='Почта',
            is_staff=True,
            is_superuser=True,
            password='12345',
        )

        # Создать или получить простого пользователя
        simple_user = create_user(
            email='user@mail.com',
            first_name='Пользователь',
            last_name='Почта',
            is_staff=False,
            is_superuser=False,
            password='12345',
        )

        # Создать группы "Модераторы", "Пользователи" и "Администраторы"
        groups_data = [
            ('Модераторы', moderator_user, ['add', 'change', 'view']),
            ('Пользователи', simple_user, ['change', 'view']),
            ('Администраторы', admin_user, ['add', 'change', 'view']),
        ]

        app_models = [Clients, Transmission, Messages, BlogPost]  # Список всех моделей вашего приложения

        # Проход по списку данных о группах и действиях
        for group_name, user, actions in groups_data:
            # Создаем или получаем группу с указанным именем
            group, created = Group.objects.get_or_create(name=group_name)

            # Если пользователь указан, то добавляем его в группу
            if user:
                user.groups.add(group)

            # Проходим по списку моделей и действий, чтобы назначить разрешения для каждой модели
            for model in app_models:
                # Получаем ContentType для модели, чтобы использовать его для назначения разрешений
                content_type = ContentType.objects.get_for_model(model)

                # Проходим по списку действий для данной группы
                for action in actions:
                    # Создаем код разрешения для конкретной модели и действия
                    permission_codename = f'{action}_{model._meta.model_name}'

                    # Получаем или создаем разрешение с указанным кодом и ContentType
                    permission, created = Permission.objects.get_or_create(
                        codename=permission_codename,
                        content_type=content_type,
                    )

                    # Назначаем разрешение для группы, чтобы пользователи этой группы имели доступ к модели
                    group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Успешно созданы 3 пользователя и 3 группы'))
