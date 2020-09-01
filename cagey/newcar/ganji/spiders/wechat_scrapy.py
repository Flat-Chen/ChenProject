# -*- coding: utf-8 -*-
import scrapy
from ganji.items import wechat_autohomeItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import pymongo

website='wechat_autohome'

class CarSpider(scrapy.Spider):
    name = website

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
        conn=pymongo.MongoClient("192.168.1.94", 27017)
        db=conn['network']
        table=db['autohome_dealer']
        for temp in table.find().skip(0).limit(100):
            shopname=temp['shopname']
            url="http://weixin.sogou.com/weixin?type=1&s_from=input&query="+shopname+"&ie=utf8"
            metadata={"shopname":shopname}
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse, dont_filter=True)

    def parse(self,response):
        metadata = response.meta['metadata']
        x=response.xpath('//ul[@class="news-list2"]/li')
        for temp in x:
            item = wechat_autohomeItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url
            item['shopurl'] =temp.xpath('div/div[@class="txt-box"]/p/a/@href').extract_first()
            item['wechatid']=temp.xpath('div/div[@class="txt-box"]/p[@class="info"]/label/text()').extract_first()
            title = temp.xpath('div/div[@class="txt-box"]/p/a/text()').extract_first()
            item['title']= title + metadata['shopname']
            yield item




