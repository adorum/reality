from django.urls import path
from app.views import post_list, clear_posts, scrape_posts

urlpatterns = [
    path('posts/', post_list, name='posts'),
    path('clear/', clear_posts, name='posts'),
    path('scrape/', scrape_posts, name='posts')
]
