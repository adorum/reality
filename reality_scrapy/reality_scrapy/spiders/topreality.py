# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from decimal import Decimal
from ..items import RealityPostItem


class ToprealitySpider(scrapy.Spider):
    name = 'topreality'
    allowed_domains = ['topreality.sk']
    start_urls = [
        'https://www.topreality.sk/vyhladavanie-nehnutelnosti.html?cat=&form=1&type%5B%5D=802&searchType=string&obec=5%2C8%2C9%2C14%2C15%2C16%2C17%2C19%2C20%2C22&distance=&q=&cena_od=&cena_do=200000&vymera_od=200&vymera_do=&n_search=search&page=estate&gpsPolygon=',
        'https://www.topreality.sk/vyhladavanie-nehnutelnosti.html?cat=&form=1&type%5B%5D=201&type%5B%5D=202&type%5B%5D=204&type%5B%5D=205&type%5B%5D=206&type%5B%5D=207&searchType=string&obec=5%2C8%2C9%2C14%2C15%2C16%2C17%2C19%2C20%2C22&distance=&q=&cena_od=&cena_do=330000&vymera_od=200&vymera_do=&n_search=search&page=estate&gpsPolygon=']

    def parse(self, response):
        for inzerat in response.css('div.row.estate'):
            print("Parse inzerat")
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
            date_obj = datetime.datetime.strptime(date, '%d.%m.%Y')

            item['title'] = title
            item['link_url'] = url
            item['image_url'] = 'https://topreality.sk{0}'.format(image) if image else None
            item['price'] = Decimal(price)
            item['size'] = int(size)
            item['date_updated'] = date_obj.isoformat()

            yield item

        next_page = response.css(
            'div.paginatorContainerDown li.page-item.page-item-next:not(.d-none) a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
