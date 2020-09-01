# -*- coding: utf-8 -*-
import scrapy
import time
from baogang.items import XingzhengItem


class Minzheng2Spider(scrapy.Spider):
    name = 'minzheng2'
    allowed_domains = ['xzqh.mca.gov.cn']
    # start_urls = ['http://xzqh.mca.gov.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_USER': 'dataUser94',
        'MYSQL_PWD': '94dataUser@2020',
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_PORT': 3306,
        'MYSQL_DB': 'xingzhengqu',
        'MYSQL_TABLE': 'xingzhengqu2',
        # 'REDIS_URL': 'redis://192.168.1.241:6379/10',
        # 'SCHEDULER_PERSIST': False,
        # 'MONGODB_SERVER': '180.167.80.118',
        # 端口号，默认是27017
        # 'MONGODB_PORT': 1206,
        # 'MONGODB_DB': 'baogang',
        # 'MONGODB_COLLECTION': 'ouyeel_new',
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 5,
        # 'LOG_LEVEL': 'INFO',
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            # 'baogang.middlewares.SeleniumMiddleware': 300,
            # 'baogang.middlewares.SeleniumFirefoxMiddleware': 301,

        },
    }

    def __init__(self, **kwargs):
        super(Minzheng2Spider, self).__init__(**kwargs)
        self.detail_url = 'https://www.ouyeel.com/buyer-ng/resource/resourceData?resourceType=10&resId=1392404789'
        self.k = []

    def start_requests(self):
        url_list = "http://xzqh.mca.gov.cn/advancedDataQueryDefaut?shengji=-1&diji=-1&xianji=-1&tp=4&leiXing=-1"
        yield scrapy.Request(
            url=url_list,
        )

    def parse(self, response):
        tr_list = response.xpath("//table[@class='info_table']//tr")[2:]
        for tr in tr_list:
            item = XingzhengItem()
            item["shiji"] = tr.xpath("./td[1]/a/text()").get()
            item["diji"] = tr.xpath("./td[2]/a/text()").get()
            item["xianji"] = tr.xpath("./td[3]/a/text()").get()
            item["zhudi"] = tr.xpath("./td[4]//text()").get()
            item["xingzheng_level"] = tr.xpath("./td[5]//text()").get().replace("\t", "").replace("\n", "").replace("\r", "").replace(" ", "")
            item["area_type"] = tr.xpath("./td[6]//text()").get().replace("\t", "").replace("\n", "").replace("\r", "").replace(" ", "")
            item["people"] = tr.xpath("./td[8]/text()").get()
            item["area"] = tr.xpath("./td[9]/text()").get()
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(item)
            yield item

