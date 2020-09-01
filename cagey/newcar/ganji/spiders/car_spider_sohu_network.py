# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from ganji.items import SuhuagencyItem
import json
import re
import logging


website ='sohu_network'

class CarSpider(scrapy.Spider):

    name = website
    #allowed_domains = ["dealer.auto.sohu.com"]
    start_urls = [
        "http://auto.sohu.com/dealer/static/cityArr.js"
    ]

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

    #city
    def parse(self, response):
        jsdata = json.loads(response.body_as_unicode().replace("var cityArr = ",""))
        for pd in jsdata:
            for ct in jsdata[pd]:
                provinceid=pd
                cityid=ct['id']
                cityname=ct['name']
                urlbase="http://dealer.auto.sohu.com/map/?city="+cityid
                metadata={'provinceid':provinceid,'cityid':cityid,'cityname':cityname}
                yield scrapy.Request(urlbase, meta={'metadata': metadata}, callback=self.agency_parse, dont_filter=True)

    #agency
    def agency_parse(self,response):
        metadata=response.meta['metadata']
        data=response.xpath('//body/script[@type="text/javascript"]/text()').extract_first()
        if data:
            data=re.findall('"id":"'+'\d+',data)
            for line in data:
                agencyid=re.findall('\d+',line.split(':')[-1])[0]
                metadata_agency=dict({'agencyid':agencyid},**metadata)
                urlbase="http://dealer.auto.sohu.com/"+agencyid
                yield scrapy.Request(urlbase, meta={'metadata': metadata_agency}, callback=self.infro_parse)


    def infro_parse(self,response):
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        item=SuhuagencyItem()
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = response.url
        item['status'] = response.url
        item['website'] = website
        item['datasave'] = response.xpath('//html').extract_first()
        metadata = response.meta['metadata']
        if metadata:
            item['provinceid']=metadata['provinceid']
            item['cityid'] = metadata['cityid']
            item['cityname'] = metadata['cityname']
            item['agencyid'] = metadata['agencyid']
        item['agencyname']=response.xpath('//h3[@class="group-title"]/a/text()').extract_first() \
            if response.xpath('//h3[@class="group-title"]/a/text()') else "-"
        item['mainbrand']=response.xpath('//ul[@class="group-list"]/li/span[@class="color1"]/text()').extract_first().strip() \
            if response.xpath('//ul[@class="group-list"]/li/span[@class="color1"]/text()') else "-"
        item['telephone']=response.xpath('//ul[@class="group-list"]/li/span[@class="color2 emClass"]/text()').extract_first() \
            if response.xpath('//ul[@class="group-list"]/li/span[@class="color2 emClass"]/text()') else "-"
        item['adress']=response.xpath('//ul[@class="group-list"]/li/p[@class="adress-info"]/span/text()').extract_first() \
            if response.xpath('//ul[@class="group-list"]/li/p[@class="adress-info"]/span/text()') else "-"
        if response.xpath('//span[@class="pt_4s"]') :
            item['shopclass']=u'4S\u5e97'
        elif response.xpath('//span[@class="rz_zh"]'):
            item['shopclass']=u'\u8ba4\u8bc1\u7efc\u5408\u5e97'
        elif response.xpath('//span[@class="rz_port"]'):
            item['shopclass']=u'\u8ba4\u8bc1\u6e2f\u53e3\u5e97'
        else:
            item['shopclass']="-"
        item['mainclass']=';'.join(response.xpath('//div[@class="search-model"]/h4/text()').extract()) \
            if response.xpath('//div[@class="search-model"]/h4/text()') else "-"
        item['seriesclass']=';'.join(response.xpath('//div[@class="search-model"]/ul/li/a/text()').extract()) \
            if response.xpath('//div[@class="search-model"]/ul/li/a/text()') else "-"
        yield item






