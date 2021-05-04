from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Post model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    # Use the slug field to build beautiful, SEO-friendly URLs for your blog posts
    # - added the unique_for_date parameter to this field so that you can build URLs for
    # - posts using their publish date and slug
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

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
