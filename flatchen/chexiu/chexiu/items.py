# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChexiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ChexiuPriceItem(scrapy.Item):
    # 品牌
    brandname = scrapy.Field()
    brand_id = scrapy.Field()

    # 车系
    familyname = scrapy.Field()
    family_id = scrapy.Field()

    # 车型
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()

    # 厂商名
    factoryname = scrapy.Field()

    # 城市名
    city_name = scrapy.Field()

    # 最低净车价
    min_clean_price = scrapy.Field()

    # 指导价
    guide_price = scrapy.Field()

    # 最低全包售价
    min_all_price = scrapy.Field()

    # 地区
    region = scrapy.Field()

    # 净车价
    clean_price = scrapy.Field()

    # 购置税
    purchase_tax = scrapy.Field()

    # 上牌费用
    license_price = scrapy.Field()

    # 商业保险
    insurance = scrapy.Field()

    # 精品套装
    boutique_suite = scrapy.Field()

    # 全包售价
    all_price = scrapy.Field()



    url = scrapy.Field()
    grab_time = scrapy.Field()
    status = scrapy.Field()


class ChexiucarsItem(scrapy.Item):
    # 品牌
    brandname = scrapy.Field()
    brand_id = scrapy.Field()

    # 车系
    familyname = scrapy.Field()
    family_id = scrapy.Field()

    # 车型
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()

    # 厂商名
    factoryname = scrapy.Field()
    # factory_id = scrapy.Field()

    # 指导价
    guideprice = scrapy.Field()

    # 发动机
    engine = scrapy.Field()
    # 变速箱
    transmission = scrapy.Field()
    # 车身结构
    car_structure = scrapy.Field()
    # 车门
    car_door = scrapy.Field()
    # 车座
    car_seat = scrapy.Field()
    # 排量
    displacement = scrapy.Field()
    #
    air_intake = scrapy.Field()
    # 燃料形式
    fuel = scrapy.Field()
    # 环保标准
    environmental_protection_standard = scrapy.Field()
    # 变速箱类型
    transmission_type = scrapy.Field()
    # 驱动方式
    drive_way = scrapy.Field()

    info = scrapy.Field()
    url = scrapy.Field()
    grab_time = scrapy.Field()
    status = scrapy.Field()
