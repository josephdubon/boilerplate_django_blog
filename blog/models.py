from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Published custom post manager model
class PublishedManager(models.Manager):
    # Returns the QuerySet that will be executed / custom manager
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# Post model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    # Use the slug field to build beautiful, SEO-friendly URLs for your blog posts
    # - added the unique_for_date parameter to this field so that you can build URLs for
    # - posts using their publish date and slug -> unique_for_date ensures there will be only one post
    # - with a slug for a given date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # Many-to-one relationship for author, meaning that each post is written by a user, and a user
    # - can write any number of posts
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    # This datetime indicates when the post was published. You use Django's timezone now method as the default value.
    # - This returns the current datetime in a timezone-aware format.
    publish = models.DateTimeField(default=timezone.now)
    # This datetime indicates when the post was created. Since you are using auto_now_add here, the date will be
    # - saved automatically when creating an object.
    created = models.DateTimeField(auto_now_add=True)
    # This datetime indicates the last time the post was updated. Since you are using auto_now here, the date will
    # - be updated automatically when saving an object.
    updated = models.DateTimeField(auto_now=True)
    # Set default status of post to 'draft'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # Default manager
    objects = models.Manager()
    # Custom manager
    published = PublishedManager()
    # Add the taggit TaggableManager for tag functionality
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # You will use the get_absolute_url() method in
    # - your templates to link to specific posts.
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ]
        )


# Comment model
class Comment(models.Model):
    # ForeignKey to associate a comment with a single post.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Boolean field that you will use to manually deactivate inappropriate/unwanted comments.
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
