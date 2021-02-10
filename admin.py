"""Add blog to Django Admin"""

from django.contrib import admin

from .models import Post, BlogImage

admin.site.register(Post)
admin.site.register(BlogImage)
