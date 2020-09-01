# -*- coding: utf-8 -*-
from copy import deepcopy
import time
from random import randint

import scrapy
# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()
from scrapy.mail import MailSender
import logging
import json
from koubei_new.items import Chehang168Item

website = 'chehang168'


class Chehang168TestSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['*']
    # start_urls = ['http://www.chehang168.com']
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_COLLECTION': website,
        'MONGODB_DB': 'koubei',
        'CrawlCar_Num': 1000000,
        'CONCURRENT_REQUESTS': 8,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': randint(1, 3),
    }

    def __init__(self, **kwargs):
        super(Chehang168TestSpider, self).__init__(**kwargs)
        self.counts = 0

        self.DEVICE_ID = "ad8a7d65a063ede2a3ec035f96ca81cc"
        self._uab_collina = "157051961723139799923937"
        self.soucheAnalytics_usertag = "43wfR4SfIL"
        self.U = "1497797_d51aecb5183ede2691a53a97a963906c"
        self.UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

        self.cookies = {
            'DEVICE_ID': f'{self.DEVICE_ID}',
            '_uab_collina': f'{self._uab_collina}',
            'soucheAnalytics_usertag': f'{self.soucheAnalytics_usertag}',
            'U': f'{self.U}',
        }

        self.headers = {
            # 'User-agent': "{}".format(self.UserAgent),
            'cookies': f"DEVICE_ID={self.DEVICE_ID}; _uab_collina={self._uab_collina}; soucheAnalytics_usertag={self.soucheAnalytics_usertag}; U={self.U}"
            # 'cookies': "DEVICE_ID={}; soucheAnalytics_usertag={}; U={}".format(self.DEVICE_ID, self.soucheAnalytics_usertag, self.U)
        }

    def start_requests(self):
        logging.log(level=logging.INFO, msg=json.dumps(self.cookies))
        url = "http://www.chehang168.com/index.php?c=index&m=allBrands"
        print(self.headers)
        return [scrapy.Request(url=url, cookies=self.cookies,
                               headers=self.headers)]

    def parse(self, response):
        item = Chehang168Item()
        li_list = response.xpath("//*/div/ul[@class='cyxx_wrap_ull pt_1']/li")
        for li in li_list:
            a_list = li.xpath("./a")
            for a in a_list:
                item["brandcode"] = a.xpath("./@href").get()
                item["brandname"] = a.xpath("./text()").get()
                list_url = "http://www.chehang168.com" + item["brandcode"]
                yield scrapy.Request(
                    url=list_url,
                    callback=self.detail_url,
                    meta={"item": deepcopy(item)},
                    cookies=self.cookies,
                    headers=self.headers,
                    dont_filter=True
                )

    def detail_url(self, response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@class='sx_tiaojian cyxx_div_ull']//li")
        for li in li_list:
            item["familyname"] = li.xpath("./a/text()").get()
            item["familycode"] = li.xpath("./a/@href").get()
            detail_url = "http://www.chehang168.com" + item["familycode"]
            self.headers["Referer"] = detail_url
            print(self.headers)
            print("*"*100)
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                meta={"item": deepcopy(item)},
                cookies=self.cookies,
                headers=self.headers,
                dont_filter=True
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        cars = response.xpath("//*[@class='ch_carlistv3']/li")
        # print(item)
        if not cars:
            print("-"*100)
        for car in cars:
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['title'] = car.xpath("div/h3/a/text()").extract_first()
            item['guideprice'] = car.xpath("div/h3/b/text()").extract_first()
            item['price'] = car.xpath("div/span/b/text()").extract_first().replace("万", "")
            item['store'] = car.xpath("p[@class='c3']/a/text()").extract_first()

            item['desc1'] = car.xpath("p[@class='c1']/text()[1]").extract_first()
            item['desc2'] = car.xpath("p[@class='c2']/text()").extract_first()
            item['time'] = car.xpath("p[@class='c3']/cite[1]/text()").extract_first()
            item['desc3_2'] = car.xpath("p[@class='c3']/cite[2]/text()").extract_first()
            item['desc3_3'] = car.xpath("p[@class='c3']/cite[3]/text()").extract_first()
            item['status'] = item["title"] + "-" + item["desc1"] + "-" + item["store"]
            print(item)
