# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomeItem_bfv
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website ='autohome_bfv_zt'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls = ['http://www.autohome.com.cn/car/#pvareaid=101452']

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
        i=0
        x=response.xpath('//div[@class="clear brand-series"]/dl')
        for temp in x[1:25]:
            y=temp.xpath('dd')
            for temp1 in y:
                i=i+1
                brandname=temp1.xpath('a/@cname').extract_first()
                brandtag=i
                brandid=temp1.xpath('a/@vos').extract_first()
                metadata = {"brandid": brandid, "brandname": brandname, "brandtag": brandtag}
                url='http://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?b=' + brandid
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_familyinfo, dont_filter=True)
        # for href in response.xpath('//ul[@class="brandgroup"]/li'):
        #     i=i+1
        #     brandid = href.xpath('@v').extract_first()
        #     brandname = href.xpath('strong/text()').extract_first()
        #     brandtag = i
        #     metadata = {"brandid": brandid, "brandname": brandname,"brandtag":brandtag}
        #     url = 'http://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?b=' + brandid
        #     yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_familyinfo, dont_filter=True)

    #family
    def parse_familyinfo(self,response):
        #
        item = AutohomeItem_bfv()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        #
        metadata = response.meta['metadata']
        if metadata:
            item['brandtag']= metadata['brandtag']
            item['brandid'] = metadata['brandid']
            item['brandname']= metadata['brandname']
        # list value
        items = eval(response.xpath('//p/text()').extract_first())
        i=0
        for factory in items['result']['allSellSeries']:
            i += 1
            print factory['Id']
            item['factoryid']= factory['Id']
            item['factoryname']= factory['name']
            item['factorytag'] = i
            #print factoryid ,factoryname
            j=0
            for family in factory['SeriesItems']:
                j = j+1
                item['familyid'] = str(family['id'])
                item['familyname'] = family['name']
                item['familytag'] = j
                #print familyid,familyname
                item['status'] = hashlib.md5(response.url+str(family['id'])+str(item['factoryid'])).hexdigest()
                if len(item['status'])==0:
                    print 'ERROR OCCURES'
                yield item
