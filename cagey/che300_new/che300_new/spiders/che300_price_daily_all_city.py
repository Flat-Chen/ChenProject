# -*- coding: utf-8 -*-
import logging
import time
import re
import redis
import pymysql
import scrapy
import json

from che300_new.items import Che300PriceDaily
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
dbconn = pymysql.connect(host="192.168.1.94", database='for_android', user="dataUser94", password="94dataUser@2020",
                         port=3306, charset='utf8')
cur = dbconn.cursor()

website = 'che300_price_daily_all_city'

class Che300PriceDailyAllCitySpider(RedisSpider):
    name = website
    # allowed_domains = ['che300.com']
    redis_key = "che300_price_daily_all_city:start_urls"
    # start_urls = ['http://che300.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(Che300PriceDailyAllCitySpider, self).__init__(**kwargs)
        self.c = con.client()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://m.che300.com/wechat_01",
        }

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        return scrapy.Request(url, headers=self.headers, dont_filter=True)


    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'che300',
        'MYSQL_TABLE': 'che300_price_daily_all_city',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_price_daily_all_city',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.2.149:6379/15',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 1,
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_new.middlewares.MoGuProxyMiddleware': 543,
            'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }

    }

    def structure_http(self, result):
        # 'https://dingjia.che300.com/app/EvalResult/allProvPrices?callback=jQuery18309705734921018707_1534391096144&
        # 'brand=127&series=1264&model=17575&regDate=2017-4&mile=6.33'
        meta = dict()
        brand = re.search(r'&brand=(.*?)&', result).group(1)
        series = re.search(r'&series=(.*?)&', result).group(1)
        model = re.search(r'&model=(.*?)&', result).group(1)
        registerDate = re.search(r'&regDate=(.*?)&', result).group(1)
        # mile = re.search(r'&mile=(.*?)', result).group(1)
        mile = result.split('mile=')[1]
        meta['brand'] = brand
        meta['series'] = series
        meta['model'] = model
        meta['registerDate'] = registerDate
        meta['mile'] = mile
        return meta

    def parse(self, response):
        data = response.text.replace('jQuery18309705734921018707_1534391096144(', '').replace(')', '')
        meta = self.structure_http(response.url)
        item = dict()
        json_data = json.loads(data)["success"]["prices"]
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["brand"] = meta["brand"]
        item["series"] = meta["series"]
        item["salesdescid"] = meta["model"]
        item["regDate"] = meta["registerDate"]
        item["mile"] = meta["mile"]
        item["prices"] = json.dumps(json_data, ensure_ascii=False)
        # print(item)
        yield item
        next_url = self.c.lpop('che300_price_daily_all_city:start_urls')
        if next_url:
            start_url = bytes.decode(next_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                headers=self.headers
            )
