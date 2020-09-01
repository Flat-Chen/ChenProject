# -*- coding: utf-8 -*-
import scrapy
from ganji.items import Autohomepic
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import urllib
import os


website='autohome_all_pic'

class CarSpider(scrapy.Spider):
    name=website
    allowed_domains=["autohome.com.cn"]
    start_urls=['http://car.m.autohome.com.cn/#pvareaid=100235']

    def __init__(self,**kwargs):
        super(CarSpider, self).__init__(**kwargs)
        #problem report
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000
        #mongo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self,response):
        print "do parse"
        for href in response.xpath('//ul[@class="brandgroup"]/li'):
            brandid=href.xpath('@v').extract_first()
            url='http://car.autohome.com.cn/pic/brand-'+str(brandid)+'.html'
            metadata={"brandid": brandid}
            yield scrapy.Request(url,meta={"metadata": metadata},callback=self.middle_parse)


    def middle_parse(self,response):
        print "do middle_parse"
        metadata = response.meta['metadata']
        x=response.xpath('//div[@class="uibox-con carpic-list02"]/ul/li')
        for temp in x:
            urlbase=temp.xpath('a/@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"metadata": metadata},callback=self.parse_info)

    def parse_info(self,response):
        print "do parse_info"
        metadata = response.meta['metadata']
        x=response.xpath('//a[@class="more"]/@href').extract_first()
        url=response.urljoin(x)
        yield scrapy.Request(url,meta={"metadata": metadata},callback=self.parse_maininfo)

    def parse_maininfo(self,response):
        print "do parse_maininfo"
        metadata = response.meta['metadata']
        familyid=re.findall('\d+',response.url)[0]
        x=response.xpath('//div[@class="uibox-con carpic-list03 border-b-solid"]/ul/li')
        for temp in x:
            title=temp.xpath('a/@title').extract_first()
            picurl=temp.xpath('a/img/@src').extract_first()
            status=temp.xpath('a/img/@src').re('__(.*)\.jpg')[0] \
                if temp.xpath('a/img/@src').re('__(.*)\.jpg') else "_"
            # status=re.findall('__(.*)\.jpg',picurl)[0]
            file_name=metadata['brandid']+"_"+familyid+"_"+title+"_"+status+".jpg"
            file_path=os.path.join("/home/drive3/data/pictures",file_name)
            urllib.urlretrieve(picurl,file_path)
        next_page=response.xpath(u'//a[contains(text(),"\u4e0b\u4e00\u9875")]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_maininfo)
