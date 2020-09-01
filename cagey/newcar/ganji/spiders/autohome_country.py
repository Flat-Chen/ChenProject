# -*- coding: utf-8 -*-
import scrapy
from ganji.items import autohomeaddinfo
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
website ='autohomecountry_zt_v1'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls=[
                 'http://www.autohome.com.cn/car/'
                ]

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

    # nation select
    def parse(self, response):
        for i in range(1,13):
            for j in (1,3):
                url = response.url+"0_0-0.0_0.0-0-0-0-"+str(j)+"-0-"+str(i)+"-0-0/"
                print url
                yield scrapy.Request(url,callback=self.parse_brandfamily)

    # brandfamily
    def parse_brandfamily(self, response):
        # item loader
        item = autohomeaddinfo()
        item['nation'] = response.xpath(u'//div[@class="carfilter-width01"]/span[@class="fontgrey"][contains(text(),"\u56fd\u522b")]/../ul/li/a[@class="current"]/text()').extract_first()
        item['property']= response.xpath(u'//div[@class="carfilter-width04"]/span[@class="fontgrey name-01"][contains(text(),"\u751f\u4ea7\u65b9\u5f0f")]/../ul/li/a[@class="current"]/text()').extract_first()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        for temp in response.xpath('//div[@class="uibox-con rank-list rank-list-pic"]/dl'):
            item['brandname'] = temp.xpath('dt/div/a/text()').extract_first()
            item['brandid'] = temp.xpath('dt/div/a/@href').re('\d+')[0]
            item['factoryname'] = temp.xpath('dd/div/text()').extract_first()
            family = temp.xpath('dd/ul/li[1]/@id').extract_first()
            print family
            # item['status'] = family +  item['brandid']
            status = item['factoryname'].encode('utf-8')+item['nation'].encode('utf-8') \
                              + item['property'].encode('utf-8')+item['brandname'].encode('utf-8') \
                              + item['brandid'].encode('utf-8')+item['grabtime']
            item['status']=hashlib.md5(status).hexdigest()
            # item['status'] = factoryname.encode('utf-8')
            yield item

