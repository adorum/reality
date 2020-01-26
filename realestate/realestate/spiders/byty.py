# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from decimal import Decimal
from ..items import RealityPostItem


class BytySpider(scrapy.Spider):
    name = 'byty'
    allowed_domains = ['byty.sk']
    start_urls = ['https://www.byty.sk/3-izbove-byty/predaj/?p[location]=t10.t14&p[param1][to]=185000&p[param11][from]=65']

    def parse(self, response):
        for inzerat in response.css('div#inzeraty'):
            item = RealityPostItem()

            title = inzerat.css('h2 a::text').get()

            description = inzerat.css('.advertisement-content-p::text').get()
            description = re.sub("\n|\r", ' ', description.strip())

            image = inzerat.css('.advertisement-photo img::attr(src)').get()
            url = inzerat.css('h2 a::attr(href)').get()

            price = inzerat.css('.price .tlste::text').get()
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = price.strip()[:-1]
            price = price.replace(',', '.')

            size = 0

            date = inzerat.css('.date::text').get()
            date = date.replace(' ', '').replace('\n', '')
            if date[-2:] == '20':
                date = "{}20".format(date)
            date_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
            date = date_obj.isoformat()

            item['link_url'] = url
            item['image_url'] = image
            item['title'] = title
            item['description'] = description
            item['price'] = Decimal(price)
            item['size'] = size
            item['date_updated'] = date

            yield item

        next_page = response.css('div#nastranu li.active+li a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
