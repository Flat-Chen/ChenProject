# -*- coding: utf-8 -*-
import scrapy
from ganji.items import autohomedealeritem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re

website="autohome_dealer"

class CarSpider(scrapy.Spider):

    name=website
    # allowed_domains=["autohome.com.cn"]
    # start_url=['http://dealer.autohome.com.cn/china?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=1&kindId=1&orderType=0']

    def __init__(self,**kwargs):
        print "do initial"
        super(CarSpider,self).__init__(**kwargs)
        #problem report
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000
        #mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'network', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')


    def start_requests(self):
        print "do start request"
        carlist = []
        for i in range(0,1644):
            url="http://dealer.autohome.com.cn/china?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex="+str(i)+"&kindId=1&orderType=0"
            car = scrapy.Request(url)
            carlist.append(car)
            # yield scrapy.Request(url,callback=self.parse_middle)
        return carlist

    def parse(self,response):
        print "do parse_middle"
        x=response.xpath('//ul[@class="list-box"]/li')
        for temp in x:
            urlbase = temp.xpath('a/@href').extract_first()
            url="http://"+str(urlbase[2:len(urlbase)])
            yield scrapy.Request(url,callback=self.parse_maininfo)

    def parse_maininfo(self,response):
        print "do parse_maininfo"
        item=autohomedealeritem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()
        item['tel']=response.xpath('//span[@class="dealer-api-phone"]/text()').extract_first() \
            if response.xpath('//span[@class="dealer-api-phone"]/text()').extract_first() else "-"
        item['shopname']=response.xpath('//div[@class="text-main"]/text()').extract_first() \
            if response.xpath('//div[@class="text-main"]/text()').extract_first() else "-"
        item['shoptype']=response.xpath(u'//p[contains(text(),"\u6240\u5c5e\u7ea7\u522b")]/text()').re(u'\u6240\u5c5e\u7ea7\u522b\uff1a(.*)')[0] \
            if response.xpath(u'//p[contains(text(),"\u6240\u5c5e\u7ea7\u522b")]/text()').re(u'\u6240\u5c5e\u7ea7\u522b\uff1a(.*)') else "-"
        x=response.xpath('//div[@class="brandtree"]/div[@class="brandtree-name"]')
        bstring=""
        for temp in x:
            bstring=temp.xpath('p[2]/text()').extract_first()+"-"+bstring
        item['mainbrand']=bstring[0:len(bstring)-1]
        item['location']=response.xpath('//p[@class="address"]/@title').extract_first() \
            if response.xpath('//p[@class="address"]/@title').extract_first() else "-"
        item['status']=response.url
        item['promotion']=response.xpath('//div[@class="salescont-name font-yh"]/a/text()').extract_first() \
            if response.xpath('//div[@class="salescont-name font-yh"]/a/text()').extract_first() else "-"
        urlbase=response.xpath('//div[@class="salescont-name font-yh"]/a/@href').extract_first() \
            if response.xpath('//div[@class="salescont-name font-yh"]/a/@href').extract_first() else "-"
        item['promotionurl']=response.urljoin(urlbase)
        item['salesregion']=response.xpath('//i[@class="icon icon-salebc"]/@title').extract_first() \
            if response.xpath('//i[@class="icon icon-salebc"]/@title').extract_first() else "-"
        yield item
