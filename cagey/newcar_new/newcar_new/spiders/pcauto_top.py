# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
# from .items import PcautoTopSpider Item


class PcautoTopSpider(scrapy.Spider):
    name = 'pcauto_top'
    allowed_domains = ['pcauto.com']
    # start_urls = ['http://pcauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(PcautoTopSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'newcar',
        'MYSQL_TABLE': 'pcauto_top',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'newcar',
        'MONGODB_COLLECTION': 'pcauto_top',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        key_list = [93, 94, 105, 111, 112, 134, 135, 74, 131, 132, 133, 70, 72, 71, 73, 76, 110, 0]
        for key in key_list:
            url = f"https://price.pcauto.com.cn/top/k{str(key)}.html"
            print(url)
            yield scrapy.Request(
                url=url,
                dont_filter=True
            )

    def parse(self, response):
        info_list = response.xpath("//div[@class='info']")
        for info in info_list:
            item = dict()
            item["sname"] = info.xpath(".//p[@class='sname']//text()").get()
            item["sid"] = info.xpath(".//p[@class='sname']//@href").get().replace('/', '')
            item["brand"] = info.xpath(".//p[@class='col col1'][1]/text()").get().replace('品牌：', '')
            item["level"] = info.xpath(".//p[@class='col'][1]/text()").get().replace('级别：', '')
            item["redmark"] = info.xpath(".//span[@class='fl red rd-mark'][1]/text()").get().replace('热度', '')
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = item["brand"] + '-' + item["sname"] + '-' + item["redmark"]
            # print(item)
            yield item

        next_url = response.xpath("//a[@class='next']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            print(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True
            )


