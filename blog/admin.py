from django.contrib import admin

from blog.models import BlogPost


# Register your models here.
@admin.register(BlogPost)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["title"]