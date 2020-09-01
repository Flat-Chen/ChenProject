# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from ganji.items import Okcis
import logging

website='okcis'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['http://www.okcis.cn/apporg/hot/bn/qiche/1.html']
    def __init__(self,**kwargs):
        # report bug session
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000
        # mongo setting
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self,response):
        url=response.url
        yield scrapy.Request(url,self.parse_middle)

    def parse_middle(self,response):
        for temp in response.xpath('//div[@class="liebiaos_20140314"]/table/tr'):
            urlbase=str(temp.xpath('td[2]/h4/a/@href').extract_first())
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.info_parse)
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/../a/@href')
        if next_page:
            url=response.urljoin(next_page.extract_first())
            yield scrapy.Request(url,callback=self.parse_middle,dont_filter=True)


    def info_parse(self,response):
        self.counts+=1
        item=Okcis()
        item['grabtime']=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        item['url']=response.url
        item['status']=response.url
        item['website']=website
        desc=response.xpath('//div[@class="main_m01_20140314"]/h3/text()').extract_first()
        item['desc']=desc.strip()
        item['updatetime']=response.xpath('//div[@class="jbxx_20140314"]/p[7]/text()').re('\d+\-\d+\-\d+')[0] \
            if response.xpath('//div[@class="jbxx_20140314"]/p[7]/text()').re('\d+\-\d+\-\d+') else "_"

        strlist=response.xpath('//div[@class="jbxx_20140314"]/p/a/text()').extract() \
            if response.xpath('//div[@class="jbxx_20140314"]/p/a/text()').extract() else "_"
        string=''
        for pp in strlist:
            string=string+' '+pp
        item['label']=string
        yield item
