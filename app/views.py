from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.serializers.post import PostSerializer
from app.models import Post
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from realestate.realestate.spiders.topreality import ToprealitySpider
from realestate.realestate.spiders.nehnutelnosti import NehnutelnostiSpider

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
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner()
    runner.crawl(ToprealitySpider)
    runner.crawl(NehnutelnostiSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return Response(status.HTTP_200_OK)
