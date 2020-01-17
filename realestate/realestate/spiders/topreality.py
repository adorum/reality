# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ..items import RealityPostItem

class ToprealitySpider(scrapy.Spider):
    name = 'topreality'
    allowed_domains = ['topreality.sk']
    start_urls = ['https://www.topreality.sk/vyhladavanie-nehnutelnosti-1.html?type%5B0%5D=104&form=1&obec=5&cena_do=250000&n_search=search&gpsPolygon=&searchType=string']

    def parse(self, response):
        for inzerat in response.css('div.row.estate'):
            item = RealityPostItem()

            title = inzerat.css('h2 a::text').get().strip()
            url = inzerat.css('h2 a::attr(href)').get()
            image = inzerat.css('div.img-square-wrapper img::attr(data-src)').get()

            price = inzerat.css('strong.price::text').get()
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = price.strip()[:-1]
            price = price.replace(',', '.')

            size = inzerat.css('.areas .value::text').get()
            size = size.strip()[:-1]
            size = size.strip()

            date = inzerat.css('li.date::text').get()
            date_time_obj = datetime.datetime.strptime(date, '%d.%m.%Y')

            item['title'] = title
            item['link_url'] = url
            item['image_url'] = 'https://topreality.sk{0}'.format(image) if image else None
            item['price'] = float(price)
            item['size'] = int(size)
            item['date'] = date_time_obj.isoformat()

            yield item

        next_page = response.css('div.paginatorContainerDown li.page-item.page-item-next:not(.d-none) a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
