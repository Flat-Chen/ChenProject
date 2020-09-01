# -*- coding: utf-8 -*-
import scrapy
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
import car_spider_iautos
import os

website='yiche_all_pic'

class CarSpider(scrapy.Spider):
    name=website
    allowed_domains=["bitauto.com"]
    start_urls=["http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&pid=0&rt=master&callback=callback#"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        #problem report
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000
        #mongo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        x = response.xpath('//p/text()').extract_first()
        temp = re.findall('DataList:(.*)}\)', x)[0]
        data = json.loads(temp)
        length = len(data)
        brandid = []
        for i in range(0, length):
            brandid.append(data[i]['id'])
        for temp in brandid:
            metadata={"brandid":temp}
            url="http://photo.bitauto.com/master/"+str(temp)+"/"
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.middle_parse)


    def middle_parse(self,response):
        metadata=response.meta['metadata']
        x=response.xpath('//div[@class="row block-4col-180"]/div')
        for temp in x:
            urlbase=temp.xpath('div/div/a/@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.middle2_parse)

    def middle2_parse(self,response):
        seriesid=re.findall('\d+',response.url)[0] \
            if re.findall('\d+',response.url) else "_"
        addmeta={"seriesid":seriesid}
        metadata=response.meta['metadata']
        metadata=dict(metadata, **addmeta)
        x=response.xpath(u'//a[contains(text(),"\u5916\u89c2")]/@href').extract_first()
        url=response.urljoin(x)
        yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_maininfo)

    def parse_maininfo(self,response):
        metadata=response.meta['metadata']
        x=response.xpath('//div[@class="row block-4col-180"]/div')
        for temp in x:
            picurl=temp.xpath('div/div/a/img/@src').extract_first()
            title=temp.xpath('div/div/a/img/@alt').extract_first()
            status=temp.xpath('div/div/a/img/@src').re('\d+')[0] \
                if temp.xpath('div/div/a/img/@src').re('\d+') else "_"
            file_name=metadata['brandid']+"_"+metadata['seriesid']+"_"+title+"_"+status+".jpg"
            file_path=os.path.join("/home/drive3/data/yiche_pictures",file_name)
            urllib.urlretrieve(picurl,file_path)
        next_page=response.xpath('//a[@class="next_on"]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_maininfo)