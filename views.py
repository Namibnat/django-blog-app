"""Personal site view page"""

import datetime as dt

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .forms import PostForm
from .models import Post


class CoreBase(View):
    """Core classed based view for pages"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}
        year = dt.datetime.now().year
        if year == 2021:
            self.context['year'] = "2021"
        else:
            self.context['year'] = f"2021 - {year}"


class BlogList(CoreBase, ListView):
    """Home page view"""
    queryset = Post.objects.order_by('-publication_date')
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'


class PostBlogPost(CoreBase):
    """Post a new blog post"""

    def get(self, request):
        self.context['postform'] = PostForm()
        template_name = 'blog/post_blog_post.html'
        return render(request, template_name, self.context)

    def post(self, request):
        postform = PostForm(request.POST)
        if postform.is_valid():
            postform.save()
            return HttpResponseRedirect('/blog/posted/')
        else:
            self.context['postform'] = PostForm()
            template_name = 'blog/post_blog_post.html'
            return render(request, template_name, self.context)

class PostPosted(CoreBase):
    """For submitted blog posts"""

    def get(self, request):
        """For successful post of a blog post"""
        self.context['posted'] = "Blog posted successfully"
        template_name = 'blog/posted_success.html'
        return render(request, template_name, self.context)
