"""Models for blog"""

from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            default=slugify(title))
    intro = models.TextField()
    body = models.TextField()
    publication_date = models.DateField()
    added = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class Image(models.Model):
    """Add images to blog posts

    A blog post can have zero to
    many images, and so the name given
    should be able to map clearly to
    a url that can be used in the post"""

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='image')
    image = models.ImageField()