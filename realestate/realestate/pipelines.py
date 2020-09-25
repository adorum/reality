# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pydispatch import dispatcher
from scrapy import signals
from app.models import Post
from scrapy.exceptions import DropItem


class DatabasePipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
        )

    def process_item(self, item, spider):
        if any(word in item['title'].lower() for word in ['prenájom', 'prenajom', 'kúpim', 'kupim']):
       # if any(item['title'].lower() in s for s in ['prenájom', 'prenajom', 'kúpim', 'kupim']):
            raise DropItem('Neriesim kupim a prenajom')

        try:
            existing_post = Post.objects.get(title=item['title'])
        except Post.DoesNotExist:
            existing_post = None

        if existing_post:
            if int(existing_post.price) != int(item['price']):
                existing_post.price = item['price']
                existing_post.date_updated = item['date_updated']
                existing_post.save()
        else:
            scrapy_item = Post()
            scrapy_item.title = item['title']
            scrapy_item.source = spider.name
            scrapy_item.price = item['price']
            scrapy_item.size = item['size']
            scrapy_item.image_url = item['image_url']
            scrapy_item.link_url = item['link_url']
            scrapy_item.date_updated = item['date_updated']
            scrapy_item.save()

        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
