from rest_framework import serializers
from app.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'source', 'image_url', 'link_url', 'price', 'size', 'date_updated',
                  'date_created')
