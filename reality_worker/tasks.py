from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from reality_worker.celery import app
from reality_scrapy.reality_scrapy.spiders.topreality import ToprealitySpider


@app.task
def create_random_user_accounts():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ToprealitySpider)
    process.start()
    return 0
