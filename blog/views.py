from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm


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
