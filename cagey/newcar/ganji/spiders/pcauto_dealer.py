# -*- coding: utf-8 -*-
import scrapy
from ganji.items import PcautoDistributorItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re

website ='pcauto_dealer'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["price.pcauto.com.cn"]
    start_urls=['http://price.pcauto.com.cn/cars/']

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'network', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        url_temp_t = response.xpath('//div[@class="layA w88"]/div[@class="dFix"]/a')
        for url_temp in url_temp_t:
            urlbase = url_temp.xpath('@href').extract_first()
            #url_temp = response.xpath('//div[@class="layA w88"]/div[@class="dFix"]/a/@href').extract_first()
            brandid = re.findall("/price/(.*?)/", urlbase)[0]
            metadata = {"brandid": brandid}
            url = "http://price.pcauto.com.cn/shangjia/" + brandid + "/"
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_shangjia)

    def parse_shangjia(self, response):
        print "do parse_shangjia"
        metadata = response.meta['metadata']
        herfs = response.xpath('//div[@class="listTb"]//li')
        for herf in herfs:
            url = herf.xpath('div/p[1]/a/@href').extract_first()
            #print url
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)
        next_page = response.xpath(u'//a[contains(text(), "\u4e0b\u4e00\u9875")]/@href').extract_first()
        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, meta={"metadata": metadata}, callback=self.parse_shangjia)

    def parse_info(self, response):
        metadata = response.meta['metadata']
        item = PcautoDistributorItem()
        item['website'] = website
        item['brandid'] = metadata["brandid"]
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())


        item['tel'] = response.xpath('//div[@class="topleftpt"]/div[@class="otlisttl otlisttlyh"]/i/text()').extract_first()
        item['shopname'] = response.xpath('//div[@class="topleftpt"]/p[1]/text()').extract_first()
        item['shopstar'] = response.xpath('//div[@class="topleftpt"]/div[@class="pfen"]/span/i/@datas').extract_first()
        item['shoptype'] = response.xpath('//div[@class="topleftpt"]/p[@class="tit"]/i/text()').extract_first() \
            if response.xpath('//div[@class="topleftpt"]/p[@class="tit"]/i/text()') else "-"
        item['location'] = response.xpath('//div[@class="topleftpt"]/p[1]/text()').extract_first()
        item['url'] = response.url
        item['status'] = response.url

        mainbrand = "-"
        mainbrands_temp = response.xpath('//div[@class="ppbox"]/dl/dd')
        if mainbrands_temp:
            flag = 0

            for temp in mainbrands_temp:
                mainbrand_temp = temp.xpath('.//div[@class="pic-txt"]/text()').extract()[1].strip()
                if flag == 0:
                    mainbrand = mainbrand_temp
                    flag = 1
                else:
                    mainbrand += " + " + mainbrand_temp
        item['mainbrand'] = mainbrand

        promotionurl_temp = response.xpath('//dl[@class="atozixun"]/dd/span/a/@href').extract_first()
        promotionurl = response.urljoin(promotionurl_temp)
        item['promotionurl'] = promotionurl

        item['promotion'] = response.xpath('//dl[@class="atozixun"]/dd/span/a/@title').extract_first()

        yield item
