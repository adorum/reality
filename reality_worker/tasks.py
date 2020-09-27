from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from reality_worker.celery import app
from reality_scrapy.reality_scrapy.spiders.topreality import ToprealitySpider
from reality_scrapy.reality_scrapy.spiders.nehnutelnosti import NehnutelnostiSpider
from reality_scrapy.reality_scrapy.spiders.bazos import BazosSpider


@app.task
def create_random_user_accounts():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ToprealitySpider)
    process.crawl(NehnutelnostiSpider)
    process.crawl(BazosSpider)
    process.start()
    return 0
