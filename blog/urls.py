from django.urls import path
from . import views

# Define app namespace
#  - You will refer to your blog URLs easily by using the namespace
#  - followed by a colon and the URL name, for example:
#  - blog:post_list and blog:post_detail
app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]
