# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import redis
import time
import pymysql
import re
from scrapy_redis.spiders import RedisSpider

from che300_new.items import che300_price

# update_code = settings["UPDATE_CODE"]
update_code = time.strftime("%Y%m%d", time.localtime())

website = 'che300_futureprice'


pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
dbconn = pymysql.connect(host="192.168.1.94", database='for_android', user="dataUser94", password="94dataUser@2020",
                         port=3306, charset='utf8')
cur = dbconn.cursor()


class Che300FuturepriceSpider(RedisSpider):
    name = website
    allowed_domains = ['che300.com']
    redis_key = "che300_futureprice:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che300FuturepriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.c = con.client()

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_evaluation',
        'MYSQL_TABLE': 'che300_futureprice_update_test',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_evaluation',
        'MONGODB_COLLECTION': 'che300_futureprice_update_test',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.2.149:6379/15',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }
    }

    def structure_http(self, result):
        # "(2, 'price22.1863101943prov3city3mile0.1model11805year2006month6typedealer_price', 'D46B1542376EE8F1')"
        # "https://dingjia.che300.com/demo/evaluate/getPriceTrendSign?mile=3&sign=5061D26526E610B6&city=3&prov=3&year=2018&month=1&price=33.2503327331714&app_type=android_price&type=dealer_price&model=1146056"
        mile = re.search(r'mile=(.*?)&', result).group(1)
        city = re.search(r'city=(.*?)&', result).group(1)
        prov = re.search(r'prov=(.*?)&', result).group(1)
        year = re.search(r'year=(.*?)&', result).group(1)
        month = re.search(r'month=(.*?)&', result).group(1)
        model = re.search(r'&model=(.*)', result).group(1)

        meta = dict()
        meta['provid'] = prov
        meta['cityid'] = city
        meta['salesdescid'] = model
        meta['regDate'] = str(year) + "-" + str(month)
        meta['mile'] = mile
        return meta

    def parse(self, response):
        item = che300_price()
        datainfo = self.structure_http(response.url)
        item = dict(item, **datainfo)
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = response.url + "-" + update_code
        data = json.loads(response.text)['data']
        for dataitem in data:
            year = str(3 * data.index(dataitem))
            price = dataitem['eval_price']
            item[year] = price
        yield item
        list_len = self.c.llen('che300_futureprice:start_urls')
        if list_len > 0:
            start_url = self.c.lpop('che300_futureprice:start_urls')
            start_url = bytes.decode(start_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
            )
        else:
            print("*"*100)
            cur.execute("update che300_detection set che300_futureprice_update_test=1 WHERE che300_futureprice_update_test=0")
            dbconn.commit()
            # cur.close()
            # dbconn.close()

