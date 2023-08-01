from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def mediapath(image_path):
    media_url = getattr(settings, 'MEDIA_URL', '')
    full_path = '{}{}'.format(media_url, image_path)
    return full_path

