# -*- coding: utf-8 -*-
import scrapy
from lxml import etree

import time
import json
from copy import deepcopy
import re
import uuid
import demjson
from baogang.items import YicheKoubeiItem


class YicheKoubeiWeiduSpider(scrapy.Spider):
    name = 'yiche_koubei_weidu'

    # allowed_domains = ['dianping.bitauto.com']
    # start_urls = ['http://dianping.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YicheKoubeiWeiduSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '180.167.80.118',
        'MYSQL_DB': 'baogang',
        'MYSQL_PORT': 2502,
        'MYSQL_PWD': 'Baogang@2019',
        # 'MYSQL_SERVER': '192.168.2.120',
        # 'MYSQL_DB': 'baogang',
        'MYSQL_TABLE': 'yiche_koubei_tag',
        # 'MONGODB_SERVER': '',
        # 'MONGODB_DB': '',
        'MONGODB_COLLECTION': 'yiche_koubei_tag',
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
        item = YicheKoubeiItem()
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
        # print(response.url)
        for i in data:
            for c in i["child"]:
                detail_url = f"http://car.bitauto.com/{c['urlSpell']}/"
                item["serise"] = c["showName"]
                item["familyname"] = c["name"]
                item["usage"] = c["urlSpell"]
                item["familynameid"] = c["id"]
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_like_url,
                    meta={"item": deepcopy(item), "urlSpell": c['urlSpell']}
                )

    def parse_like_url(self, response):
        item = response.meta["item"]
        urlSpell = response.meta['urlSpell']
        ul_list = response.xpath("//div[@id='divSimilarSerial']//ul")
        like_dic = {ul.xpath("./li[1]//text()").get(): ul.xpath("./li[2]//text()").get() for ul in ul_list}
        item["like_series"] = json.dumps(like_dic, ensure_ascii=False)
        tag_url = f"http://dianping.bitauto.com/{urlSpell}/koubei/"
        yield scrapy.Request(
            url=tag_url,
            callback=self.parse_tag_url,
            meta={"item": deepcopy(item)}
        )

    def parse_tag_url(self, response):
        item = response.meta["item"]
        # print(response.url)
        tag_list = response.xpath("//div[@class='cm-list-tag-box']/span/text()").getall()
        series_score = response.xpath("//span[@class='cm-list-score-val']/text()").get()
        if series_score:
            series_score = series_score.replace(' ', '').replace('\n', '')

        item["series_score"] = "暂无评分" if series_score is None else series_score
        item["url"] = response.url
        # item["_id"] = item["_id"] = uuid.uuid4().__str__()
        if len(tag_list) > 0:
            tag_list = [i.replace(' ', '').replace('\n', '') for i in tag_list]
            item["tag_list"] = json.dumps(tag_list, ensure_ascii=False)
        # print(item)
        yield item
