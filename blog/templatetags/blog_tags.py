from django import template
from django.db.models import Count
from ..models import Post, Comment

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def total_comments():
    return Comment.objects.count()


@register.inclusion_tag('blog/most_commented_posts.html')
def most_commented_posts(count=3):
    commented_posts = Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]

    return {'commented_posts': commented_posts}
