# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
# from .items import LyhSpider Item


class LyhSpider(scrapy.Spider):
    name = 'lyh'
    # allowed_domains = ['lyh.com']
    # start_urls = ['http://lyh.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(LyhSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '127.0.0.1',
        'MYSQL_DB': 'luntan',
        'MYSQL_TABLE': 'lyh',
        'MONGODB_SERVER': '127.0.0.1',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'lyh',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "https://www.bumc.bu.edu/busm/directory/letter/a/"
        yield scrapy.Request(
            url=url,
            dont_filter=True
        )

    def parse(self, response):
        url_list = response.xpath("//ul[@class='profileList-letterNav']/li/a/@href").getall()
        print(url_list)
        for url in url_list:
            url = "https://www.bumc.bu.edu"+url
            yield scrapy.Request(
                url=url,
                callback=self.parse_list,
                dont_filter=True
            )

    def parse_list(self, response):
        li_list = response.xpath("//ul[@class='basic']/li")
        for li in li_list:
            url = li.xpath("./a/@href").get()
            name = li.xpath("./a/p[1]/text()").get()
            pos = li.xpath("./a/p[2]/text()").get()
            meta = {
                "name": name,
                "pos": pos,
            }
            response.meta.update(**meta)
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta=response.meta,
                dont_filter=True
            )

    def parse_detail(self, response):
        items = dict()
        items["email"] = response.xpath("//a[@class='profile-email']/text()").get()
        content = response.xpath("//div[@class='profile-bio col-sm-12 profile-grid']//text()").getall()
        items["content"] = ''.join(content).replace('\n', '').replace('\t', '')
        items["website"] = response.xpath("//li[@class='profile-website']//text()").get()
        items["website_url"] = response.xpath("//li[@class='profile-website']//a/@href").get()
        items["name"] = response.meta["name"]
        items["pos"] = response.meta["pos"]
        items["url"] = response.url
        items["statusplus"] = response.url
        print(items)
        yield items