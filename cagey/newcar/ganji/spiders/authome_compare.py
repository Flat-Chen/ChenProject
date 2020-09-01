# -*- coding: utf-8 -*-
import scrapy
from ganji.items import autohome_compare
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website = 'autohome_family_compare2'


class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls = ['http://car.m.autohome.com.cn/#pvareaid=100235']

    # start_urls = ['http://www.autohome.com.cn/509/']

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'auto_compare', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        for href in response.xpath('//ul[@class="brandgroup"]/li'):
            brandid = href.xpath('@v').extract_first()
            brandname = href.xpath('strong/text()').extract_first()
            url = 'http://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?b=' + brandid
            yield scrapy.Request(url, callback=self.parse_familyinfo, dont_filter=True)

    # family parse
    def parse_familyinfo(self, response):
        # list value
        items = eval(response.xpath('//p/text()').extract_first())
        for factory in items['result']['allSellSeries']:
            for family in factory['SeriesItems']:
                familyid = str(family['id'])
                url = 'http://k.autohome.com.cn/compareseries/' + str(familyid) + "/"
                yield scrapy.Request(url, callback=self.parse_compare)

    def parse_compare(self, response):
        # count
        print("response.url", response.url)
        self.counts += 1
        print("download              " + str(self.counts) + "                  items")
        # item loader
        item = autohome_compare()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['familyid'] = re.findall("\d+", response.url)[0]
        item['shortdesc'] = response.xpath('//span[@class="cd60000"]/text()').extract_first()

        for data in response.xpath('//div[@class="ranking-tit rank-bg-gray seriesItemBox"]'):
            if len(data.xpath('div/span').extract()) != 0:
                for rank in data.xpath('div/span'):
                    item['rank'] = rank.xpath('text()').extract_first()
            else:
                item['rank'] = '第1名'

            for rankname in data.xpath('h4/a'):
                item['comparename'] = rankname.xpath('text()').extract_first()
                item['compareurl'] = rankname.xpath('@href').extract_first()
                item['comparefamilyid'] = rankname.xpath('@href').re('\d+')[0]
                item['status'] = hashlib.md5(item['compareurl'] + item['url']).hexdigest()
                yield item
