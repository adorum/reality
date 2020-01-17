from django.urls import path, include
from app.views import RealityPostList

urlpatterns = [
    path('', RealityPostList.as_view(), name='post-list')
]
