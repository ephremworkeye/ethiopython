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
