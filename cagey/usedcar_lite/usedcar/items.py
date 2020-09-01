# -*- coding: utf-8 -*-
import scrapy

class UsedcarItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    pagetime = scrapy.Field()
    status = scrapy.Field()
    datasave = scrapy.Field()

class Chezhibao2(UsedcarItem):
    # carid = scrapy.Field()
    accident_score = scrapy.Field()
    city = scrapy.Field()
    # totalgrade = scrapy.Field()
    emission = scrapy.Field()
    shortdesc = scrapy.Field()
    pagetitle = scrapy.Field()
    img_url = scrapy.Field()
    years = scrapy.Field()

    mileage = scrapy.Field()
    registerdate = scrapy.Field()
    carno = scrapy.Field()
    series = scrapy.Field()
    # bodystyle = scrapy.Field()

class Youxinpai2(UsedcarItem):
    change_times = scrapy.Field()
