# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import pymysql
import pymongo
import redis
from datetime import datetime
from pandas.core.frame import DataFrame
# from che300_new.items import Che300PriceDaily
from scrapy_redis.spiders import RedisSpider

settings = {
    "redis_host": "192.168.1.241",
    "redis_db": 15
}

pool = redis.ConnectionPool(host=settings["redis_host"], port=6379, db=settings["redis_db"])
con = redis.Redis(connection_pool=pool)

# connection = pymongo.MongoClient('192.168.1.94', 27017)
# db = connection["residual_value"]
# collection = db["jzg_modellist2"]


class Jzg40citySpider(RedisSpider):
# class Jzg40citySpider(scrapy.Spider):
    name = 'jzg_40city'
    # allowed_domains = ['jzg.com']
    redis_key = "jzg_40city:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(Jzg40citySpider, self).__init__(**kwargs)
        self.c = con.client()
        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        # model_data = collection.find({}, {"brandname": 1, "familyname": 1, "familyid": 1, "brandid": 1, "modelid": 1, "make_year": 1, "next_year": 1, "_id": 0})
        # self.car_msg = DataFrame(list(model_data))

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'jzg',
        'MYSQL_TABLE': 'jzg_40city',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'jzg',
        'MONGODB_COLLECTION': 'jzg_40city',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': f'redis://{settings["redis_host"]}:6379/{settings["redis_db"]}',
        'DOWNLOAD_TIMEOUT': 8,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 8,
        'DOWNLOADER_MIDDLEWARES': {
            'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            # 'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }

    }

    # def start_requests(self):
    #     # url = "http://m.jingzhengu.com/sale-s10000128-r2019-3-1-m20000-c2401-y-j-h"
    #     # url = "http://m.jingzhengu.com/buy-s10000128-r2019-3-1-m20000-c2401-y-j-h"
    #     url = "https://qd.jingzhengu.com/appraise-s105084-r2017-9-1-m60000-c2301-ugongzh-m2.html"
    #     yield scrapy.Request(
    #         url=url,
    #         dont_filter=True
    #     )

    def structure_http(self, result):
        # 'http://m.jingzhengu.com/sale-s10000128-r2019-3-1-m20000-c2401-y-j-h'
        meta = dict()
        model = re.search(r'-s(.*?)-r', result).group(1)
        mile = re.search(r'-m(.*?)-c', result).group(1)
        city = re.search(r'-c(.*?)-', result).group(1)
        registerDate = re.search(r'-r(.*?)-m', result).group(1)
        type = re.search(r'com/(.*?)-s', result).group(1)
        type = 'sale' if type == 'appraise' else type
        meta['model'] = model
        meta['registerDate'] = registerDate
        meta['mile'] = mile
        meta['city'] = city
        meta['type'] = type
        return meta

    def parse(self, response):
        meta = self.structure_http(response.url)
        item = dict()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["modelid"] = meta["model"]
        item["regDate"] = meta["registerDate"]
        item["cityid"] = meta["city"]
        item["mile"] = meta["mile"]
        item["type"] = meta["type"]
        # item["status"] = response.url + "-" + str(datetime.now().year) + "-" + str(datetime.now().month)
        business_data = dict()
        personal_data = dict()
        if meta["type"] == "sale":
            # 车商报价数据
            price_list = response.xpath("//ul[@class='clearfix cl_carlist']//i/text()").getall()

            data_aprice_list = response.xpath('//div[@class="cl_carlist_top"]/@data-aprice').getall()
            # data_bprice_list = response.xpath('//div[@class="cl_carlist_top"]/@data-bprice').getall()
            data_cprice_list = response.xpath('//div[@class="cl_carlist_top"]/@data-cprice').getall()

            business_data["ordinary"] = {"range": f"{data_cprice_list[0]}-{data_aprice_list[0]}", "price": price_list[0]}
            business_data["good"] = {"range": f"{data_cprice_list[1]}-{data_aprice_list[1]}", "price": price_list[1]}
            business_data["superb"] = {"range": f"{data_cprice_list[2]}-{data_aprice_list[2]}", "price": price_list[2]}
            # 个人报价数据
            personal_data["ordinary"] = {"range": f"{data_cprice_list[3]}-{data_aprice_list[3]}", "price": price_list[3]}
            personal_data["good"] = {"range": f"{data_cprice_list[4]}-{data_aprice_list[4]}", "price": price_list[4]}
            personal_data["superb"] = {"range": f"{data_cprice_list[5]}-{data_aprice_list[5]}", "price": price_list[5]}

            for k, v in business_data.items():
                item["condition"] = k
                item["business_price"] = v["price"]
                item["business_range"] = v["range"]
                item["personal_price"] = personal_data[k]["price"]
                item["personal_range"] = personal_data[k]["range"]
                yield item
                # print(item)

        else:
            item["condition"] = "default"
            price_list = response.xpath("//div[@class='zw_sh_txt']/span/em/text()").getall()
            business_price = price_list[0:3]
            personal_price = price_list[3:6]
            item["business_price"] = business_price[-1]
            item["business_range"] = "-".join(business_price[:2])
            item["personal_price"] = personal_price[-1]
            item["personal_range"] = "-".join(personal_price[:2])
            yield item
            # print(item)

        next_url = self.c.lpop('jzg_40city:start_urls')
        if next_url:
            start_url = bytes.decode(next_url)
            yield scrapy.Request(
                url=start_url,
                headers=self.headers,
                callback=self.parse,
                dont_filter=True
            )

