# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import pymongo
from pandas.core.frame import DataFrame
# from .items import PcautoPowerSpider Item
connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["newcar"]
collection = db["pcauto_tmp"]
model_data = collection.find({}, {"carid": 1, "brandname": 1, "factoryname": 1, "familyname": 1, "brandid": 1,"_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('carid')


class PcautoPowerSpider(scrapy.Spider):
    name = 'pcauto_power_minBtPrice'
    allowed_domains = ['pcauto.com']
    # start_urls = ['https://price.pcauto.com.cn/price/api/v1/serialgroup/serial_group_bt_data/r3-m85355']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(PcautoPowerSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'newcar',
        'MYSQL_TABLE': 'pcauto_power_newtext',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'newcar',
        'MONGODB_COLLECTION': 'pcauto_minBTprice',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        # s = ["sg4640", "sg11962", "sg1584", "sg7280", "sg7659", "sg11962"]
        # for rows in s:
        for index, rows in self.car_msg_df_new .iterrows():
            carid = rows['carid']
            # familyid = rows
            url = f"https://price.pcauto.com.cn/price/api/v1/serialgroup/serial_group_bt_data/r3-m{carid}"
            meta = {
                "carid": carid,
                "brandname": rows['brandname'],
                "factoryname": rows['factoryname'],
                "familyname": rows['familyname'],
                "brandid": rows['brandid']
            }
            yield scrapy.Request(
                url=url,
                meta={"meta": meta}
            )

    def parse(self, response):
        meta = response.meta["meta"]
        item = dict()
        item["carid"] = meta["carid"]
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        minBtPrice = json_data['data']['minBtPrice']
        if minBtPrice != None:
            item["minBtPrice"] = minBtPrice
            # try:
            #     item["score"] = response.xpath("//div[@class='scoreAll scoreNotAll']/text()").get().replace("\r\n", "")
            # except :
            #     item["score"] = response.xpath("//div[@class='scoreAll ']/text()").get().replace("\r\n", "")
            # c_list = response.xpath("//div[@class='processBar']//div[@class='processBar-txt']/span/text()").getall()
            # score_list = response.xpath("//div[@class='processBar']//div[@class='processBar-txt']/p/text()").getall()
            # config = dict(zip(c_list, score_list))
            # item["config"] = json.dumps(config, ensure_ascii=False)
            item["brandname"] = meta["brandname"]
            item["factoryname"] = meta["factoryname"]
            item["familyname"] = meta["familyname"]
            item["brandname"] = meta["brandname"]
            item["brandid"] = meta["brandid"]
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = item["url"] + '-' + str(item['minBtPrice'])

            print(item)
            yield item

