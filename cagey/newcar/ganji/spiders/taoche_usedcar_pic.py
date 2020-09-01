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

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

website = 'taoche_usedcar_pic'


class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["taoche.com"]
    start_urls = ['http://www.taoche.com/']

    def __init__(self, **kwargs):
        print 'do intitial step'
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 500000
        # mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')


    def parse(self, response):
        print "do parse"
        href = response.xpath('//a[@class="link sub"]/@href').extract_first()
        url = response.urljoin(href)
        yield scrapy.Request(url, callback=self.brand_parse, dont_filter=True)

    def brand_parse(self, response):
        print "do brand_parse"
        hrefs = response.xpath('//div[@class="brand-name"]')
        for href in hrefs:
            """choice the brand"""
            brandname = href.xpath('a/text()').extract_first()
            metadata = {"brandname": brandname}
            url_temp = href.xpath('a/@href').extract_first()
            url = response.urljoin(url_temp)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.family_parse, dont_filter=True)

    def family_parse(self, response):
        print "do family_parse"
        """choice the family"""
        metadata = response.meta['metadata']
        hrefs = response.xpath('//div[@class="content-area car-series clear_"]/dl//li')
        for href in hrefs:
            addmeta = {"num": 0}
            metadata = dict(metadata, **addmeta)
            familyname = href.xpath('a/text()').extract_first()
            addmeta = {"familyname": familyname}
            metadata = dict(metadata, **addmeta)
            url_temp = href.xpath('a/@href').extract_first()
            url = response.urljoin(url_temp)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.pic_parse, dont_filter=True)

    def pic_parse(self, response):
        print "do pic_parse"
        metadata = response.meta['metadata']
        hrefs = response.xpath('//div[@id="container_base"]//div[@class="img_stop"]')
        if hrefs:
            for href in hrefs:
                metadata["num"] += 1
                title = href.xpath('a/@title').extract_first()
                picurl_temp = href.xpath('a/img/@src').extract_first()

                pic_test = re.findall("picholder", picurl_temp)
                if pic_test:
                    picurl = href.xpath('a/img/@data-src').extract_first()
                else:
                    picurl = picurl_temp

                print picurl
                if re.findall("\d\S\/(.*).jpg", picurl):
                    status = re.findall("\d\S\/(.*).jpg", picurl)[0]
                elif re.findall("\d\S\/(.*).png", picurl):
                    status = re.findall("\d\S\/(.*).png", picurl)[0]
                elif re.findall("\d\S\/(.*).gif", picurl):
                    status = re.findall("\d\S\/(.*).gif", picurl)[0]
                else:
                    print picurl + " 正则无法匹配"
                    status = str(metadata["num"])

                file_name_temp = metadata['brandname'] + "_" + metadata['familyname'] + "_" + "_" + title + "_" + status + ".jpg"
                file_name = re.sub("\/","_",  file_name_temp)
                file_path = os.path.join('/home/drive3/data/yiche_usedcar_pictures', file_name)
                urllib.urlretrieve(picurl, file_path)

                if metadata["num"] >= 100:
                    break

            next_page = response.xpath('//a[@class="pages-next"]/@href').extract_first()
            if next_page and metadata["num"]<100:
                yield scrapy.Request(next_page, meta={"metadata": metadata}, callback=self.pic_parse, dont_filter=True)

