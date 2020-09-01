# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ah100CpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()
    all_star = scrapy.Field()
    view_rank = scrapy.Field()
    view_star = scrapy.Field()
    space_rank = scrapy.Field()
    space_star = scrapy.Field()
    power_rank = scrapy.Field()
    power_star = scrapy.Field()
    speed_rank = scrapy.Field()
    speed_star = scrapy.Field()
    oil_rank = scrapy.Field()
    oil_star = scrapy.Field()
    brake_rank = scrapy.Field()
    brake_star = scrapy.Field()
    feel_rank = scrapy.Field()
    feel_star = scrapy.Field()
    noise_rank = scrapy.Field()
    noise_star = scrapy.Field()
    cross_country_rank = scrapy.Field()
    cross_country_star = scrapy.Field()
    price_rank = scrapy.Field()
    price_star = scrapy.Field()
    url = scrapy.Field()
    grab_time = scrapy.Field()
    status = scrapy.Field()
