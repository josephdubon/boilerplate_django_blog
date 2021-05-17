from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import Post


# First subclass the Feed class of the syndication framework
class LatestPostFeed(Feed):
    # The title, link, and description attributes correspond to the
    # - <title>, <link>, and <description> RSS elements, respectively.
    title = "My Blog"
    link = reverse_lazy('blog:post_list')  # reverse_lazy() to generate the URL for the link attribute
    description = 'New posts of my blog.'

    # The items() method retrieves the objects to be included in the feed. You are retrieving only the
    # - last five published posts for this feed.
    def items(self):
        return Post.published.all()[:5]

    #  The item_title() and item_description() methods will receive each object returned by items()
    #  - and return the title and description for each item.
    def item_title(self, item):
        return item.title

    # - Use the truncatewords built-in template filter to build the description of the blog post with the
    # -  first 30 words.
    def item_description(self, item):
        return truncatewords(item.body, 30)
