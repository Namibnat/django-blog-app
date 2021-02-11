"""Models for blog"""

from django.db import models


class Post(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    intro = models.TextField()
    body = models.TextField()
    pub_date = models.DateField()
    is_draft = models.BooleanField(default=True)
    added = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    custom_css = models.TextField(blank=True)
    custom_javascript = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}"


class BlogImage(models.Model):
    """Add images to use in blog posts

    For now, images aren't related to any one
    blog post, and can just be updloaded in admin
    """

    image = models.ImageField(upload_to='post/')
