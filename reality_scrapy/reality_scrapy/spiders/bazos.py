# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from decimal import Decimal
from ..items import RealityPostItem


class BazosSpider(scrapy.Spider):
    name = 'bazos'
    allowed_domains = ['reality.bazos.sk']
    start_urls = ['https://reality.bazos.sk/predam/byt/?hledat=3+izbov%C3%BD&rubriky=reality&hlokalita=83102&humkreis=5&cenaod=&cenado=185000&Submit=H%C4%BEada%C5%A5&kitx=ano']

    @staticmethod
    def parse_date(s):
        parsed = s[s.find("[") + 1:s.find("]")]
        parsed = parsed.replace(' ', '').replace('\n', '')
        return parsed

    def parse(self, response):
        for inzerat in response.css('table.inzeraty'):
            item = RealityPostItem()

            title = inzerat.css('td .nadpis a::text').get()

            description = inzerat.css('td .popis::text').get()
            description = re.sub("\n|\r", ' ', description.strip())

            image = inzerat.css('td a img::attr(src)').get()
            url = inzerat.css('td a::attr(href)').get()
            url = "https://reality.bazos.sk{}".format(url)

            price = inzerat.css('td .cena b::text').get()
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = price.strip()[:-1]
            price = price.replace(',', '.')

            size = 0

            date = inzerat.css('.velikost10::text').getall()
            if len(date) == 2:
                date = BazosSpider.parse_date(date[1])
            else:
                date = BazosSpider.parse_date(date[0])

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

        next_page = response.css('.strankovani b + a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
