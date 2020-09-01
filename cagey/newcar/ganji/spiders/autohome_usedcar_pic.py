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
import urllib2
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

website='autohome_usedcar_pic'

class CarSpider(scrapy.Spider):
    name=website
    allowed_domains=["autohome.com.cn"]
    start_urls=['http://car.m.autohome.com.cn/']

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
        # print "do parse, get the brandid and brandname"
        for href in response.xpath('//div[@id="div_ListBrand"]/ul/li'):
            brandid=href.xpath('@v').extract_first()
            url = "http://car.autohome.com.cn/pic/brand-" + str(brandid) + ".html"
            metadata={"brandid": brandid}
            yield scrapy.Request(url,meta={"metadata": metadata},callback=self.fimily_parse, dont_filter=True)

    def fimily_parse(self,response):
        #print "do fimily_parse, get the familyid and familyname"
        metadata = response.meta['metadata']
        x=response.xpath('//div[@class="uibox-con carpic-list02"]/ul/li')
        for temp in x:
            familybase=temp.xpath('a/@href').extract_first()
            familyid=re.findall("(\d+).html", familybase)[0]
            addmeta = {"num": 1, "familyid": familyid}
            metadata = dict(metadata, **addmeta)
            url = "http://www.autohome.com.cn/" + familyid + "/"
            #print url
            yield scrapy.Request(url,meta={"metadata": metadata},callback=self.temp_fun, dont_filter=True)

    def temp_fun(self, response):
        #print "do temp_fun, get the pic"
        metadata = response.meta['metadata']
        url_temp = response.xpath('//a[@id="nav_che168link"]/@href').extract_first()
        if url_temp:
            #print url
            url = "http:" + url_temp
            addmeta = {"num": 0}
            metadata = dict(metadata, **addmeta)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        print "do parse_info, get the pic"
        metadata = response.meta['metadata']
        test = response.xpath('//ul[@id="CurConditions"]/li[4]')
        if test:
            x=response.xpath('//ul[@id="viewlist_ul"]/li')
            if x:
                for temp in x:
                    metadata["num"] += 1
                    title=temp.xpath('.//h3/text()').extract_first()
                    #print title
                    if title:
                        picurl_temp=temp.xpath('a/img[@class="photo"]/@src').extract_first()
                        #print picurl_temp

                        pic_test = re.findall("default", picurl_temp)
                        if pic_test:
                            picurl = temp.xpath('a/img[@class="photo"]/@src2').extract_first()
                        else:
                            picurl = picurl_temp

                        if not re.findall("https", picurl):
                            picurl = "http:" + picurl

                        if temp.xpath('a/img/@src').re('__(.*)\.jpg'):
                            status = temp.xpath('a/img/@src').re('__(.*)\.jpg')[0]
                        elif temp.xpath('a/img/@src').re('_(.*)\.jpg'):
                            status = temp.xpath('a/img/@src').re('_(.*)\.jpg')[0]
                        else:
                            status = str(metadata["num"])

                        #file_name = str(metadata['brandid']) + "_" + str(metadata['familyid']) + "_" + str(metadata["num"]) + "_" + title + "_" + status + ".jpg"
                        file_name = str(metadata['brandid']) + "_" + str(metadata['familyid']) + "_" + title + "_" + status + ".jpg"
                        #print picurl
                        try:
                            file_path=os.path.join('/home/drive3/data/autohome_usedcar_pictures',file_name)
                            urllib.urlretrieve(picurl,file_path)
                        except:
                            print "write to file bad..."
                            print picurl
                        if metadata["num"]>100:
                            break
                next_page=response.xpath('//a[@class="page-item-next"]/@href').extract_first()

                if next_page and metadata["num"]<100:
                    url=response.urljoin(next_page)
                    yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_info, dont_filter=True)
