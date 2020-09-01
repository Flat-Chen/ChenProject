# -*- coding: utf-8 -*-
import scrapy
import time
import json
# from .items import WoniuhcSpider Item


class WoniuhcSpider(scrapy.Spider):
    name = 'woniuhc'
    allowed_domains = ['woniuhuoche.com']
    # start_urls = ['http://woniuhuoche.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(WoniuhcSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '',
        'MYSQL_DB': '',
        'MYSQL_TABLE': 'woniuhc',
        'MONGODB_SERVER': '',
        'MONGODB_DB': '',
        'MONGODB_COLLECTION': 'woniuhc',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://woniuhuoche.com/"
        yield scrapy.Request(
            url=url,
        )

    def parse(self, response):
        pass
