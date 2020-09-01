# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomefamilyItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random

website ='autohome_family'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls=['http://car.m.autohome.com.cn/#pvareaid=100235']

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        for href in response.xpath('//ul[@class="brandgroup"]/li'):
            brandid = href.xpath('@v').extract_first()
            brandname = href.xpath('strong/text()').extract_first()
            metadata ={"brandid":brandid,"brandname":brandname}
            url= 'http://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?b='+brandid
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_family,dont_filter=True)

    # get car infor
    def parse_family(self, response):
        metadata =response.meta['metadata']
        # item loader
        itembase = AutohomefamilyItem()
        itembase['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        itembase['website'] = website
        itembase = dict(itembase,**metadata)
        # list value
        items = eval(response.xpath('//p/text()').extract_first())
        for factory in items['result']['allSellSeries']:
            itemfactory = AutohomefamilyItem()
            itemfactory['factoryid'] = factory['Id']
            itemfactory['factoryname']= factory['name']
            itemfactory = dict(itemfactory,**itembase)
            for family in factory['SeriesItems']:
                # counts
                self.counts += 1
                logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
                item = AutohomefamilyItem()
                item['familyid'] = family['id']
                item['familyname'] = family['name']
                item['maxprice'] = family['maxprice']
                item['minprice'] = family['minprice']
                item['seriesPicUrl'] = family['seriesPicUrl']
                item['url']='http://www.autohome.com.cn/'+str(family['id'])+'/'
                item['status']=item['url']
                item = dict(item,**itemfactory)
                yield item