# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
# from .items import DasoucheModellistSpider Item


class DasoucheModellistSpider(scrapy.Spider):
    name = 'dasouche_modellist'
    # allowed_domains = ['dasouche.com']
    # start_urls = ['http://dasouche.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(DasoucheModellistSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.92',
        'MYSQL_DB': 'dasouche',
        'MYSQL_TABLE': 'dasouche_modellist',
        'MONGODB_SERVER': '192.168.1.92',
        'MONGODB_DB': 'dasouche',
        'MONGODB_COLLECTION': 'dasouche_modellist',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        # url = "https://aolai.souche.com/v1/shopApi/getShopCity.json"
        url = "https://aolai.souche.com/v2/indexApi/getHotBrandList.json"
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            dont_filter=True
        )

    def parse(self, response):
        data_list = json.loads(response.text)["data"]["items"]
        for data in data_list:
            brandCode = data["code"]
            brandName = data["name"]
            # brandImg = data["img"]
            meta = {
                "brandCode": brandCode,
                "brandName": brandName,
                # "brandImg": brandImg
            }
            series_url = f"https://aolai.souche.com/v1/menuApi/queryBrandSeriesGroupList.json?brand={brandCode}"
            response.meta.update(**meta)
            # print(meta)
            yield scrapy.Request(
                url=series_url,
                meta=response.meta,
                callback=self.parse_series,
                dont_filter=True
            )

    def parse_series(self, response):
        items_list = json.loads(response.text)["data"]["items"]
        for item in items_list:
            factoryName = item["key"]
            series_list = item["row"]
            for series in series_list:
                seriesCode = series["code"]
                seriesName = series["name"]
                meta = {
                    "factoryName": factoryName,
                    "seriesCode": seriesCode,
                    "seriesName": seriesName,
                }
                model_url = f"https://aolai.souche.com/v1/searchApi/getCarModelBySeries.json?series={seriesCode}&detailType=1"
                response.meta.update(**meta)
                yield scrapy.Request(
                    url=model_url,
                    meta=response.meta,
                    callback=self.parse_model,
                    dont_filter=True
                )

    def parse_model(self, response):
        items_list = json.loads(response.text)["data"]["items"]
        for item in items_list:
            year = item["key"]
            model_list = item["row"]
            for model in model_list:
                items = dict()
                modelCode = model["code"]
                modelName = model["name"]
                items["year"] = year
                items["modelCode"] = modelCode
                items["modelName"] = modelName
                items["brandCode"] = response.meta["brandCode"]
                items["brandName"] = response.meta["brandName"]
                items["factoryName"] = response.meta["factoryName"]
                items["seriesCode"] = response.meta["seriesCode"]
                items["seriesName"] = response.meta["seriesName"]
                items["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
                items["url"] = response.url+'_'+items["brandCode"]+items["seriesCode"]+items["modelCode"]+items["modelName"]
                # print(items)
                yield items






