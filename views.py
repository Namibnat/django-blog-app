"""Personal site view page"""

import datetime as dt

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.text import slugify

from .forms import PostForm
from .models import Post

PAGE_JUMPS = 3


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
    queryset = Post.objects.order_by('-pub_date')[:PAGE_JUMPS]
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = value
        context['older'] = 1
        return context


class BlogArchive(CoreBase):

    def get(self, request, page):
        page = int(page)
        page_from = page * PAGE_JUMPS
        page_to = page_from + PAGE_JUMPS
        self.context['posts'] = Post.objects.order_by('-pub_date')[page_from: page_to]
        if Post.objects.count() > page_to:
            self.context['older'] = page + 1 
        # Make 'newer' a string so '0' still valid in template
        self.context['newer'] = str(page - 1) 
        template_name = 'blog/post_list.html'
        return render(request, template_name, self.context)


class BlogDetail(CoreBase, DetailView):
    """Blog post detail view"""

    model = Post

    def get_slug_field(self, **kwargs):
        slug = super().get_slug_field(**kwargs)
        return slug

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = value
        return context


class PostBlogPost(CoreBase):
    """Post a new blog post"""

    def get(self, request):
        self.context['postform'] = PostForm()
        template_name = 'blog/post_blog_post.html'
        return render(request, template_name, self.context)

    def post(self, request):
        postform = PostForm(request.POST)
        if postform.is_valid():
            post = postform.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
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
