# -*- coding: utf-8 -*-
import scrapy
from ganji.items import autohome_compare
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website ='autohome_general_store'

class CarSpider(scrapy.Spider):
    name = website
    # allowed_domains = ["autohome.com.cn"]
    #选择城市，从这个入口获得城市信息
    start_urls = ['http://dealer.autohome.com.cn/Ajax?actionName=GetAreasAjax&ajaxProvinceId=0&ajaxCityId=310100&ajaxBrandid=0&ajaxManufactoryid=0&ajaxSeriesid=0']
    # start_urls = ['http://www.autohome.com.cn/509/']

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        # settings.set('MONGODB_DB', 'auto_compare', priority='cmdline')
        settings.set('MONGODB_DB', "newcar", priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        citylist = []
        citylist_base = json.loads(response.body)
        city_unit = []
        # HotCites = citylist_base['HotCites'] #这个列表在下面是重复出现的
        AreaInfoGroups = citylist_base['AreaInfoGroups']
        for i in AreaInfoGroups:
            j = i['Values']
            for k in j:
                citylist.append(k)
        for city in citylist:
            city_pinyin = city['Pinyin']
            url = "http://dealer.autohome.com.cn/" \
                  + city_pinyin \
                  + "?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=1&kindId=2&orderType=0&_abtest=0#pvareaid=2113390"
            yield scrapy.Request(url, callback=self.parse_middle1, dont_filter=True)


    def parse_middle1(self, response):
        if response.xpath('//div[@class="tab"]/a[contains(text(),"\u7efc\u5408\u7ecf\u9500\u5546")]'):
            urlbase = response.xpath('//ul[@class="list-box"]/li/a/@href').extract_fiorst()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        # count
        item = autohome_compare()
        self.counts += 1
        print "download              " + str(self.counts) + "                  items"
        # item loader
        item = autohome_compare()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['familyid'] = re.findall("\d+", response.url)[0]
        item['shortdesc'] = response.xpath('//span[@class="cd60000"]/text()').extract_first()

    #family parse
    def parse_familyinfo(self, response):
        # list value
        items = eval(response.xpath('//p/text()').extract_first())
        for factory in items['result']['allSellSeries']:
            for family in factory['SeriesItems']:
                familyid = str(family['id'])
                url = 'http://k.autohome.com.cn/compareseries/' + str(familyid) + "/"
                yield scrapy.Request(url, callback=self.parse_compare)

    def parse_compare(self,response):
        # count
        print "response.url", response.url
        self.counts += 1
        print "download              " + str(self.counts) + "                  items"
        # item loader
        item = autohome_compare()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['familyid'] = re.findall("\d+",response.url)[0]
        item['shortdesc'] = response.xpath('//span[@class="cd60000"]/text()').extract_first()

        for data in response.xpath('//div[@class="ranking-tit rank-bg-gray seriesItemBox"]'):
            if len(data.xpath('div/span').extract())!=0:
                for rank in data.xpath('div/span'):
                    item['rank'] = rank.xpath('text()').extract_first()
            else:
                item['rank'] = '第1名'

            for rankname in data.xpath('h4/a'):
                item['comparename'] = rankname.xpath('text()').extract_first()
                item['compareurl'] = rankname.xpath('@href').extract_first()
                item['comparefamilyid'] = rankname.xpath('@href').re('\d+')[0]
                item['status'] = hashlib.md5(item['compareurl']+item['url']).hexdigest()
                yield item

