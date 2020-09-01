# -*- coding: utf-8 -*-

import scrapy
from ganji.items import YicheShopItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5

website='yiche_shop_test'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.58.com/ershouche/changecity/"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self, response):
        sblist = ['http://hk.58.com/ershouche/', 'http://am.58.com/ershouche/', 'http://tw.58.com/ershouche/',
                  'http://diaoyudao.58.com/', 'http://cn.58.com/ershouche/']
        for href in response.xpath('//dl[@id="clist"]/dd/a/@href'):
            url = str(response.urljoin(href.extract()))
            if url not in sblist:
                urlbase=re.findall('\/\/(.*)\.58',url)[0]
                url="http://"+str(urlbase)+".58.com/zhaozu/"
                yield scrapy.Request(url,callback=self.middle1_parse)

    def middle1_parse(self,response):
        x = response.xpath('//div[@class="filter-wrap"]/dl[1]/dd/a')
        for i in range(1,len(x)-1):
            urlbase=x[i].xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle2_parse)

    def middle2_parse(self,response):
        x = response.xpath('//dl[@class="secitem secitem-fist"]/dd/div/a')
        for temp in x:
            urlbase = temp.xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle3_parse)

    def middle3_parse(self,response):
        x = response.xpath('//div[@class="content-wrap"]/div/ul/li')
        for temp in x:
            url = temp.xpath('div[@class="list-info"]/h2/a/@href').extract_first()
            yield scrapy.Request(url,callback=self.parse_info)
        next_page=response.xpath(u'//span[containsc(text(),"下一页")]/../@href').extract_first()
        if next_page:
            url=str(next_page)
            yield scrapy.Request(url,callback=self.middle3_parse)

    def parse_info(self,response):
        item=w58officeitem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['city'] = response.xpath('//span[@id="crumbs"]/a[1]/text()').re(u'(.*)58同城')[0] \
            if response.xpath('//span[@id="crumbs"]/a[1]/text()').re(u'(.*)58同城') else "-"
        item['shortdesc'] = response.xpath('//div[@class="w headline"]/h1/text()').extract_first().strip() \
            if response.xpath('//div[@class="w headline"]/h1/text()').extract_first() else "-"
        item['district'] = response.xpath('//ul[@class="info"]/li/a[1]/text()').extract_first().strip() \
            if response.xpath('//ul[@class="info"]/li/a[1]/text()').extract_first() else "-"
        item['address'] = response.xpath(u'//i[contains(text(),"地段：")]/../text()').extract_first().strip() \
            if response.xpath(u'//i[contains(text(),"地段：")]/../text()').extract_first() else "-"
        item['buildingname']=response.xpath(u'//i[contains(text(),"楼盘：")]/../text()').extract_first().strip() \
            if response.xpath(u'//i[contains(text(),"楼盘：")]/../text()').extract_first() else "-"
        item['type1'] = response.xpath(u'//i[contains(text(),"类别：")]/../text()[2]').extract_first() \
            if response.xpath(u'//i[contains(text(),"类别：")]/../text()[2]').extract_first() else "-"
        item['area'] = response.xpath(u'//i[contains(text(),"面积：")]/../text()').extract_first().strip() \
            if response.xpath(u'//i[contains(text(),"面积：")]/../text()').extract_first() else "-"
        item['price'] = response.xpath('//em[@class="redfont"]/text()').extract_first() \
            if response.xpath('//em[@class="redfont"]/text()').extract_first() else "-"
        item['agent'] = response.xpath('//ul[@class="userinfo"]/li[2]/a/text()').extract_first().strip() \
            if response.xpath('//ul[@class="userinfo"]/li[2]/a/text()').extract_first() else "-"
        item['posttime'] = response.xpath(u'//div[contains(text(),"发布时间：")]/text()').re(u'发布时间：(.*)')[0].strip() \
            if response.xpath(u'//div[contains(text(),"发布时间：")]/text()').re(u'发布时间：(.*)') else "-"
        item['browse'] = response.xpath('//em[@id="totalcount"]/text()').extract_first() \
            if response.xpath('//em[@id="totalcount"]/text()').extract_first() else "-"
        item['phone'] = response.xpath('//span[@class="phone"]/text()').extract_first().strip() \
            if response.xpath('//span[@class="phone"]/text()').extract_first() else "-"
        item['creditlevel'] = response.xpath(u'//i[contains(text(),"信用等级：")]/../a/img/@title').extract_first() \
            if response.xpath(u'//i[contains(text(),"信用等级：")]/../a/img/@title').extract_first() else "-"
        item['agentcompany'] = response.xpath(u'//i[contains(text(),"所属公司：")]/../label/text()').extract_first() \
            if response.xpath(u'//i[contains(text(),"所属公司：")]/../label/text()').extract_first() else "-"
        yield item