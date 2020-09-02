# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import pymongo
from pandas.core.frame import DataFrame

connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["chexiu"]
collection = db["chexiu_car"]
model_data = collection.find({}, {"vehicle_id": 1, "vehicle": 1, "brandname": 1, "brand_id": 1, "familyname": 1,
                                  "family_id": 1, "factoryname": 1, '_id': 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


class ChexiuspiderSpider(scrapy.Spider):
    name = 'chexiuSpider'
    allowed_domains = ['chexiu.com']

    start_urls = ['https://sz.chexiu.com/index.php?r=site/api/depList&isshowall=1']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(ChexiuspiderSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'chexiu',
        'MONGODB_COLLECTION': 'chexiu_price',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def parse(self, response):
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        city_list = json_data['data']['hotList']
        for i in city_list:
            city_domain = i['domain']
            city_name = i['name']
            for index, rows in self.car_msg_df_new.iterrows():
                meta = {
                    'vehicle_id': rows['vehicle_id'],
                    'vehicle': rows['vehicle'],
                    'brandname': rows['brandname'],
                    'brand_id': rows['brand_id'],
                    'familyname': rows['familyname'],
                    'family_id': rows['family_id'],
                    'factoryname': rows['factoryname'],
                    'city_name': city_name
                }
                vehicle_id = rows['vehicle_id']
                url = f'https://{city_domain}.chexiu.com/car/{vehicle_id}.html'
                # url = 'https://www.chexiu.com/car/177163.html'
                yield scrapy.Request(url=url, callback=self.parse_price,
                                     meta={"meta": meta})

    def parse_price(self, response):
        meta = response.meta["meta"]
        try:
            test = response.xpath('//div[@class="J_priceListBox"]')
            min_clean_price = "".join(response.xpath('//div[@class = "clean-price"]/em/text()').extract())
            guide_price = "".join(response.xpath('//div[@class = "clean-price"]/del/text()').extract())
            min_all_price = "".join(response.xpath('//li[@class = "nprice"]/em/text()').extract())
            trs = response.xpath('//tr[@data-priceid]')
            for tr in trs:
                item = dict()
                region = "".join(tr.xpath('.//td[@class="n-area"]/text()').extract()).strip()
                clean_price = "".join(tr.xpath('.//em[@class="b-line pr J_tip"]/text()').extract()).strip()
                purchase_tax = "".join(tr.xpath('.//td[@class="n-gprice"]//text()').extract()).strip()
                license_price = "".join(tr.xpath('.//td[class="n-sprice"]//text()').extract()).strip()
                insurance = "".join(tr.xpath('.//span[@class="J_insSelectVal"]//text()').extract()).strip()
                boutique_suite = "".join(tr.xpath('.//em[@class="b-line J_tip"]//text()').extract()).strip()
                boutique_suite = re.sub(" ", "", boutique_suite)
                all_price = "".join(tr.xpath('.//span[@class="price-box"]/em/text()').extract()).strip()

                item['brandname'] = meta['brandname']
                item['brand_id'] = meta['brand_id']
                item['familyname'] = meta['familyname']
                item['family_id'] = meta['family_id']
                item['vehicle'] = meta['vehicle']
                item['vehicle_id'] = meta['vehicle_id']
                item['factoryname'] = meta['factoryname']
                item['city_name'] = meta['city_name']
                item['region'] = region
                item['min_clean_price'] = min_clean_price
                item['guide_price'] = guide_price
                item['min_all_price'] = min_all_price
                item['clean_price'] = clean_price
                item['purchase_tax'] = purchase_tax
                item['license_price'] = license_price
                item['insurance'] = insurance
                item['boutique_suite'] = boutique_suite
                item['all_price'] = all_price
                item['url'] = response.url
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['status'] = response.url + '-' + guide_price
                print(item)
                yield item

        except:
            ss
