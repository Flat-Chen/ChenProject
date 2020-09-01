# -*- coding: utf-8 -*-
import scrapy
from ganji.items import Pcauto_comments
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import random
import re
import hashlib
from hashlib import md5

website='pcauto_comments'

class CarSpider(scrapy.Spider):
    name=website
    # allowed_domains=['http://www.pcauto.com.cn/']
    start_urls = ['http://price.pcauto.com.cn/cars/']

    def __init__(self,**kwargs):
        # problem report
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=1010000
        #mongo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    # series select
    def parse(self,response):
        logging.log(msg="do the parse step",level=logging.INFO)
        # x=response.xpath('//div[@class="wrap iContent"]/div[@class="main clearfix"]/div[2]/div[@class="modA"]/div[2]/dl/dd/p[1]/a')
        x = response.xpath("//*[@class='tit']")
        for temp in x:
            urlbase=str(temp.xpath('./a/@href').extract_first())
            url='http://price.pcauto.com.cn/comment'+urlbase
            yield scrapy.Request(url,self.parse_main_info)

    def parse_main_info(self,response):
        logging.log(msg="do the parse_main_info step",level=logging.INFO)
        item = Pcauto_comments()
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = response.url
        item['website'] = website
        item['brand']=response.xpath('//div[@class="pos-mark"]/a[3]/text()').extract_first()
        x=response.xpath('//div[@class="scollbody"]/div[@class="litDy clearfix"]')
        for temp in x:
            item['ext_vehicle_type']=temp.xpath('table/tr/td/div[1]/div[1]/div[2]/a/text()').extract_first()
            item['user_name']=temp.xpath('table/tr/td/div[1]/div[1]/div[1]/p/a/text()').extract_first()
            item['appearance']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[3]/span/text()').extract_first()
            item['why_buy']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[1]/span/text()').extract_first()
            item['unsatisfaction']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[2]/span/text()').extract_first()
            item['control_suv']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[8]/span/text()').extract_first()
            item['comfort']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[10]/span/text()').extract_first()
            item['power']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[7]/span/text()').extract_first()
            item['fuel']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[9]/span/text()').extract_first()
            item['space']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[5]/span/text()').extract_first()
            item['trim']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[4]/span/text()').extract_first()
            item['equipment']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[6]/span/text()').extract_first()
            item['score_app']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[1]/b/text()').extract_first()
            item['score_trim']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[2]/b/text()').extract_first()
            item['score_space']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[3]/b/text()').extract_first()
            item['score_equipment']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[4]/b/text()').extract_first()
            item['score_power']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[5]/b/text()').extract_first()
            item['score_control']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[6]/b/text()').extract_first()
            item['score_fuel']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[7]/b/text()').extract_first()
            item['score_comfort']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[8]/b/text()').extract_first()
            status = item['user_name'].encode('utf-8')
            item['status']= hashlib.md5(status).hexdigest()
            yield item
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url=str(next_page[1].extract())
            yield scrapy.Request(url,callback=self.parse_main_info,dont_filter=True)

