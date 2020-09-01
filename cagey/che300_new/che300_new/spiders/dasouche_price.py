# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import redis
from scrapy_redis.spiders import RedisSpider

pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=14)
con = redis.Redis(connection_pool=pool)

website = 'dasouche_price'


class DasouchePriceSpider(RedisSpider):
    name = website
    redis_key = "dasouche_price:start_urls"
    # allowed_domains = ['dasouche.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(DasouchePriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.92',
        'MYSQL_DB': 'dasouche',
        'MYSQL_TABLE': 'dasouche_price',
        'MONGODB_SERVER': '192.168.1.92',
        'MONGODB_DB': 'dasouche',
        'MONGODB_COLLECTION': 'dasouche_price',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.1.241:6379/14',
        'DOWNLOAD_TIMEOUT': 8,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_new.middlewares.MoGuProxyMiddleware': 543,
            'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }

    }

    # def start_requests(self):
    #     # url = "https://aolai.souche.com/v1/shopApi/getShopCity.json"
    #     url = "https://aolai.souche.com/v2/indexApi/getHotBrandList.json"
    #     yield scrapy.Request(
    #         url=url,
    #         headers=self.headers,
    #         dont_filter=True
    #     )

    def structure_http(self, result):
        # https://aolai.souche.com//v2/evaluateApi/getEvaluateInfo.json?modelCode=140493&regDate=2020-3&mile=0.1&cityName=武汉&cityCode=01726
        meta = dict()
        model = re.search(r'modelCode=(.*?)&', result).group(1)
        mile = re.search(r'&mile=(.*?)&', result).group(1)
        city = result.split('cityCode=')[1]
        registerDate = re.search(r'regDate=(.*?)&', result).group(1)
        meta['model'] = model
        meta['registerDate'] = registerDate
        meta['mile'] = mile
        meta['city'] = city
        return meta

    def parse(self, response):
        json_data = json.loads(response.text)
        if json_data['data']['normal']['evaluateValue'] is not None:
            meta = self.structure_http(response.url)
            item = dict()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            # item["price"] = json.dumps(json_data["data"], ensure_ascii=False)
            item["normal_evaluateValue"] = json_data["data"]["normal"]["evaluateValue"]
            item["excellent_evaluateValue"] = json_data["data"]["excellent"]["evaluateValue"]
            item["good_evaluateValue"] = json_data["data"]["good"]["evaluateValue"]
            item["modelId"] = meta["model"]
            item["regDate"] = meta["registerDate"]
            item["cityId"] = meta["city"]
            item["mile"] = meta["mile"]
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            # print(item)
            if meta["model"] is None:
                item["modelId"] = response.url.split("modelCode=")[1].split("&")[0]
            if item["normal_evaluateValue"]:
                yield item


        # next_url = self.c.lpop('che300_price_daily_sh_city:start_urls')
        # if next_url:
        #     start_url = bytes.decode(next_url)
        #     yield scrapy.Request(
        #         url=start_url,
        #         callback=self.parse,
        #     )















