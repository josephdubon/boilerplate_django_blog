from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

register = template.Library()


####
# Register as simple tags
####

# A simple template tag that returns the number of posts published so far.=
@register.simple_tag
def total_posts():
    return Post.published.count()


# A simple template tag that displays the 5 most commented posts
@register.simple_tag
def get_most_commented_posts(count=5):
    # Build a QuerySet using the annotate() function to aggregate the
    # - total number of comments for each post.
    return Post.published.annotate(
        # use the Count aggregation function to store the number of comments
        # - in the computed field total_comments for each Post object.
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


####
# Register as inclusion_tags
####

# An inclusion tag that returns the 5 latest posts.
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }


####
# Register Template Filters
####

# A template filter to enable use of markdown .md syntax in blog posts and then converts
# - post contents to HTML in the templates
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
