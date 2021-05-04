from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# List posts view
class PostListView(ListView):
    # Use a specific QuerySet instead of retrieving all objects.
    # - Instead of defining a queryset attribute, you could have specified model = Post
    # - and Django would have built the generic Post.objects.all() QuerySet for you.
    queryset = Post.published.all()
    # Use the context variable posts for the query results.
    # - The default variable is object_list if you don't specify any context_object_name
    context_object_name = 'posts'
    # Paginate the result, displaying three objects per page.
    paginate_by = 3
    # Use a custom template to render the page. If you don't set a default
    # template, ListView will use blog/post_list.html
    template_name = 'blog/post/list.html'


# Detail post view
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request,
                  'blog/post/detail.html',
                  {'post': post}
                  )
