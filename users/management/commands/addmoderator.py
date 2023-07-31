from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from catalog.models import Product
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='moderator@mail.com',
            defaults={
                'first_name': 'moderator',
                'last_name': 'Mail',
                'is_staff': True,
                'is_superuser': False,
            }
        )

        user.set_password('12345')
        user.save()

        # Создать группу "Модераторы" или получить ее, если она уже существует
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        # Получить ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получить право доступа "catalog.add_product"
        can_add_product_permission, created = Permission.objects.get_or_create(
            codename='add_product',
            content_type=content_type,
        )

        # Получить или создать право доступа "change_product"
        can_change_product_permission, created = Permission.objects.get_or_create(
            codename='change_product',
            content_type=content_type,
        )

        # Получить или создать право доступа "view_product"
        can_view_product_permission, created = Permission.objects.get_or_create(
            codename='view_product',
            content_type=content_type,
        )

        # Добавить права доступа к группе "Модераторы"
        moderator_group.permissions.add(can_add_product_permission)
        moderator_group.permissions.add(can_change_product_permission)
        moderator_group.permissions.add(can_view_product_permission)

        # Добавить пользователя в группу "Модераторы"
        user.groups.add(moderator_group)
