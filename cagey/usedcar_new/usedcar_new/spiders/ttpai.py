# -*- coding: utf-8 -*-
import scrapy
import time
import json
from usedcar_new.items import GuaziItem
import time
import logging

website ='ttpai'

class TtpaiSpider(scrapy.Spider):
    name = website
    allowed_domains = ["ttpai.cn"]

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(TtpaiSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'ttpai_online',
        'WEBSITE': 'ttpai',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'ttpai',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "https://www.ttpai.cn/quanguo/list"
        yield scrapy.Request(
            url=url,
        )

    # get car list
    def parse(self, response):
        datacheck = len(response.xpath("//html").extract_first())
        if datacheck > 20000:
            # as list
            for href in response.xpath('//li[@class="item"]'):
                urlbase = href.xpath("a/@href").extract_first()
                datasave1 = href.extract()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)

    # get car info
    def parse_car(self, response):
        if response.status == 200:
            # datasave
            if 'datasave1' in response.meta:
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            status = "sold"
            price = response.xpath('//strong[@class="s-orange"]/text()')
            price = ".".join(price.re('\d+')) if price else "zero"
            datetime ="zero"

            # item loader
            item = GuaziItem()
            item['url'] = response.url
            item['grab_time'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            sold_date = response.xpath('//p[@class="closing-date"]/text()').get()
            if sold_date:
                item["sold_date"] = sold_date.replace("成交", "")
            item['status'] = response.url + "-" + str(price) + "-" + str(status)+"-"+str(datetime)
            item['statusplus'] = response.url + "-" + str(price) + "-" + str(status) + "-" + str(datetime)
            # item["totalcheck_desc"] = response.xpath("//div[@class='right-car-info']/div[4]/span/text()").get()
            item['pagetime'] = datetime
            # item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            item['datasave'] = datasave1 + response.xpath('//html').extract_first()

            yield item
            # print(item)
