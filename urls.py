"""Urls for Me pages"""

from django.urls import path

from .views import (BlogArchive, BlogDetail, BlogList,
                    PostBlogPost, PostPosted)

app_name = 'blog-posts'

urlpatterns = [
    path('post-new-blog-post/',
         PostBlogPost.as_view(),
         name='post-blog-post'),

    path('posted/',
         PostPosted.as_view(),
         name='posted'),

    path('post/<slug:slug>/',
         BlogDetail.as_view(),
         name='blog-detail'),

    path('post/archive/<int:page>/',
         BlogArchive.as_view(),
         name='blog-archive'),

    path('', BlogList.as_view(),
         name='blog-home'),
]
