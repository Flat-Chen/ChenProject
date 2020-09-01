# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YicheLuntanItem(scrapy.Item):
    _id = scrapy.Field()
    grabtime = scrapy.Field()  # 抓取时间
    parsetime = scrapy.Field()  # 解析时间
    content = scrapy.Field()
    url = scrapy.Field()
    user_name = scrapy.Field()  # 车主
    posted_time = scrapy.Field() # 发帖时间
    user_car = scrapy.Field()
    brand = scrapy.Field()
    province = scrapy.Field()
    region = scrapy.Field()
    click_num = scrapy.Field()
    reply_num = scrapy.Field()
    title = scrapy.Field()
    content_num = scrapy.Field()
    md5 = scrapy.Field()
    statusplus = scrapy.Field()
    classify = scrapy.Field()  # 帖子种类
    # source = scrapy.Field()
    information_source = scrapy.Field()



class TouSuItem(scrapy.Item):
    _id = scrapy.Field()
    grabtime = scrapy.Field()  # 抓取时间
    content = scrapy.Field()
    url = scrapy.Field()
    user_name = scrapy.Field()
    brand = scrapy.Field()
    series = scrapy.Field()
    title = scrapy.Field()
    issue = scrapy.Field()
    complainant = scrapy.Field()
    complaint_area = scrapy.Field()
    complaint_time = scrapy.Field()
    complaint_num = scrapy.Field()
    buy_time = scrapy.Field()
    four_name = scrapy.Field()
    four_phone = scrapy.Field()
    appeal = scrapy.Field()
    car_status = scrapy.Field()
    result = scrapy.Field()
    result_publish_time = scrapy.Field()
    mileage = scrapy.Field()



class LuntanItem(scrapy.Item):
    # define the fields for your item here like:
    grabtime = scrapy.Field()  # 抓取时间
    parsetime = scrapy.Field()  # 解析时间
    content = scrapy.Field()
    url = scrapy.Field()
    user_name = scrapy.Field()
    posted_time = scrapy.Field()
    user_car = scrapy.Field()
    province = scrapy.Field()
    region = scrapy.Field()
    click_num = scrapy.Field()
    reply_num = scrapy.Field()
    title = scrapy.Field()
    content_num = scrapy.Field()
    md5 = scrapy.Field()
    statusplus = scrapy.Field()
    information_source = scrapy.Field()
    brand = scrapy.Field()
    province = scrapy.Field()
    # classify = scrapy.Field()

