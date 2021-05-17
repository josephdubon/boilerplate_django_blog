from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector

from taggit.models import Tag

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post


# List posts view
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # Start tag with default value of None.
    tag = None
    # If there is a given tag slug, you get the Tag object with the given slug.
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Filter the posts by the ones that contain the given tag.
        object_list = object_list.filter(tags__in=[tag])
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
            'tag': tag,
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
    # List of active comments for this specific post.
    # QuerySet to retrieve all active comments for this post:
    comments = post.comments.filter(active=True)
    new_comment = None
    #  Instead of building a QuerySet for the Comment model
    #  directly, you leverage the post object to retrieve the related Comment objects.
    if request.method == "POST":
        # A comment was posted
        # build a form instance with comment_form = CommentForm() if the view is
        # called by a GET request. If the request is done via POST, you instantiate
        # the form using the submitted data and validate it using the is_valid() method.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but do not save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Now save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts based off tags.
    # Retrieve a Python list of IDs for the tags of the current post.
    # - ass flat=True to it to get single values such as
    # - [1, 2, 3, ...] instead of one-tuples such as [(1,), (2,), (3,) ...].
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get all posts that contain any of these tags, excluding the current post itself.
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Use the Count aggregation function to generate a calculated field —same_tags— that
    # - contains the number of tags shared with all the tags queried.
    # - order the result by the number of shared tags (descending order) and by publish
    # - to display recent posts first for the posts with the same number of shared tags.
    # You slice the result to retrieve only the first four posts.
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html', {
                      'post': post,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form,
                      'similar_posts': similar_posts,
                  }
                  )


# Email post form
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # If form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # If form fields were validated
            cd = form.cleaned_data
            # Retrieve the absolute path of the post using its get_absolute_url() method.
            # - You use this path as an input for request.build_absolute_uri() to build a
            # - complete URL, including the HTTP schema and hostname.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            # Send the email to the email address contained in the to field of the form
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })


# 'Full Text' search form
def post_search(request):
    # Instantiate the SearchForm form
    form = SearchForm()
    query = None
    results = []

    # To check whether the form is submitted, you look for the query parameter
    # - in the request.GET dictionary.
    if 'query' in request.GET:
        # send the form using the GET method instead of POST, so that the resulting
        # - URL includes the query parameter and is easy to share.
        form = SearchForm(request.GET)
        # When the form is submitted, you instantiate it with the submitted GET data, and
        # - verify that the form data is valid.
        if form.is_valid():
            query = form.cleaned_data['query']
            #  If the form is valid, you search for published posts with a custom
            #  - SearchVector instance built with the title and body fields.
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request,
                  'blog/post/search.html',
                  {
                      'form': form,
                      'query': query,
                      'results': results,
                  }
                  )
