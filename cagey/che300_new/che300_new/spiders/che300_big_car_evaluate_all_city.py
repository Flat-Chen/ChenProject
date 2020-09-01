# -*- coding: utf-8 -*-
import scrapy
import time
import json
import redis
import re
from scrapy_redis.spiders import RedisSpider
from che300_new.items import Che300_Big_Car_evaluate_Item

pool = redis.ConnectionPool(host='192.168.1.249', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
website = 'che300_big_car_evaluate_all_city'


class Che300BigCarEvaluateAllCitySpider(RedisSpider):
    name = website
    redis_key = "che300_big_car_evaluate_all_city:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(Che300BigCarEvaluateAllCitySpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {'Referer': 'https://m.che300.com',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        self.c = con.client()

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'truck',
        'MYSQL_TABLE': 'che300_big_car_evaluate_all_city_online',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'truck',
        'MONGODB_COLLECTION': 'che300_big_car_evaluate_all_city_online',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.1.249:6379/15',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'DOWNLOADER_MIDDLEWARES': {
            'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            # 'che300_new.middlewares.MoGuProxyMiddleware': 400,
            'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }

    }

    def parse(self, response):
        data = json.loads(response.text)
        if "eval_prices" in data["data"]:
            data_dict = data["data"]["eval_prices"]
        else:
            print(data)
            if not data["data"]:
                self.c.lpush('che300_big_car_evaluate_all_city:start_urls', response.url)
                print("push url in redis again!")
                return
            else:
                data_dict = data["data"]["eval_prices"]
        item = Che300_Big_Car_evaluate_Item()
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["url"] = response.url
        mile = re.search(r'mile=(.*)', response.url).group(1)
        item["goods_type"] = None
        item["mile"] = mile
        brand_id = re.search(r'brand_id=(.*?)&', response.url).group(1)
        series_id = re.search(r'series_id=(.*?)&', response.url).group(1)
        model_id = re.search(r'model_id=(.*?)&', response.url).group(1)
        prov_id = re.search(r'prov_id=(.*?)&', response.url).group(1)
        city_id = re.search(r'city_id=(.*?)&', response.url).group(1)
        reg_date = re.search(r'&reg_date=(.*)', response.url).group(1)
        item["brand_id"] = brand_id
        item["series_id"] = series_id
        item["model_id"] = model_id
        item["prov_id"] = prov_id
        item["city_id"] = city_id
        item["reg_date"] = reg_date
        item["default_car_condition"] = data["data"]["default_car_condition"]
        for i in data_dict:
            ci = i["condition"]
            item["{}_dealer_high_buy_price".format(ci)] = i["dealer_high_buy_price"]
            item["{}_dealer_low_buy_price".format(ci)] = i["dealer_low_buy_price"]
            item["{}_dealer_high_sold_price".format(ci)] = i["dealer_high_sold_price"]
            item["{}_dealer_buy_price".format(ci)] = i["dealer_buy_price"]
            item["{}_dealer_low_sold_price".format(ci)] = i["dealer_low_sold_price"]
            item["{}_dealer_sold_price".format(ci)] = i["dealer_sold_price"]

        item["statusplus"] = response.text + item["url"]
        yield item

        # print(item)
        next_url = self.c.lpop('che300_big_car_evaluate_all_city:start_urls')
        print("*" * 100+'next_url')
        if next_url:
            next_url = bytes.decode(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True
            )
