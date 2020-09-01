# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from ganji.items import BidNewsInfo
import authome_compare
import logging

website='newsbid'

class CarSpider(scrapy.Spider):
    name = website
    start_urls = ['http://www.bidnews.cn/caigou/search-htm-page-1-kw-qichejituan.html']
    # settings.set('DOWNLOAD_DELAY', 0.5, priority='cmdline')
    def __init__(self, **kwargs):
        # report bug session
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo setting
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def parse(self,response):
        url=response.url
        yield scrapy.Request(url,self.parse_middle)

    def parse_middle(self,response):
        x=response.xpath('//table[@class="zblist_table"]/tr')
        try:
            for temp in x[1:36]:
                url = str(temp.xpath('td[3]/a/@href').extract_first())
                # url = str(temp.xpath('td[2]/a/@href').extract_first())
                yield scrapy.Request(url, callback=self.info_parse)
        except:
            for temp in x[1:36]:
                # url = str(temp.xpath('td[3]/a/@href').extract_first())
                url = str(temp.xpath('td[2]/a/@href').extract_first())
                yield scrapy.Request(url, callback=self.info_parse)
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url,callback=self.parse_middle,dont_filter=True)

    def info_parse(self,response):
        self.counts += 1
        item = BidNewsInfo()
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = response.url
        item['status'] = response.url
        item['website'] = website
        item['desc']=response.xpath('//div[@class="xq_title"]/h1/text()').extract_first() \
            if response.xpath('//div[@class="xq_title"]/h1/text()').extract_first() else "_"
        item['updatetime']=response.xpath('//div[@class="color_9 xq_time"]/text()').re('\d+\-\d+\-\d+')[0] \
            if response.xpath('//div[@class="color_9 xq_time"]/text()').re('\d+\-\d+\-\d+') else "_"
        yield item
