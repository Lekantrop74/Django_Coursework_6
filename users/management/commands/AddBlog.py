from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from random import choice

from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Создает контент для модели BlogPost'

    def handle(self, *args, **options):
        users = get_user_model().objects.all()
        blog_data = []

        for i in range(10):
            title = f"Заголовок блога {i + 1}"
            content = f"Содержимое блога {i + 1}"
            is_published = choice([True, False])
            views_count = 0
            blog = {
                'title': title,
                'content': content,
                'preview': None,
                'is_published': is_published,
                'views_count': views_count,
            }
            blog_data.append(blog)

        for data in blog_data:
            title = data['title']
            slug = slugify(title)

            existing_blog = BlogPost.objects.filter(slug=slug).first()
            if existing_blog is None:
                owner = choice(users)  # Выбираем случайного владельца из всех пользователей
                BlogPost.objects.create(
                    title=title,
                    slug=slug,
                    content=data['content'],
                    preview=data['preview'],
                    owner=owner,
                    is_published=data['is_published'],
                    views_count=data['views_count']
                )

        self.stdout.write(self.style.SUCCESS('Успешно создано 10 объектов модели BlogPost.'))
