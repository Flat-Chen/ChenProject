# -*- coding: utf-8 -*-
import scrapy
import time
import json
from baogang.items import BaogangItem


class YicheRankSpider(scrapy.Spider):
    name = 'yiche_rank'
    allowed_domains = ['car.bitauto.com']
    # start_urls = ['http://car.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(YicheRankSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.120',
        'MYSQL_DB': 'baogang',
        'MYSQL_TABLE': 'yiche_rank',
        'MONGODB_SERVER': '192.168.1.92',
        'MONGODB_DB': 'baogang',
        'MONGODB_COLLECTION': 'yiche_rank',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://car.bitauto.com/"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
            # callback=
        )

    def parse(self, response):
        div_list = response.xpath("//div[@class='main-inner-section focus-ranking js-tab-container']//div[@class='row ranking2']/div[@class='col-xs-4']")
        for div in div_list:
            item = BaogangItem()
            title = div.xpath(".//h3/a/text()").get()
            li_list = div.xpath(".//ul/li")
            count = 1
            ranking_list = list()
            for li in li_list:
                data = dict()
                data["series"] = li.xpath("./a/text()").get()
                data["category"] = li.xpath("./span/text()").get()
                data["ranking"] = count
                count += 1
                ranking_list.append(data)
            ranking_list = json.dumps(ranking_list, ensure_ascii=False)
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["ranking"] = ranking_list
            item["model"] = title
            if "万" not in title:
                item["tag"] = "按级别排行"
            else:
                item["tag"] = "按价位排行"
            # print(item)
            yield item
        print("*"*100)
        buy_car_url = "http://shanghai.bitauto.com/"
        yield scrapy.Request(
            url=buy_car_url,
            callback=self.parse_buy_car,
            dont_filter=True
        )

    def parse_buy_car(self, response):
        print("*"*100)
        model_list = response.xpath("//div[@id='tab-djdmsmc']/div[1]//li/text()").getall()
        first_list = response.xpath("//div[@id='tab-djdmsmc']/div[2]//ul/li[@class='name']/a/text()").getall()
        div_list = response.xpath("//div[@id='tab-djdmsmc']/div[2]/div")
        count = 0
        for div in div_list:
            item = BaogangItem()
            # buy_car_data = dict()
            other_car_list = list(div.xpath("./ul/li/a/text()").getall())
            model = model_list[count]
            first_car = first_list[count].replace(" ", "")
            count += 1
            other_car_list.insert(0, first_car)
            tmp_dic = {car: other_car_list.index(car)+1 for car in other_car_list}
            # for car in other_car_list:
            #     buy_car_data = dict()
            #     buy_car_data["series"] = car
            #     buy_car_data["ranking"] = other_car_list.index(car) + 1
            #     tmp_list.append(buy_car_data)
            item["tag"] = "大家都买什么车"
            item["model"] = model
            item["ranking"] = json.dumps(tmp_dic, ensure_ascii=False)
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(item)
            yield item



