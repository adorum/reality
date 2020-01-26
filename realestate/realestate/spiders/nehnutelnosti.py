# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from decimal import Decimal
from ..items import RealityPostItem


class NehnutelnostiSpider(scrapy.Spider):
    name = 'nehnutelnosti'
    allowed_domains = ['nehnutelnosti.sk']
    start_urls = ['https://www.nehnutelnosti.sk/3-izbove-byty/predaj/?p%5Border%5D=15&p%5Blocation%5D=t14.t10&p%5Bparam1%5D%5Bfrom%5D=&p%5Bparam1%5D%5Bto%5D=190000&p%5Bparam11%5D%5Bfrom%5D=68&p%5Bparam11%5D%5Bto%5D=']

    def parse(self, response):
        for inzerat in response.css('div#inzeraty .advertisement-box-image-main:not(.project-column-1)'):
            item = RealityPostItem()

            title = inzerat.css('h2 a::text').get()

            description = inzerat.css('.truncate-text::text').get()
            description = re.sub("\n|\r", ' ', description.strip())

            image = inzerat.css('picture data-img::attr(data-src)').get()
            url = inzerat.css('h2 a::attr(href)').get()

            price = inzerat.css('div.advertisement-price-panel::text').get()
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = price.strip()[:-1]
            price = price.replace(',', '.')

            size = inzerat.css('.location-text span::text').get()
            if size:
                size = size.strip()[:-2]
                size = size.strip()
            else:
                size = 0

            date = inzerat.css('span.advertisement-add-date::text').get()
            date_obj = datetime.datetime.strptime(date.replace(' ', '').replace('\n', ''), '%d.%m.%Y')
            date = date_obj.isoformat()

            item['link_url'] = url
            item['image_url'] = image
            item['title'] = title
            item['description'] = description
            item['price'] = Decimal(price)
            item['size'] = size
            item['date_updated'] = date

            yield item

        next_page = response.css('div.paginatorContainerDown li.page-item.page-item-next:not(.d-none) a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
