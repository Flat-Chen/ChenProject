# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomeItem_network
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re



website ='autohome_network'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls=['http://dealer.autohome.com.cn/Ajax?actionName=GetAreasAjax&ajaxProvinceId=0'
                '&ajaxCityId=0&ajaxBrandid=0&ajaxManufactoryid=0&ajaxSeriesid=0',]

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

    #get region list
    def parse(self, response):
        # list value
        jsonlist = json.loads(response.xpath('//p/text()').extract_first()) \
                if response.xpath('//p/text()').extract_first() else '-'

        for region in jsonlist['AreaInfoGroups']:
            for prov in region['Values']:
                provdata =dict()
                provdata['Key'] = prov['FirstChar']
                provdata['prov_ID'] = prov['Id']
                provdata['prov_Name'] = prov['Name']
                provdata['prov_Pinyin'] = prov['Pinyin']
                provdata['prov_Count'] = prov['Count']
                for city in prov['Cities']:
                    citydata=dict()
                    citydata['city_ID'] = city['Id']
                    citydata['city_Name'] = city['Name']
                    citydata['city_Pinyin'] = city['Pinyin']
                    citydata['city_Count'] = city['Count']
                    citydata=dict(citydata,**provdata)
                    url='http://dealer.autohome.com.cn/'+city['Pinyin']
                    yield scrapy.Request(url,
                                         meta={'citydata':citydata},
                                         callback=self.parse_brand)
                    # get region list
    #get brand
    def parse_brand(self, response):
        for brand in response.xpath('//a[@class="item"]'):
            brandname =brand.xpath('text()').extract_first()
            brandid=brand.xpath('@href').re('brandId=([\s\S]*?)&')[0] \
                if brand.xpath('@href').re('brandId=([\s\S]*?)&') else '-'
            branddata={'brandname':brandname,'brandid':brandid}
            urlbase = brand.xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,
                                 meta={'citydata':  response.meta['citydata'],'branddata':branddata},
                                 callback=self.parse_factory)

    # get factory
    def parse_factory(self, response):
        for factory in response.xpath('//li[@class="row row-child data-series-item"]/div'):
            factoryname =factory.xpath('span/text()').extract_first()
            factoryid=factory.xpath(u'a[contains(text(),"全部")]/@href').re('factoryId=([\s\S]*?)&')[0] \
                if factory.xpath(u'a[contains(text(),"全部")]/@href').re('factoryId=([\s\S]*?)&') else '-'
            factorydata={'factoryname':factoryname,'factoryid':factoryid}
            urlbase = factory.xpath(u'a[contains(text(),"全部")]/@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,
                                 meta={'citydata': response.meta['citydata'],'branddata': response.meta['branddata'],'factorydata':factorydata},
                                 callback=self.parse_network)

    # get car infor
    def parse_network(self, response):
        for shop in response.xpath('//li[@class="list-item"]'):
            item=AutohomeItem_network()
            ####metadata:
            #city
            item['Key'] = response.meta['citydata']['Key']
            item['prov_ID'] = response.meta['citydata']['prov_ID']
            item['prov_Name'] = response.meta['citydata']['prov_Name']
            item['prov_Pinyin'] = response.meta['citydata']['prov_Pinyin']
            item['prov_Count'] = response.meta['citydata']['prov_Count']
            item['city_ID'] = response.meta['citydata']['city_ID']
            item['city_Name'] = response.meta['citydata']['city_Name']
            item['city_Pinyin'] = response.meta['citydata']['city_Pinyin']
            item['city_Count'] = response.meta['citydata']['city_Count']
            #brand
            item['brandname'] = response.meta['branddata']['brandname']
            item['brandid'] = response.meta['branddata']['brandid']
            #factory
            item['factoryname'] = response.meta['factorydata']['factoryname']
            item['factoryid'] = response.meta['factorydata']['factoryid']
            ####key info
            item['shopname'] =shop.xpath('ul/li[@class="tit-row"]/a/span/text()').extract_first() \
                if shop.xpath('ul/li[@class="tit-row"]/a/span/text()') else '-'
            item['url']=shop.xpath('ul/li[@class="tit-row"]/a/@href').extract_first() \
                if shop.xpath('ul/li[@class="tit-row"]/a/@href') else '-'
            if shop.xpath('ul/li[@class="tit-row"]/span[@class="green"]'):
                item['shoptype'] = shop.xpath('ul/li[@class="tit-row"]/span[@class="green"]/text()').extract_first() \
                    if shop.xpath('ul/li[@class="tit-row"]/span[@class="green"]/text()') else '-'
                item['shopcolor'] = 'green'
            elif shop.xpath('ul/li[@class="tit-row"]/span[@class="blue"]'):
                item['shoptype'] = shop.xpath('ul/li[@class="tit-row"]/span[@class="blue"]/text()').extract_first() \
                    if shop.xpath('ul/li[@class="tit-row"]/span[@class="blue"]/text()') else '-'
                item['shopcolor'] = 'blue'
            item['shopstar'] = str(int(shop.xpath('ul/li[@class="tit-row"]/span[@class="icon star"]/i/@style').re('\d+')[0])*5/100) \
                if shop.xpath('ul/li[@class="tit-row"]/span[@class="icon star"]/i/@style').re('\d+') else '-'
            ####salemodel and saleprice
            item['modelnumber']=str(shop.xpath('ul/li[2]/a/text()').re('\d+')[0]) \
                if shop.xpath('ul/li[2]/a/text()').re('\d+') else '-'
            item['mainbrands'] = '-'.join(shop.xpath('ul/li[2]/em/text()').extract()) \
                if shop.xpath('ul/li[2]/em/text()') else '-'
            item['tel'] = shop.xpath('ul/li[3]/span[@class="tel"]/text()').extract_first() \
                if shop.xpath('ul/li[3]/span[@class="tel"]/text()') else '-'
            item['saleregion'] = shop.xpath('ul/li[3]/span[@class="sale-whole"]/span/text()').extract_first() \
                if shop.xpath('ul/li[3]/span[@class="sale-whole"]/span/text()') else '-'
            item['priceurl']=shop.xpath('ul/li[2]/a/@href').extract_first() \
                if shop.xpath('ul/li[2]/a/@href') else '-'
            ####location
            item['location']=shop.xpath('ul/li[4]/span/text()').extract_first().replace(u'址：','') \
                if shop.xpath('ul/li[4]/span/text()') else '-'
            item['locationurl'] = shop.xpath('ul/li[4]/a/@href').extract_first() \
                if shop.xpath('ul/li[4]/a/@href') else '-'
            ####promotion
            item['promotion'] = shop.xpath('ul/li[5]/a/text()').extract_first() \
                if shop.xpath('ul/li[5]/a/text()') else '-'
            item['promotionurl'] = shop.xpath('ul/li[5]/a/@href').extract_first() \
                if shop.xpath('ul/li[5]/a/text()') else '-'
            ####img
            item['imageurl'] = shop.xpath('a/img/@src').extract_first() \
                if shop.xpath('a/img/@src') else '-'
            ####normal infor
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = item['url']
            yield item
        ##
        #下一页跳转
        ascnum = int(response.xpath('//span[@class= "num data-dealer-count"]/text()').extract_first())
        maxpage = int(ascnum/15)+1
        page = re.findall(r"\d+",re.findall(r"pageIndex=\d+",response.url)[0])[0]\
            if re.findall(r"pageIndex=\d+",response.url) else "-"
        if page!="-":
            pagenext=int(page)+1
            if pagenext <= maxpage:
                next_pageurl = re.sub("pageIndex=\d+", "pageIndex=" + str(pagenext), response.url)
                #print next_pageurl
                yield scrapy.Request(next_pageurl,
                                 meta={'citydata': response.meta['citydata'], 'branddata': response.meta['branddata'],
                                       'factorydata': response.meta['factorydata']},
                                 callback=self.parse_network)
        ##
        # pagenext=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        # if not(pagenext=='javascript:void(0)'):
        #     url=response.urljoin(pagenext)
        #     yield scrapy.Request(url,
        #                          meta={'citydata': response.meta['citydata'], 'branddata': response.meta['branddata'],
        #                                'factorydata': response.meta['factorydata']},
        #                          callback=self.parse_network)

        ##
        kindnext=response.xpath('//div[@class="tab"]/a[@class="nav"]/@href').extract_first()
        if kindnext:
            if not(kindnext.find('kindId=2')==-1):
                url = response.urljoin(kindnext)
                yield scrapy.Request(url,
                                     meta={'citydata': response.meta['citydata'], 'branddata': response.meta['branddata'],
                                           'factorydata': response.meta['factorydata']},
                                     callback=self.parse_network)