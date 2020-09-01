# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IautosFamilyItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    brandname = scrapy.Field()
    factoryname = scrapy.Field()
    familyname = scrapy.Field()
    familyid = scrapy.Field()
    ershou_brand = scrapy.Field()
    ershou_factory = scrapy.Field()
    ershou_family = scrapy.Field()


class KoubeiNewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutohomeButieItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    autohomeid = scrapy.Field()
    minprice = scrapy.Field()
    maxprice = scrapy.Field()


class YicheKoubeiItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    u_carinfo = scrapy.Field()
    carinfo = scrapy.Field()
    userinfo = scrapy.Field()
    familyname = scrapy.Field()
    familynameid = scrapy.Field()
    shortdesc = scrapy.Field()
    guideprice = scrapy.Field()
    usage = scrapy.Field()
    fuel = scrapy.Field()
    buy_date = scrapy.Field()
    buy_location = scrapy.Field()
    buy_pure_price = scrapy.Field()
    buyerid = scrapy.Field()
    buyername = scrapy.Field()
    comment_detail = scrapy.Field()
    comment_people = scrapy.Field()
    isGoodComment = scrapy.Field()
    mileage = scrapy.Field()
    oil_consume = scrapy.Field()
    picurl = scrapy.Field()
    score = scrapy.Field()
    score_star = scrapy.Field()
    score_appearance = scrapy.Field()
    score_appearance_compare = scrapy.Field()
    score_comfort = scrapy.Field()
    score_comfort_compare = scrapy.Field()
    score_control = scrapy.Field()
    score_control_compare = scrapy.Field()
    score_cost = scrapy.Field()
    score_cost_compare = scrapy.Field()
    score_fuel = scrapy.Field()
    score_fuel_compare = scrapy.Field()
    score_power = scrapy.Field()
    score_power_compare = scrapy.Field()
    score_space = scrapy.Field()
    score_space_compare = scrapy.Field()
    score_trim = scrapy.Field()
    score_trim_compare = scrapy.Field()

    # ucid = scrapy.Field()
    brand = scrapy.Field()
    satisfied = scrapy.Field()
    unsatisfied = scrapy.Field()

    visitCount = scrapy.Field()
    helpfulCount = scrapy.Field()
    commentCount = scrapy.Field()
    post_time = scrapy.Field()
    spec_id = scrapy.Field()

    description = scrapy.Field()
    # urlspell = scrapy.Field()


class XinlangItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    screen_name = scrapy.Field()
    gender = scrapy.Field()
    user_id = scrapy.Field()
    create_time = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    brand = scrapy.Field()
    grabtime = scrapy.Field()
    series = scrapy.Field()
    content = scrapy.Field()


class YicheLuntanItem(scrapy.Item):
    _id = scrapy.Field()
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
    classify = scrapy.Field()  # 帖子种类


class DianchebangItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    familyid = scrapy.Field()
    familyname = scrapy.Field()
    brandid = scrapy.Field()
    brandname = scrapy.Field()
    factory = scrapy.Field()
    modelname = scrapy.Field()
    guideprice = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    miles = scrapy.Field()
    drivemode = scrapy.Field()
    seats = scrapy.Field()
    body = scrapy.Field()
    doors = scrapy.Field()


class DiyidiandongButieItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    brandname = scrapy.Field()
    brandid = scrapy.Field()
    familyname = scrapy.Field()
    familyid = scrapy.Field()
    diandong = scrapy.Field()
    butiejiage = scrapy.Field()
    mileage = scrapy.Field()
    modelname = scrapy.Field()
    ckg = scrapy.Field()
    gonglv = scrapy.Field()
    charge_time = scrapy.Field()
    fast_charge = scrapy.Field()
    guide_price = scrapy.Field()
    butiehoujiage = scrapy.Field()
    modelid = scrapy.Field()


class Chehang168Item(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    brandname = scrapy.Field()
    brandcode = scrapy.Field()
    familyname = scrapy.Field()
    familycode = scrapy.Field()
    title = scrapy.Field()
    guideprice = scrapy.Field()
    price = scrapy.Field()
    desc = scrapy.Field()
    store = scrapy.Field()
    time = scrapy.Field()
    desc1 = scrapy.Field()
    desc2 = scrapy.Field()
    desc3_2 = scrapy.Field()
    desc3_3 = scrapy.Field()


class PautoKoubeiItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    u_carinfo = scrapy.Field()
    carinfo = scrapy.Field()
    userinfo = scrapy.Field()

    familyname = scrapy.Field()
    familynameid = scrapy.Field()
    shortdesc = scrapy.Field()
    guideprice = scrapy.Field()
    usage = scrapy.Field()
    fuel = scrapy.Field()
    buy_date = scrapy.Field()
    buy_location = scrapy.Field()
    buy_pure_price = scrapy.Field()
    buyerid = scrapy.Field()
    buyername = scrapy.Field()
    comment_detail = scrapy.Field()
    comment_people = scrapy.Field()
    isGoodComment = scrapy.Field()
    mileage = scrapy.Field()
    oil_consume = scrapy.Field()
    picurl = scrapy.Field()
    score = scrapy.Field()
    score_star = scrapy.Field()
    score_appearance = scrapy.Field()
    score_appearance_compare = scrapy.Field()
    score_comfort = scrapy.Field()
    score_comfort_compare = scrapy.Field()
    score_control = scrapy.Field()
    score_control_compare = scrapy.Field()
    score_cost = scrapy.Field()
    score_cost_compare = scrapy.Field()
    score_fuel = scrapy.Field()
    score_fuel_compare = scrapy.Field()
    score_power = scrapy.Field()
    score_power_compare = scrapy.Field()
    score_space = scrapy.Field()
    score_space_compare = scrapy.Field()
    score_trim = scrapy.Field()
    score_trim_compare = scrapy.Field()

    # ucid = scrapy.Field()
    brand = scrapy.Field()
    satisfied = scrapy.Field()
    unsatisfied = scrapy.Field()

    visitCount = scrapy.Field()
    helpfulCount = scrapy.Field()
    commentCount = scrapy.Field()
    post_time = scrapy.Field()
    spec_id = scrapy.Field()

    description = scrapy.Field()


class KBBItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    MILEAGE = scrapy.Field()
    DRIVE_TYPE = scrapy.Field()
    ENGINE = scrapy.Field()
    TRANSMISSION = scrapy.Field()
    FUEL_TYPE = scrapy.Field()
    EXTERIOR = scrapy.Field()
    INTERIOR = scrapy.Field()
    VIN = scrapy.Field()
    MPG = scrapy.Field()
    status = scrapy.Field()
