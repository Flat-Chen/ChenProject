# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from ganji.items import AutohomeCarUpcoming
import re



website ='autohome_upcoming'

class CarSpider(scrapy.Spider):

    name = website
    #allowed_domains = ["dealer.auto.sohu.com"]
    start_urls = [
        # "http://www.autohome.com.cn/newbrand/"
        "https://www.autohome.com.cn/newbrand/"
    ]
    def __init__(self,**kwargs):
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #city
    def parse(self, response):
        divs = response.xpath("//*[@class='select-list']")
        for div in divs:
            metadata = {"uptime":div.xpath("./h4/text()").extract_first()}
            lis = div.xpath("./ul/li")
            for li in lis:
                yield scrapy.Request(response.urljoin(li.xpath("./a/@href").extract_first()), meta={'metadata': metadata}, callback=self.sales_parse)
        # for sel in response.xpath('//div[@class="uibox-con upcoming-list"]/div[@class="wrap"]'):
        #     uptime=sel.xpath('p[@class="date"]/text()').extract_first()
        #     #title=sel.xpath('p[@class="description"]/a/text()').extract_first()
        #     urlbase=response.urljoin(sel.xpath('p[@class="description"]/a/@href').extract_first())
        #     metadata={'uptime': uptime}
        #     yield scrapy.Request(urlbase, meta={'metadata': metadata}, callback=self.sales_parse)

    #sales
    def sales_parse(self,response):
        self.counts+=1
        item=AutohomeCarUpcoming()
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = response.url
        item['status'] = response.url
        item['website'] = website
        metadata = dict(response.meta['metadata'])
        if metadata:
            item['uptime']=metadata['uptime']
            #item['title'] = metadata['title']
        strll=response.xpath('//div[@class="area article"]/h1/text()').extract_first()
        item['title']=strll.strip()
        item['trimid']=''.join(response.xpath('//div[@class="subnav-title-name"]/a/@href').re('\d+\.?\d*')) \
            if response.xpath('//div[@class="subnav-title-name"]/a/@href') else "-"
        item['shortdesc']=response.xpath('//div[@class="subnav-title-name"]/a/text()').extract_first() \
            if response.xpath('//div[@class="subnav-title-name"]/a') else "-"
        yield item






