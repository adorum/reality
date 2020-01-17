# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pydispatch import dispatcher
from scrapy import signals
from app.models import RealityPost


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
        scrapy_item = RealityPost()
        scrapy_item.title = item['title']
        scrapy_item.source = spider.name
        scrapy_item.price = item['price']
        scrapy_item.size = item['size']
        scrapy_item.image_url = item['image_url']
        scrapy_item.link_url = item['link_url']
        scrapy_item.date_updated = item['date_updated']

        existing_post = RealityPost.objects.filter(link_url=item['link_url'])
        if len(existing_post) == 0:
            scrapy_item.save()

        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
