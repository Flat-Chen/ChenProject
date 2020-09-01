# -*- coding: utf-8 -*-
import scrapy
import demjson
import time
import json
import re
from copy import deepcopy
from lxml import etree
from baogang.items import NewsItem



class YicheNewsSpider(scrapy.Spider):
    name = 'yiche_news'
    # allowed_domains = ['yiche.com']
    # start_urls = ['http://yiche.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(YicheNewsSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '180.167.80.118',
        'MYSQL_DB': 'baogang',
        'MYSQL_PORT': 2502,
        'MYSQL_PWD': 'Baogang@2019',
        'MYSQL_TABLE': 'baogang_news',
        'MONGODB_SERVER': '180.167.80.118',
        'MONGODB_DB': 'baogang',
        'MONGODB_COLLECTION': 'baogang_news',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = 'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=master'
        yield scrapy.Request(
            url=url,
            dont_filter=True,
        )

    def parse(self, response):
        item = NewsItem()
        data = demjson.decode(response.text)
        for i in data['DataList']:
            item["brand"] = i['name']
            series_id = i['id']
            series_url = f'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=serial&pid={series_id}'
            yield scrapy.Request(
                url=series_url,
                callback=self.parse_series_list,
                meta={"item": deepcopy(item)},
                dont_filter=True
            )

    def parse_series_list(self, response):
        item = response.meta["item"]
        data = demjson.decode(response.text)
        for i in data:
            for c in i["child"]:
                item['series'] = c["name"]
                urlSpell = c["urlSpell"]
                news_url = f"http://car.bitauto.com/{urlSpell}/xinwen/"
                yield scrapy.Request(
                    url=news_url,
                    callback=self.parse_news_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_news_list(self, response):
        item = response.meta["item"]
        div_list = response.xpath("//div[@class='main-inner-section']//div[@class='inner-box']")
        for div in div_list:
            item["url"] = div.xpath("./a/@href").get()
            item["title"] = div.xpath(".//h2/a/text()").get()
            item["postd_date"] = div.xpath(".//span[@class='time']/text()").get()
            item["label"] = None
            item["data_source"] = "易车网"
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if item['url']:
                url = item["url"]
                news_id = re.findall("\d/(.*?).html", url)[0][:-3]
                view_num_url = f"http://newsapi.yiche.com/promotion-api/traffic/news/pv-total?callback=pvcommentsCallback&ids={news_id}"
                yield scrapy.Request(
                    url=view_num_url,
                    callback=self.parse_view_num,
                    meta={"item": deepcopy(item)}
                )
        next_url = response.xpath("//a[@class='next_on']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_news_list,
                meta={"item": deepcopy(item)}
            )

    def parse_view_num(self, response):
        item = response.meta["item"]
        text = response.text.replace('pvcommentsCallback(', '').replace(')', '')
        data = json.loads(text)
        # print(data)
        # print(type(data))
        # print("*"*100)
        if data["data"]:
            view_num = data["data"][0]["num"]
            item["view_num"] = view_num
            news_id = data["data"][0]["id"]
            reply_num_url = f"http://newsapi.yiche.com/comment/commentobject/getcommentcount?callback=pvcommentsCallback_cnewsid&commentIds=1-{news_id}"
            yield scrapy.Request(
                url=reply_num_url,
                callback=self.parse_reply_num,
                meta={"item": deepcopy(item)}
            )
        else:
            item["view_num"] = '0'
            item["reply_num"] = '0'
            # print(item)
            yield item

    def parse_reply_num(self, response):
        item = response.meta["item"]
        data = re.findall(':(\d+)},', response.text)
        if data:
            item["reply_num"] = data[0]
            # print("*"*100)
        else:
            item["reply_num"] = "0"
        yield item






