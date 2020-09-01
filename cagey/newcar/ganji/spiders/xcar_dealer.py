# -*- coding: utf-8 -*-
import scrapy
from ganji.items import aikadealerItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re

website="xcar_dealer_f"

class CarSpider(scrapy.Spider):

    name=website
    allowed_domains = ["http://www.xcar.com.cn/"]
    start_urls=['http://dealer.xcar.com.cn/']

    def __init__(self,**kwargs):
        print "do initial"
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000
        #MonGo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','network',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')
        print "finish initial"

    # brand select
    def parse(self,response):
        print "do parse"
        x=response.xpath('//div[@class="ulcon"]/a')
        print x
        for temp in x[14:len(x)]:
            urlbase=temp.xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.parse_middle,dont_filter=True)

    def parse_middle(self,response):
        print "do parse_middle"
        # brandid=re.findall('d1000/(.*).htm', response.url)[0]
        # metadata = {"brandid": brandid}
        x=response.xpath('//div[@class="main_list"][1]/ul/li')
        for temp in x[0:10]:
            urlbase=temp.xpath('a/@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.parse_maininfo,dont_filter=True)
        next_page=response.xpath('//div[@class="main_list"]/div/a[@class="page_down"]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            # yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_middle,dont_filter=True)
            yield scrapy.Request(url,callback=self.parse_middle, dont_filter=True)


    def parse_maininfo(self,response):
        print "parse_maininfo"
        # metadata = response.meta['metadata']
        item=aikadealerItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()
        # item['brandid']=metadata['brandid']
        item['tel']=response.xpath('//div[@class="tele_s"]/b/text()').extract_first() \
            if response.xpath('//div[@class="tele_s"]/b/text()').extract_first() else "-"
        item['shopname']=response.xpath('//div[@class="shop_logo"]/dl/dd/span/text()').extract_first() \
            if response.xpath('//div[@class="shop_logo"]/dl/dd/span/text()').extract_first() else "-"
        item['shoptype']=response.xpath('//div[@class="store carx_map"]/dl[2]/dd/text()').extract_first() \
            if response.xpath('//div[@class="store carx_map"]/dl[2]/dd/text()').extract_first() else "-"
        item['mainbrand']=response.xpath('//dl[@class="pp_list clearfix"]/dd/span/text()').extract_first() \
            if response.xpath('//dl[@class="pp_list clearfix"]/dd/span/text()').extract_first() else "-"
        item['location']=response.xpath(u'//dt[contains(text(),"\u5730\u5740\uff1a")]/../dd/p/text()').extract_first() \
            if response.xpath(u'//dt[contains(text(),"\u5730\u5740\uff1a")]/../dd/p/text()').extract_first() else "-"
        item['status']=response.url
        item['promotion']=response.xpath('//span[@class="yh_tit"]/a/@title').extract_first() \
            if response.xpath('//span[@class="yh_tit"]/a/@title').extract_first() else "-"
        item['promotionurl']=response.urljoin(response.xpath('//span[@class="yh_tit"]/a/@href').extract_first())
        item['salesregion']=response.xpath('//div[@class="tele_s"]/em/text()').extract_first() \
            if response.xpath('//div[@class="tele_s"]/em/text()').extract_first() else "-"
        yield item