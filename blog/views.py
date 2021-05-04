from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# List posts view
def post_list(request):
    object_list = Post.published.all()
    # Instantiate the Paginator class with the number of
    # objects that you want to display on each page.
    paginator = Paginator(object_list, 3)
    # Get the page GET parameter, which indicates the
    # current page number.
    page = request.GET.get('page')
    # Obtain the objects for the desired page by
    # calling the page() method of Paginator.
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, you retrieve
        # the first page of results.
        posts = paginator.page(1)
    except EmptyPage:
        # If this parameter is a number higher than the last page
        # of results, you retrieve the last page.
        posts = paginator.page(paginator.num_pages)
        # Pass the page number and retrieved objects to the template.
    return render(
        request,
        'blog/post/list.html',
        {
            'page': page,
            'posts': posts,
        },
    )


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
