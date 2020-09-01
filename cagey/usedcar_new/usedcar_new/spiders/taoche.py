# -*- coding: utf-8 -*-
import scrapy
import time
import json
import logging
from usedcar_new.items import GanjiItem

website = 'taoche'
class TaocheSpider(scrapy.Spider):
    name = website
    allowed_domains = ['taoche.com']
    start_urls = [
        "https://hefei.taoche.com/all/?orderid=5&direction=2&page=1"
    ]

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(TaocheSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'taoche',
        'WEBSITE': 'taoche',
        'CrawlCar_Num': 1000000,
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'taoche',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

    }

    def parse(self, response):
        for href in response.xpath('//div[@class="header-city-province-text"]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)

    def list_parse(self, response):
        for href in response.xpath('//div[@id="container_base"]/ul/li'):
            url = href.xpath('.//div[@class="item_img"]/a[1]/@href').extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback= self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="pages-next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            url = response.urljoin(url)
            yield scrapy.Request(url,callback=self.list_parse)

    def parse_car(self, response):
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="detail-over-btn clearfix"]/em')
        status = "sold" if status else "sale"

        price = response.xpath('//input[@id="hidPrice"]/@value')
        price = str(price.extract_first()) if price else "zero"

        datetime = response.xpath('//div[@class="tab-menu margin-md"]/i/text()')
        datetime = str(datetime.extract_first()[5:]) if datetime else "zero"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
        item['pagetime'] = datetime
        item['datasave'] = response.xpath('//html').extract_first()
        item["statusplus"] = item['status']
        yield item
        # print(item)