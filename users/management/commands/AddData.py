from django.core.management import BaseCommand
from users.management.commands.AddGroupAndUser import Command as AddGroupAndUser
from users.management.commands.CreateClients import Command as CreateContent
from users.management.commands.CreateMessages import Command as CreateMessages


class Command(BaseCommand):
    help = 'Запускает все команды из users'

    def handle(self, *args, **options):
        # Вызываем команду AddGroupAndUser
        add_group_and_user_command = AddGroupAndUser()
        add_group_and_user_command.handle(*args, **options)

        # Вызываем команду CreateContent
        create_content_command = CreateContent()
        create_content_command.handle(*args, **options)

        # Вызываем команду CreateMessages
        create_content_command = CreateMessages()
        create_content_command.handle(*args, **options)
