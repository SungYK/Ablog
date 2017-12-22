from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category
import markdown

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                            created_time__month=month)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    #Override get() to increase num of view in Post
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    
    #content to markdown
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
        return post
    
'''
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })
'''
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body, extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    return render(request, 'blog/detail.html', context={'post':post})

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def about(request):
    return render(request, 'blog/about.html', context={})
