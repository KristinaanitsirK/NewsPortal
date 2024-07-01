from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    queryset = Post.objects.order_by('title')
    template_name = 'news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'

