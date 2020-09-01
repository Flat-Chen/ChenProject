# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from ganji.items import ChinaBiddingInfo
import authome_compare
import logging

website='chinabidding'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['https://www.chinabidding.cn/sd/%E6%B1%BD%E8%BD%A6/']
    def __init__(self,**kwargs):
        # report bug session
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000
        #Mongo setting
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        # logging.log(msg="parse", level=logging.INFO)
        url=response.url
        yield scrapy.Request(url,self.parse_middle)

    def parse_middle(self,response):
        # print response.url+"1111"
        # logging.log(msg="parse_middle", level=logging.INFO)
        for sel in response.xpath('//tr[@class="rm_nei"]/td/h2'):
            urlbase = str(sel.xpath('a/@href').extract_first())
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.info_parse)
        # get next_page
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/../a/@href')
        if next_page:
            url=response.urljoin(next_page.extract_first())
            # print url
            yield scrapy.Request(url,callback=self.parse_middle,dont_filter=True)
            # logging.log(msg=url,level=logging.INFO)



    def info_parse(self,response):
        # logging.log(msg="info_parse",level=logging.INFO)
        self.counts+=1
        item=ChinaBiddingInfo()
        item['grabtime']=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        item['url']=response.url
        item['status']=response.url
        item['website']=website
        item['desc']=response.xpath('//h1[@class="da_biao"]/text()').extract_first()
        item['updatetime']=response.xpath('//div[@class="fl xiab_1"]/span/text()').extract_first()
        for temp in response.xpath('//div[@class="fl gjc"]'):
            string = temp.xpath('a/text()').extract()

        stringlist=''
        for pp in string:
            stringlist=stringlist+' '+pp
        item['label']=stringlist
        yield item


