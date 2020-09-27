from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.serializers.post import PostSerializer
from app.models import Post
from reality_worker.tasks import create_random_user_accounts


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.order_by('-date_updated')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def clear_posts(request):
    Post.objects.all().delete()
    return Response(status.HTTP_200_OK)


@api_view(['POST'])
def scrape_posts(request):
    create_random_user_accounts.delay()
    return Response(status.HTTP_200_OK)
