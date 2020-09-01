# -*- coding: utf-8 -*-
import scrapy
import time
import json
from baogang.items import YicheKoubeiItem


class YicheModelPaihangSpider(scrapy.Spider):
    name = 'yiche_model_paihang'
    # allowed_domains = ['car.bitauto.com']
    # start_urls = ['http://car.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(YicheModelPaihangSpider, self).__init__(**kwargs)
        self.counts = 0
        self.model_list = ['/weixingche/paihang/', '/xiaoxingche/paihang/', '/jincouxingche/paihang/', '/zhongxingche/paihang/', '/zhongdaxingche/paihang/', '/haohuaxingche/paihang/', '/mpv/paihang/', '/suv/paihang/', '/paoche/paihang/', '/mianbaoche/paihang/', '/pika/paihang/', '/keche/paihang/', '/kache/paihang/']

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.120',
        'MYSQL_DB': 'baogang',
        'MYSQL_TABLE': 'yiche_rank',
        # 'MONGODB_SERVER': '',
        # 'MONGODB_DB': '',
        'MONGODB_COLLECTION': 'yiche_rank',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        for url in self.model_list:
            url = f'http://car.bitauto.com{url}'
            yield scrapy.Request(
                url=url,
                dont_filter=True
            )

    def parse(self, response):
        item = YicheKoubeiItem()
        li_list = response.xpath("//ol[@class='list']/li")
        ranking_dic = {li.xpath('./a/text()').get(): li.xpath('./i/text()').get() for li in li_list}
        item["model"] = response.xpath("//li[@class='active']//text()").get()
        item["tag"] = '易车车型关注排行榜'
        item["ranking"] = json.dumps(ranking_dic, ensure_ascii=False)
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(item)
        yield item

