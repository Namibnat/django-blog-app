"""Personal site view page"""

import datetime as dt

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
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


class BlogList(CoreBase):
    """Home page view"""

    def get(self, request, **kwargs):
        if request.user.is_superuser:
            queryset  = Post.objects.order_by('-pub_date')[:PAGE_JUMPS]
        else:
            queryset = Post.objects.order_by('-pub_date').filter(is_draft=False)[:PAGE_JUMPS]
        self.context['posts'] = queryset
        if queryset.count() >= PAGE_JUMPS:
            self.context['older'] = 1
        template_name = 'blog/post_list.html'
        return render(request, template_name, self.context)


class BlogArchive(CoreBase):

    def get(self, request, page):
        page = int(page)
        page_from = page * PAGE_JUMPS
        page_to = page_from + PAGE_JUMPS
        self.context['posts'] = Post.objects.order_by('-pub_date')[page_from: page_to]
        if not self.context['posts']:
            raise Http404
        if Post.objects.count() > page_to:
            self.context['older'] = page + 1 
        # Make 'newer' a string so '0' still valid in template
        self.context['newer'] = str(page - 1) 
        template_name = 'blog/post_list.html'
        return render(request, template_name, self.context)


class BlogDetail(CoreBase, DetailView):
    """Blog post detail view"""

    def get(self, request, slug):
        self.context['post'] = Post.objects.get(slug=slug)
        if request.user.is_superuser:
            posts = Post.objects.order_by('-pub_date')
        else:
            posts = Post.objects.order_by('-pub_date').filter(is_draft=False)
        pub_dates = []
        for post in posts:
            if post.pub_date > self.context['post'].pub_date:
                self.context['newer_post']  = post
            if post.pub_date < self.context['post'].pub_date:
                self.context['older_post'] = post
                break
            pub_dates.append(post.pub_date)
        template_name = 'blog/post_detail.html'
        return render(request, template_name, self.context)



class PostBlogPost(CoreBase):
    """Post a new blog post"""

    def get(self, request):
        if request.user.is_superuser:
            self.context['postform'] = PostForm()
            template_name = 'blog/post_blog_post.html'
            return render(request, template_name, self.context)
        else:
            raise Http404

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
