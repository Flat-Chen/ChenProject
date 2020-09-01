# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from newcar_new.items import AutohomeItem_price

website = 'chehang168_price'


class Chehang168PriceSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['chehang.com']
    # start_urls = ['http://chehang.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(Chehang168PriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.wxsession = "a058c706dfeadcd6f59c78687ce141ec"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'newcar_price',
        'MYSQL_TABLE': 'chehang168_price',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'newcar_price',
        'MONGODB_COLLECTION': 'chehang168_price',
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = f"https://xcx.chehang168.com/site/index?U=08_EF5e_aFMFnkzFBk&sign=440d35311227c54f393502751b8b9cad&t=1587095384&version=v1.0&wxsession={self.wxsession}"
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            dont_filter=True
        )

    def parse(self, response):
        json_data = json.loads(response.text)["data"]["allPbrands"]
        for data in json_data:
            group = data["t"]
            group_brand = data["l"]
            for brand in group_brand[:1]:
                brandId = brand["pbid"]
                brandName = brand["name"]
                meta = {
                    "brandId": brandId,
                    "brandName": brandName,
                    "group": group
                }
                response.meta.update(**meta)
                series_url = f"https://xcx.chehang168.com/site/pseries?U=08_EF5e_aFMFnkzFBk&wxsession={self.wxsession}&pbid={brandId}"
                yield scrapy.Request(
                    url=series_url,
                    callback=self.parse_series,
                    meta=response.meta,
                    headers=self.headers,
                    dont_filter=True
                )

    def parse_series(self, response):
        json_data = json.loads(response.text)["data"]
        for data in json_data:
            group_series = data["pseries"]
            for series in group_series[:1]:
                seriesId = series["psid"]
                seriesName = series["psname"]
                meta = {
                    "seriesId": seriesId,
                    "seriesName": seriesName,
                }
                response.meta.update(**meta)
                series_url = f"https://xcx.chehang168.com/site/carList?U=08_EF5e_aFMFnkzFBk&wxsession={self.wxsession}&psid={seriesId}&page=1"
                yield scrapy.Request(
                    url=series_url,
                    callback=self.parse_area,
                    meta=response.meta,
                    headers=self.headers,
                    dont_filter=True
                )

    def parse_area(self, response):
        json_data = json.loads(response.text)["data"]
        if json_data["province"]:
            province_list = json_data["province"][0]["data"]
            for province in province_list:
                area_name = province["name"]
                if '全部地区' not in area_name:
                    # area_url = f"https://xcx.chehang168.com/site/carList?U=08_zax5_aFMFnkzFBk&page=1&province={area_name}&psid={response.meta['seriesId']}&sign=8739650e40962f933dd63c54c01ddd6c&t=1587109465&version=v1.0&wxsession=a058c706dfeadcd6f59c78687ce141ec"
                    area_url = f"https://xcx.chehang168.com/site/carList?U=08_EF5e_aFMFnkzFBk&province={area_name}&psid={response.meta['seriesId']}&version=v1.0&wxsession={self.wxsession}"
                    meta = {
                        "area": area_name
                    }
                    response.meta.update(**meta)
                    yield scrapy.Request(
                        url=area_url,
                        callback=self.parse_detail_data,
                        meta=response.meta,
                        headers=self.headers,
                        dont_filter=True
                    )
        else:
            print("无数据...")

    def parse_detail_data(self, response):
        json_data = json.loads(response.text)["data"]["data"]
        for data in json_data:
            item = dict()
            item["title"] = data["title"]
            item["mode"] = data["mode"]
            item["shop_name"] = data["name"]
            item["modelId"] = data["uid"]
            item["price"] = data["price"]
            item["configure"] = data["configure"]
            item["post_date"] = data["pdate"]
            item["title2"] = data["title2"]
            print(item)














