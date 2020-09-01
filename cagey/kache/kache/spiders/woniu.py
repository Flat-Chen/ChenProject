# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy_redis.utils import bytes_to_str

from kache.items import woniuItem
from copy import deepcopy



class WoniuSpider(scrapy.Spider):
    name = 'woniu'
    # allowed_domains = ['woniuhuoche.com']
    # start_urls = ['http://woniuhuoche.com/']

    def __init__(self):
        super(WoniuSpider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.city_list = []

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'REDIS_URL': 'redis://192.168.1.92:6379/6',
        'MYSQL_TABLE': 'woniu',
        'MYSQL_DB': 'truck',
        'CrawlCar_Num': 1000000,
        'AUTOTHROTTLE_START_DELAY': 8,
        'DOWNLOAD_DELAY': 0,
    }

    def start_requests(self):
        url = "https://www.woniuhuoche.com/api/v1/truck/list?pageSize=10&page=1"
        yield scrapy.FormRequest(
            method="post",
            url=url,
            headers=self.headers,
            dont_filter=True,
        )

    def parse(self, response):
        json_data = json.loads(response.text)
        page_num = json_data["totalPage"]
        for num in range(1, page_num+1):
            next_url = f"https://www.woniuhuoche.com/api/v1/truck/list?pageSize=10&page={num}"
            yield scrapy.FormRequest(
                method="post",
                url=next_url,
                callback=self.parse_json_url,
                headers=self.headers,
                dont_filter=True,
            )

    def parse_json_url(self, response):
        item = woniuItem()
        detail_data = json.loads(response.text)
        for data in detail_data["data"]:
            data["title"] = data["newTitle"]
            item["brand"] = data["brand"].replace(r"#", "")
            item["shortdesc"] = data["title"]
            item["registeryear"] = data["cardtimeStr"]
            item["mileage"] = data["showmileage"]
            item["carid"] = data["id"]
            item["url"] = "https://www.woniuhuoche.com/"+data["cityFisrtLetter"]+'/'+str(data["woniuTruckId"])+".html"
            item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["pagetitle"] = data["title"]
            item["series"] = data["series"]
            item["price"] = data["price"]
            # item["level"] = data["emission"]
            item["let"] = data["emission"]
            item["hoursepower"] = data["power"]
            item["driveType"] = data["driveform"]
            item["color"] = data["color"]
            item['statusplus'] = item["url"]+'-'+str(item["price"])
            item["city"] = data["city"]
            item["level"] = data["model"]
            # print(item)
            yield scrapy.Request(
                url=item["url"],
                callback=self.parse_detail_url,
                meta={"item": deepcopy(item)},
                headers=self.headers
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        # item["engine"] = response.xpath("//dt[contains(text(),'发动机品牌')]/following-sibling::dd/text()").get()
        item["containerLong"] = response.xpath("//dt[contains(text(),'货箱长度')]/following-sibling::dd/text()").get()
        # item["model"] = response.xpath("//dt[contains(text(),'型号')]/following-sibling::dd/text()").get()
        item["fuel"] = response.xpath("//dt[contains(text(),'燃油类型')]/following-sibling::dd/text()").get()
        item["engine"] = response.xpath("//dt[contains(text(),'发动机品牌')]/following-sibling::dd/text()").get()
        # print(item)
        yield item
        # item["containerType"] = 货箱形式
        # item["let"] = 排放标准
        # item["pull"] = 准牵引总重量
        # item["speedBox"] = 变速箱
        # item["speedRatio"] = 后桥速比
        # item["trailer"] = 挂车形式
        # item["axes"] = 轴数
        # item["hangType"] = 悬挂形式
        # item["insurance1_date"] = 交强险过期时间
        # item["company"] = 公司
        # item["linkman"] = 联系人
        # item["store_location"] = 门店位置
        # item["province"] = 省会
        # item["public_time"] = 发布时间
        # item["carSourceid"] = 车源编号


