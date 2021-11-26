from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag
from .forms import PostEmailShareForm, PostCommentForm
from .models import Post, Comment

# Create your views here.


def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html',
                  {'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, slug):

    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status='published')

    comments = post.comments.filter(is_active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = PostCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = PostCommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:3]

    return render(request, 'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'related_posts': related_posts,
                   })


def post_share(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False
    if request.method == 'POST':
        form = PostEmailShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ephremwube@gmail.com', [cd['to']])
            sent = True
    else:
        form = PostEmailShareForm()
    return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    query = request.GET.get('query', '')
    results = Post.published.annotate(
        search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'blog/search.html', {'query': query, 'results': results})
