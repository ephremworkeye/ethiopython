from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, year, month, day, slug):

    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish_day=day,
                             slug=slug,
                             status='published')
    return render(request, 'blog/post_detail.html', {'post': post})
