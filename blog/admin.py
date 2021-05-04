from django.contrib import admin
from .models import Post


# The @admin.register() decorator performs the same
# - function as the admin.site.register()
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # The list_display attribute allows you to set the fields of your
    # - model that you want to display on the administration object list page.
    list_display = (
        'title',
        'slug',
        'author',
        'publish',
        'status',
    )

    # This includes a right sidebar that allows you to filter the results
    # - by the fields included in the list_filter attribute.
    list_filter = (
        'status',
        'created',
        'publish',
        'author',
    )

    # This adds a search bar to the top of the admin page, filters
    # - through 'title' and 'body'
    search_fields = (
        'title',
        'body',
    )

    # As you type the title of a new post, the slug field is filled
    # - in automatically, based off the 'title' field.
    prepopulated_fields = {
        'slug': ('title',)
    }

    # The author field is now displayed with a lookup widget that can scale much
    # - better than a drop-down select input when you have thousands of users.
    raw_id_fields = ('author',)

    # This will add navigation links to navigate through a date hierarchy
    date_hierarchy = 'publish'

    # You can also see that the posts are ordered by STATUS and PUBLISH
    # - columns by default.
    ordering = ('status', 'publish')
