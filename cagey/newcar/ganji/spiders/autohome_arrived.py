# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from ganji.items import AutohomeCarArrived
import re



website ='car_autohome_arrived'

class CarSpider(scrapy.Spider):

    name = website
    #allowed_domains = ["dealer.auto.sohu.com"]
    # start_urls = [
    #     "http://www.autohome.com.cn/newbrand/"
    # ]
    def __init__(self,**kwargs):
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        urldata =[]
        for y in range(2008,2018):
            urlbase="http://www.autohome.com.cn/newbrand/"+str(y)
            metadata = {"produceyear": y}
            urld=scrapy.Request(urlbase,meta={'metadata': metadata},dont_filter=True)
            urldata.append(urld)
        return urldata

    #city
    def parse(self, response):
        metadata = response.meta['metadata']
        for sel in response.xpath('//div[@class="uibox-con cars-list"]/div[@class="select-list"]'):
            arrivedtime=sel.xpath('h4/text()').extract_first()
            for xp in sel.xpath("ul/li"):
                title=xp.xpath('a/span/text()').extract_first()
                urlbase=xp.xpath('a/@href').extract_first()
                primdata=dict({'arrivedtime': arrivedtime,'title':title},**metadata)
                yield scrapy.Request(urlbase, meta={'metadata': primdata}, callback=self.sales_parse)

    #sales
    def sales_parse(self,response):
        self.counts+=1
        item=AutohomeCarArrived()
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = response.url
        item['status'] = response.url
        item['website'] = website
        metadata = dict(response.meta['metadata'])
        if metadata:
            item['produceyear']=metadata['produceyear']
            item['arrivedtime']=metadata['arrivedtime']
            item['title'] = metadata['title']
        item['trimid']=''.join(response.xpath('//div[@class="subnav-title-name"]/a/@href').re('\d+\.?\d*')) \
            if response.xpath('//div[@class="subnav-title-name"]/a/@href') else "-"
        item['shortdesc']=response.xpath('//div[@class="subnav-title-name"]/a/text()').extract_first() \
            if response.xpath('//div[@class="subnav-title-name"]/a') else "-"
        yield item






