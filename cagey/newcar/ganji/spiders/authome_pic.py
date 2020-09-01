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

website ='autohome_pic'

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
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        i=0
        for href in response.xpath('//ul[@class="brandgroup"]/li'):
            i+=1
            brandid = href.xpath('@v').extract_first()
            brandname = href.xpath('strong/text()').extract_first()
            url = 'http://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?b=' + brandid
            brandtag = i
            metadata = {"brandid": brandid, "brandname": brandname,
                        "brandtag":brandtag}
            # if len(brandid)!=0:
            #     picurl="http://x.autoimg.cn/m/news/brand/"+brandid+".jpg"
            #     file_name = str(i) +'_'+ brandid + ".jpg"
            #     file_path = os.path.join("D:\\autohome_pic2", file_name)
            #     urllib.urlretrieve(picurl, file_path)
            yield scrapy.Request(url,callback=self.parse_familyinfo, dont_filter=True)

    def parse_familyinfo(self, response):
        # list value
        items = eval(response.xpath('//p/text()').extract_first())
        for factory in items['result']['allSellSeries']:
            for family in factory['SeriesItems']:
                familyid = str(family['id'])
                url = "http://www.autohome.com.cn/" + str(familyid) + "/"
                # print url
                yield scrapy.Request(url, callback=self.parse_piclink1)

    def parse_piclink1(self,response):
    # def parse(self, response):
        item = Autohomepic()
        item['purl'] = response.url

        picid = response.xpath('//div[@class="autoseries-pic-img1"]/a/@href').re("\d+")
        if len(picid) == 0:
            picid = response.xpath('//dl[@class="models_pics"]/dt/a/@href').re('\d+')
        # print picid[0], picid[1]
        url="http://car.autohome.com.cn/photo/series/" + str(picid[0]) + "/1/"+ str(picid[1]) +".html"
        request = scrapy.Request(url, callback=self.parse_piclink2)
        request.meta['item']=item
        yield request

    def parse_piclink2(self,response):
        item = response.meta['item']
        try:
            url=response.xpath('//div[@class="pic"]/img/@src').extract_first()
            # print "url2",url
            familyid = response.xpath('//div[@class="breadnav"]/a[4]/@href').re('\d+')[0]
            if len(url) != 0:
                picurl = url
                file_name = familyid + ".jpg"
                file_path = os.path.join("D:\\autohome_family_pic2", file_name)
                urllib.urlretrieve(picurl, file_path)
        except Exception,e:
            print e
            print item['purl']
            yield scrapy.Request(item["purl"],callback=self.parse_miss)
    #
    def parse_miss(self,response):
        familyid=response.xpath('//dl[@class="models_pics"]/dt/a/@href').re('\d+')[0]
        url=response.xpath('//dl[@class="models_pics"]/dt/a/img/@src').extract_first()
        if len(url)!=0:
            file_name = familyid + ".jpg"
            file_path = os.path.join("D:\\autohome_family_pic2_1", file_name)
            urllib.urlretrieve(url, file_path)