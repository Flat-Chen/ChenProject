# -*- coding: utf-8 -*-

import scrapy


class GanjiItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    pagetime = scrapy.Field()
    status = scrapy.Field()
    datasave = scrapy.Field()

class YouXinPai(GanjiItem):
    brand = scrapy.Field()
    series = scrapy.Field()

class GanJi(GanjiItem):
    guideprice = scrapy.Field()

class CheWang(GanjiItem):
    guideprice = scrapy.Field()

class CheSuPai(GanjiItem):
    accident_desc = scrapy.Field()
    outer_desc = scrapy.Field()
    safe_desc = scrapy.Field()
    road_desc = scrapy.Field()

class Auto51(GanjiItem):
    guideprice = scrapy.Field()
    factoryname = scrapy.Field()
    level = scrapy.Field()
    geartype = scrapy.Field()
    gearnumber = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    bodystyle = scrapy.Field()
    wheelbase = scrapy.Field()
    doors = scrapy.Field()
    seats = scrapy.Field()
    frontgauge = scrapy.Field()
    lwvnumber = scrapy.Field()
    maxpower = scrapy.Field()
    maxnm = scrapy.Field()
    fueltype = scrapy.Field()
    fuelnumber = scrapy.Field()
    driverway = scrapy.Field()


class Che101(GanjiItem):
    fueltype = scrapy.Field()
    doors = scrapy.Field()
    seats = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    gearnumber = scrapy.Field()
    weight = scrapy.Field()
    wheelbase = scrapy.Field()
    lwv = scrapy.Field()
    lwvnumber = scrapy.Field()
    maxnm = scrapy.Field()
    maxpower = scrapy.Field()
    frontgauge = scrapy.Field()
    compress = scrapy.Field()
    output = scrapy.Field()

class Che168(GanjiItem):
    guideprice = scrapy.Field()
    guidepricetax = scrapy.Field()

class Che273(GanjiItem):
    guideprice = scrapy.Field()
    guidepricetax = scrapy.Field()

class Che58(GanjiItem):
    fueltype = scrapy.Field()
    driverway = scrapy.Field()
    guideprice = scrapy.Field()
    doors = scrapy.Field()
    seats = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    gearnumber = scrapy.Field()
    weight = scrapy.Field()
    wheelbase = scrapy.Field()
    fuelnumber = scrapy.Field()
    lwv = scrapy.Field()
    lwvnumber = scrapy.Field()
    maxnm = scrapy.Field()
    maxpower = scrapy.Field()
    maxps = scrapy.Field()
    frontgauge = scrapy.Field()
    compress = scrapy.Field()
    gear = scrapy.Field()

class CheMao(GanjiItem):
    body = scrapy.Field()
    bodystyle = scrapy.Field()
    gear = scrapy.Field()
    gearnumber = scrapy.Field()
    doors = scrapy.Field()
    seats = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()

    fueltype = scrapy.Field()
    fuelnumber = scrapy.Field()
    maxnm = scrapy.Field()
    maxpower = scrapy.Field()
    maxps = scrapy.Field()

    lwv = scrapy.Field()
    lwvnumber = scrapy.Field()
    compress = scrapy.Field()
    driverway = scrapy.Field()