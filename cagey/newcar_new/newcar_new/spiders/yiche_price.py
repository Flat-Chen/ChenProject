# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
# import demjson
from pprint import pprint
from bs4 import BeautifulSoup

# import requests

from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider
from newcar_new.items import AutohomeItem_price

website = 'yiche_price'


class YichePriceSpider(RedisSpider):
# class YichePriceSpider(scrapy.Spider):
    name = website
    redis_key = "yiche_price:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(YichePriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        }
        with open('./tools/yiche.json', 'r') as f:
            data = f.read()
        self.brand_dic = json.loads(data)


    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'newcar_price',
        'WEBSITE': 'yiche_price',
        'MYSQL_TABLE': 'yiche_price',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'newcar_price',
        'MONGODB_COLLECTION': 'yiche_price',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.1.241:6379/15',

    }

    # def start_requests(self):
    #     self.brand_dic = {'alphard':
    #                 {'brandid': '7',
    #                 'brandname': '丰田',
    #                 'seriesname': '埃尔法',
    #                 'serise_id': '3088'}}
    #     for k, v in self.brand_dic.items():
    #         url = f"http://car.bitauto.com/{k}/baojia/c0/"
    #         yield scrapy.Request(
    #             url=url,
    #             headers=self.headers,
    #             meta={"series_pinyin": k}
    #         )

    def parse(self, response):
        series_pinyin = response.url.split('/')[3]
        city_li = response.xpath("//ul[@class='layer-txt-list']/li")
        for li in city_li:
            prov_Name = li.xpath(".//a/text()").get()
            if '全国' not in prov_Name:
                city_url = li.xpath(".//a/@href").get()
                city_url = response.urljoin(city_url)
                meta = {
                    "prov_Name": prov_Name,
                    "series_pinyin": series_pinyin,
                }
                response.meta.update(**meta)
                yield scrapy.Request(
                    url=city_url,
                    callback=self.parse_dealer,
                    headers=self.headers,
                    meta=response.meta,
                    dont_filter=True,
                )

    def parse_dealer(self, response):
        div_list = response.xpath("//div[@class='row offer-list']")
        for div in div_list:
            dealer_url = div.xpath(".//h6/a/@href").get()
            dealer_address = div.xpath(".//p[@class='add']/span/@title").get()
            city = div.xpath(".//p[@class='market-price']/following-sibling::p/text()").get()
            city = city.split(" ")[0] if " " in city else city
            meta = {
                "address": dealer_address,
                "city": city
            }
            response.meta.update(**meta)
            dealer_url = dealer_url.split('?')[0]
            yield scrapy.Request(
                url=dealer_url,
                callback=self.parse_detail_dealer,
                headers=self.headers,
                meta=response.meta,
                dont_filter=True,
            )
        next_url = response.xpath("//div[@id='divPage']//a[@class='next-on']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_dealer,
                meta=response.meta

            )

    def parse_detail_dealer(self, response):
        # print(response.text)
        soup = BeautifulSoup(response.text, "html5lib")
        html = Selector(text=soup.prettify())
        # html = response
        shopname = html.xpath("//h1[@class='name']/text()").get()
        if not shopname:
            shopname = html.xpath("//h1[@class='name ']/text()").get()
        shopid = response.url.split('/')[3]
        item = AutohomeItem_price()
        tr_list = response.xpath("//div[@class='car_list']//tr")
        for tr in tr_list:
            salesdesc = tr.xpath(".//a[@class='carname']/@title").get()
            if salesdesc:
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['website'] = website
                item['salesdesc'] = salesdesc
                salesdescid = tr.xpath(".//a[@class='carname']/@href").get()
                item["salesdescid"] = re.findall('\D/(.*?).html',salesdescid)[0]
                guideprice = tr.xpath(".//td[2]/text()").get()
                salesprice = tr.xpath(".//a[@class='imp']/text()").get()
                item['guideprice'] = guideprice.replace(' ', '').replace('\r', '').replace('\n', '') if guideprice else None
                item['salesprice'] = salesprice.replace(' ', '').replace('\r', '').replace('\n', '') if salesprice else None
                item['shopname'] = shopname.replace(' ', '').replace('\r', '').replace('\n', '')
                item["shopid"] = shopid
                item["dealer_address"] = response.meta['address']
                item['prov_Name'] = response.meta['prov_Name']
                item['city_Name'] = response.meta['city']
                item["brandname"] = self.brand_dic[response.meta['series_pinyin']]["brandname"]
                item["brandid"] = self.brand_dic[response.meta['series_pinyin']]["brandid"]
                # 车系id
                item["vehilename"] = self.brand_dic[response.meta['series_pinyin']]["seriesname"]
                item["vehilenameid"] = self.brand_dic[response.meta['series_pinyin']]["serise_id"]
                item['url'] = response.url
                item["status"] = item["brandname"]+'-'+item["vehilename"]+'-'+item["salesdesc"]+'-'+item["salesprice"]+'-'+item["shopid"]+'-'+item["shopname"]+'-'+item["city_Name"]
                # print(item)
                yield item
        # print(response.url)
        # print("*"*100)


    # def start_requests(self):
    #     url = 'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=master'
    #     yield scrapy.Request(
    #         url=url,
    #         dont_filter=True,
    #     )
    #
    # def parse(self, response):
    #
    #     data = demjson.decode(response.text)
    #     for i in data['DataList']:
    #         brandname = i['name']
    #         brandid = i["id"]
    #         meta = {
    #             "brandname": brandname,
    #             "brandid": brandid
    #         }
    #         # print(brandname)
    #         series_url = f'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=serial&pid={brandid}'
    #         # eg:http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=serial&pid=100
    #         # if brandname == "别克":
    #         #     print(series_url)
    #         response.meta.update(**meta)
    #         yield scrapy.Request(
    #                 url=series_url,
    #                 callback=self.parse_series_list,
    #                 meta=response.meta
    #             )
    #
    # def parse_series_list(self, response):
    #     datas = demjson.decode(response.text)
    #     for i in datas:
    #         for c in i["child"]:
    #             status = c["saleState"]
    #             # if "停销" not in status:
    #             data = dict()
    #             serise_id = c["id"]
    #             seriesname = c["name"]
    #             serierpinyin = c["urlSpell"]
    #             brandname = response.meta["brandname"]
    #             brandid = response.meta["brandid"]
    #             data["serise_id"] = serise_id
    #             data["seriesname"] = seriesname
    #             data["brandname"] = brandname
    #             data["brandid"] = brandid
    #             self.brand_dic[serierpinyin] = data
                # if brandname == "别克":
                #     print(self.brand_dic)
        #         self.brand_dic[serierpinyin] = data
        #         d = str(self.brand_dic) + ',\n'

        #             # f.flush()
        # #         self.brand_dic.update(**self.brand_dic)
        # print("*" * 100)
        # d = str(self.brand_dic) + ',\n'
        # with open('./yiche.json', 'w+') as f:
        #     f.writelines(d)
        # pprint(self.brand_dic)