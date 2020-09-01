# -*- coding: utf-8 -*-
import scrapy
import time
from ganji.items import yichedealeritem
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import urllib
#import car_spider_iautos
import os

website='yiche_dealer_f_new'

class CarSpider(scrapy.Spider):
    name=website
    allowed_domains=["bitauto.com"]
    start_urls=["http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&pid=0&rt=master&callback=callback#"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        #problem report

        ###
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000
        #mongo

        ###########
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','network',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        x = response.xpath('//p/text()').extract_first()
        temp = re.findall('DataList:(.*)}\)', x)[0]
        data = json.loads(temp)
        length = len(data)
        urlSpells = []
        for i in range(0, length):
            temp=data[i]['urlSpell']

            metadata={"brandid":temp}
            url="http://dealer.bitauto.com/beijing/"+str(temp)+"/"
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.middle_parse)

    #品牌
    def middle_parse(self,response):
        metadata=response.meta['metadata']
        x = response.xpath("//div[@id='d_pro']/div/ul/li/a")
        for temp in x:
            urlbase=temp.xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"metadata":metadata},callback=self.middle2_parse)

    #城市
    def middle2_parse(self, response):
        metadata = response.meta['metadata']
        x = response.xpath('//div[@class="row dealer-list"]')
        for temp in x:
            urlbase = temp.xpath('div/h6/a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.middle3_parse)



        next_page=''
        next_page=response.xpath('//div[@class="pagination"]/div/a[@class="next_on"]/@href').extract_first()
        if next_page:
            next_url=response.urljoin(next_page)
            yield scrapy.Request(next_url,meta={"metadata":metadata},callback=self.middle2_parse)

    #经销商
    def middle3_parse(self, response):
        metadata = response.meta['metadata']
        # with open("C:\Users\Admin\Desktop\hb\hb.text", 'a') as f:
        #     print('********************************************')
        #     telp = response.xpath('//meta[@name="description"]').extract_first()
        #     json.dump({'tel':re.findall(u'电话：(.*?)】',telp)[0],
        #                'shopname':response.xpath('//h2/strong/text()').extract_first(),
        #                'brandid':metadata["brandid"],
        #                'location':response.xpath('//ul/li/div[@class="ads"]/text()').extract_first(),
        #                'mainbrand':response.xpath('//div/div[@class="carmore"]/text()').extract_first(),
        #                'promotionurl': response.urljoin(response.xpath('//h2/a[@class="ad"]/@href').extract_first()),
        #                'skype': response.xpath('//div[@class="info_c"]/a/text()').extract_first(),
        #                'promotion': response.xpath('//h2/a[@class="ad"]/text()').extract_first()
        #                },
        #               f)
        #     f.write("\n")


        item = yichedealeritem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        telp=response.xpath('//meta[@name="description"]').extract_first()
        item['tel']=re.findall(u'电话：(.*?)】',telp)[0]
        item['shopname']=response.xpath('//h2/strong/text()').extract_first()
        item['shopstar']='-'
        item['shoptype']=response.xpath('//ul/li[@class="jb"]/div/text()').extract_first()
        item['brandid']=metadata["brandid"]
        item['location']=response.xpath('//ul/li/div[@class="ads"]/text()').extract_first()
        item['mainbrand']=response.xpath('//div/div[@class="carmore"]/text()').extract_first()
        item['url'] = response.url
        item['status'] = response.url
        item['promotionurl']=response.urljoin(response.xpath('//h2/a[@class="ad"]/@href').extract_first())
        item['saleregeion']='-'
        item['skype']=response.xpath('//div[@class="info_c"]/a/text()').extract_first()
        item['promotion']=response.xpath('//h2/a[@class="ad"]/text()').extract_first()
        yield item

















