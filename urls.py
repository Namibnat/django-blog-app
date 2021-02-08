"""Urls for Me pages"""

from django.urls import path

from .views import (BlogList, PostBlogPost, PostPosted)

app_name = 'blog_posts'

urlpatterns = [
    path('', BlogList.as_view(),
         name='blog-home'),

    path('post-new-blog-post/',
         PostBlogPost.as_view(),
         name='post-blog-post'),

    path('posted/',
         PostPosted.as_view(),
         name='posted'),
]
