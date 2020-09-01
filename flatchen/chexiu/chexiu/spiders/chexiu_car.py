# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import pymongo
from pandas.core.frame import DataFrame
from lxml import etree


class ChexiuspiderSpider(scrapy.Spider):
    name = 'chexiu_car'
    allowed_domains = ['chexiu.com']

    start_urls = [f'https://www.chexiu.com/index.php?r=api/car/GetHotBrandWithNoPrice&pagesize=300']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(ChexiuspiderSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'chexiu',
        'MONGODB_COLLECTION': 'chexiu_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def parse(self, response):
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for car in json_data["data"]:
            brandname = car["title"]
            cat_id = car["cat_id"]
            url = f'https://sh.chexiu.com/search/list-{cat_id}-0-0-0-0-0-0-1.html'
            yield scrapy.Request(url=url, callback=self.parse_familycars, meta={"info": (cat_id, brandname)})

    def parse_familycars(self, response):
        brand_id, brandname = response.meta.get('info')
        # print(cat_id, brandname)
        family_cars = response.xpath('//div[@class="m g-fl"]')
        for family_car in family_cars:
            family_url = family_car.xpath('./a/@href').get()
            family_id = re.sub(r'\D', '', family_url)
            familyname = family_car.xpath('.//div[@class="text"]/h3/text()').get()
            url = f'https://www.chexiu.com/index.php?r=site/api/GetCarAllByStyleWithMoreInfoGroupEngin&styleid={family_id}'
            yield scrapy.Request(url=url, callback=self.parse_cars,
                                 meta={"info": (brand_id, brandname, familyname, url)})

    def parse_cars(self, response):
        # item = dict()
        brand_id, brandname, familyname, url = response.meta.get('info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for engine_list in json_data['data']:
            engine = engine_list['engine']
            for car_list in engine_list['carList']:
                # engine = engine_list['engine']
                family_id = car_list['model_id']
                vehicle_id = car_list['car_id']
                vehicle = car_list['car_name']
                url = f'https://www.chexiu.com/option/{vehicle_id}.html'

                yield scrapy.Request(url=url, callback=self.parse_vehicle,
                                     meta={"info": (brand_id, brandname, family_id, familyname, vehicle_id, vehicle)})

    def parse_vehicle(self, response):
        item = dict()
        brand_id, brandname, family_id, familyname, vehicle_id, vehicle = response.meta.get('info')
        url = response.url
        info = {}
        trs = response.xpath('//tr')
        for tr in trs:
            tds = tr.xpath('.//td[position()<3]//text()')
            td = tds.extract()
            # print(td)
            try:
                name = td[0]
                value = td[1]
                information = {name: value}
                info.update(information)
            except:
                pass
        # print(info)

        factoryname = info['厂商']
        guideprice = info['厂商指导价(元)']

        try:
            engine = info['发动机']
        except:
            engine = None
        try:
            transmission = info['变速箱']
        except:
            transmission = None
        try:
            car_structure = info['车身结构']
        except:
            car_structure = None
        try:
            car_door = info['车门数(个)']
        except:
            car_door = None
        try:
            car_seat = info['座位数(个)']
        except:
            car_seat = None
        try:
            displacement = info['排量(L)']
        except:
            displacement = None
        try:
            air_intake = info['进气形式']
        except:
            air_intake = None
        try:
            fuel = info['燃料形式']
        except:
            fuel = None
        try:
            environmental_protection_standard = info['环保标准']
        except:
            environmental_protection_standard = None
        try:
            transmission_type = info['变速箱类型']
        except:
            transmission_type = None
        try:
            drive_way = info['驱动方式']
        except:
            drive_way = None
        item['brandname'] = brandname
        item['brand_id'] = brand_id
        item['familyname'] = familyname
        item['family_id'] = family_id
        item['vehicle'] = vehicle
        item['vehicle_id'] = vehicle_id
        item['factoryname'] = factoryname
        item['guideprice'] = guideprice
        item['engine'] = engine
        item['transmission'] = transmission
        item['car_structure'] = car_structure
        item['car_door'] = car_door
        item['car_seat'] = car_seat
        item['displacement'] = displacement
        item['air_intake'] = air_intake
        item['fuel'] = fuel
        item['environmental_protection_standard'] = environmental_protection_standard
        item['transmission_type'] = transmission_type
        item['drive_way'] = drive_way
        item['info'] = info
        item['url'] = response.url
        item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['status'] = url + '-' + guideprice
        yield item
