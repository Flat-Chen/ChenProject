# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json
from usedcar_new.items import GanjiItem


class AnxinpaiSpider(scrapy.Spider):
    name = 'anxinpai'
    # allowed_domains = ['haicj.com']
    # start_urls = ['http://www.haicj.com/bidcar']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AnxinpaiSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'anxinpai',
        'WEBSITE': 'anxinpai',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar',
        'MONGODB_COLLECTION': 'anxinpai',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://www.haicj.com/getAllAuction"
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        hc_data = json.loads(response.text)
        # print("*" * 100)
        # ids = response.xpath('//*[@id="auction_list"]/option[contains(text(), "安心拍")]/@value').getall()
        # print("*"*100)
        baseurl = 'http://www.haicj.com/bidcar?px=&id='
        # print(ids)
        for id in hc_data:
            url = baseurl + id["id"]
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_list,
            )

    def parse_list(self, response):
        lis = response.xpath('//*[@id="buycarList"]/dl/dd/a/@href').extract()
        for li in lis:
            url = response.urljoin(li)
            yield scrapy.Request(url, callback=self.parse_car)

        # next page
        next_page = response.xpath(u'//a[contains(text(), "下一页")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            if url != response.url:
                yield scrapy.Request(url, self.parse_list)

    def parse_car(self, response):
        # print response.url
        # count
        self.counts += 1
        # logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="sold"]')
        status = "sold" if status else "sale"

        price = response.xpath('//div[@class="carshowJgBox"]/strong/text()')
        price = re.findall(r'(\d.*)', price.extract_first()) if price else "zero"

        datetime = "zero"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        # item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = 'anxinpai'
        item['status'] = response.url + "-" + str(price[0]) + "-" + str(status) + "-" + str(datetime)
        item['pagetime'] = datetime
        item['datasave'] = response.xpath('//html').extract_first()
        item['statusplus'] = item['status']

        yield item
        # print(item)
