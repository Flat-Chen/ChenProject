# -*- coding: utf-8 -*-
import scrapy
from ganji.items import yicheItem_price
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

website ='yiche_price'

class CarSpider(scrapy.Spider):

    name = website
   # allowed_domains = ["bitauto.com"]
    start_urls=['http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=baojia',]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 4000000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'network', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(execu'uutable_path="/usr/local/phantomjs/bin/phantomjs")
        self.browser = webdriver.PhantomJS(executable_path="/home/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
        self.browser.set_page_load_timeout(10)
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self):
        self.browser.quit()

    # get factory
    def parse(self, response):
        jsonbrand = response.xpath('//pre/text()').re('JsonpCallBack\(([\s\S]*?)\)')[0]
        jsonbrand = jsonbrand.replace('{', '{"').replace('SP:01','SP01').replace(':', '":').replace(',', ',"').replace(',"{',',{').replace('http":', 'http:').replace('https":', 'https:').replace("\"\"bsId\"\"", "\"bsId\"").replace("\"\"tagName\"\"", "\"tagName\"")
        print(jsonbrand[220:240])
        jsonbrand = json.loads(jsonbrand)
        charkeys = jsonbrand['brand'].keys()
        for charkey in charkeys:
            for brand in jsonbrand['brand'][charkey]:
                brandname = brand['name']
                brandid = brand['id']
                brandurl = brand['url']
                brandnum=brand['num']
                urlbase ='http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=baojia&pagetype=masterbrand&objid='\
                         +str(brandid)
                familydata = {'brandname': brandname, 'brandid': brandid, 'brandurl': brandurl,'brandnum':brandnum}
                yield scrapy.Request(urlbase,meta={'familydata': familydata},
                                             callback=self.parse_factory)

    #get factory
    def parse_factory(self, response):
        jsonbrand = response.xpath('//pre/text()').re('JsonpCallBack\(([\s\S]*?}]})\)')[0]
        jsonbrand=jsonbrand.replace('{', '{"').replace('SP:01', 'SP01').replace(':', '":').replace(',', ',"').replace(',"{', ',{').replace('http":','http:').replace('https":', 'https:').replace("\"\"bsId\"\"", "\"bsId\"").replace("\"\"tagName\"\"", "\"tagName\"")
        jsonbrand=json.loads(jsonbrand)
        charkeys=jsonbrand['brand'].keys()
        brandid_key=response.meta['familydata']['brandid']
        for charkey in charkeys:
            for brand in jsonbrand['brand'][charkey]:
                brandid =brand['id']
                if brandid_key==brandid:
                    for factory in brand['child']:
                        factoryname=factory['name']
                        factorynum=factory['num']
                        factoryid = re.findall('b([\s\S]*?)/',factory['url'])[0]  \
                            if re.findall('b([\s\S]*?)/',factory['url']) else factory['url']
                        factoryurl =  factory['url']
                        familydata={'factoryname':factoryname,'factorynum':factorynum,'factoryid':factoryid,'factoryurl':factoryurl}
                        familydata =dict(familydata,**response.meta['familydata'])
                        if factory['type']=='cs':
                            familyname = factory['name']
                            familynum = factory['num']
                            familyid = re.findall('nb([\s\S]*?)/', factory['url'])[0] \
                                if re.findall('nb([\s\S]*?)/', factory['url']) else factory['url']
                            familyurl = '/nb'+familyid+'_c0/'
                            data = {'familyname': familyname, 'familynum': familynum, 'familyid': familyid,
                                    'familyurl': familyurl}
                            familydata = dict(familydata, **data)
                            urlbase = 'http://price.bitauto.com' + familyurl
                            yield scrapy.Request(urlbase,
                                                 meta={'familydata': familydata},
                                                 callback=self.parse_model)
                        else:
                            for family in factory['child']:
                                familyname =family['name']
                                familynum = family['num']
                                familyid = re.findall('nb([\s\S]*?)/',family['url'])[0]  \
                                    if re.findall('nb([\s\S]*?)/',family['url']) else family['url']
                                familyurl = '/nb' + familyid + '_c0/'
                                data ={'familyname':familyname,'familynum':familynum,'familyid':familyid,'familyurl':familyurl}
                                familydata=dict(familydata,**data)
                                urlbase = 'http://price.bitauto.com'+familyurl
                                yield scrapy.Request(urlbase,
                                                     meta={'familydata':familydata},
                                                     callback=self.parse_model)

    # get factory
    def parse_model(self, response):
        print(response.xpath('//table[@id="allzxtable"]/tbody/tr/td[1]/a/@href'))
        for href in response.xpath('//table[@id="allzxtable"]/tbody/tr/td[1]/a/@href'):
            for i in [0,1,2]:
                urlbase ='http://price.bitauto.com'+href.extract()+'?bizmode='+str(i)
                yield scrapy.Request(urlbase,
                                     meta={'familydata': response.meta['familydata'],'type':str(i)},
                                     callback=self.parse_price)

    # get car infor
    def parse_price(self, response):
        item=yicheItem_price()
        ####metadata:
        #brand
        item['brandname'] = response.meta['familydata']['brandname']
        item['brandid'] = response.meta['familydata']['brandid']
        item['brandurl'] = response.meta['familydata']['brandurl']
        item['brandnum'] = response.meta['familydata']['brandnum']
        item['factoryname'] = response.meta['familydata']['factoryname']
        item['factorynum'] = response.meta['familydata']['factorynum']
        item['factoryid'] = response.meta['familydata']['factoryid']
        item['factoryurl'] = response.meta['familydata']['factoryurl']
        item['familyname'] = response.meta['familydata']['familyname']
        item['familynum'] = response.meta['familydata']['familynum']
        item['familyid'] = response.meta['familydata']['familyid']
        item['familyurl'] = response.meta['familydata']['familyurl']
        #model
        item['modelid'] = re.findall('\d+', response.url)[0] \
            if re.findall('\d+', response.url) else '-'
        item['model'] = response.xpath('//a[@class="arrow-down h5"]/text()').extract_first().strip() \
            if response.xpath('//a[@class="arrow-down h5"]/text()') else '-'
        #key
        item['type'] = response.meta['type']
        ####key info
        for shop in response.xpath('//div[@class="row offer-list"]'):
            item_new = yicheItem_price()
            item_new['guideprice'] = shop.xpath('div[2]/div[1]/div[1]/p[1]/text()').extract_first().replace(u'万','') \
                if shop.xpath('div[2]/div[1]/div[1]/p[1]/text()') else '-'
            item_new['shopid'] = shop.xpath('div/h6/a/@href').re('\d+')[0] \
                if shop.xpath('div/h6/a/@href') else '-'
            item_new['shopname'] =shop.xpath('div/h6/a/text()').extract_first() \
                if shop.xpath('div/h6/a/text()') else '-'
            item_new['url']=shop.xpath('div/h6/a/@href').extract_first() \
                if shop.xpath('div/h6/a/@href') else '-'
            item_new['shopfullname'] = shop.xpath('div/h6/a/@title').extract_first() \
                if shop.xpath('div/h6/a/@title') else '-'
            if item['type']=='0':
                item_new['shoptype'] = u'综合店'
            elif item['type']=='1':
                item_new['shoptype'] = u'4S店'
            elif item['type']=='2':
                item_new['shoptype'] = u'特许店'
            ####salemodel and saleprice
            item_new['tel'] = shop.xpath(u'div[1]/p[@class="tel"]/span[2]/text()').re("\d+") \
                if shop.xpath(u'div[1]/p[@class="tel"]/span[2]/text()') else '-'
            item_new['tel'] = '-'.join(item_new['tel'])
            item_new['tel400'] = shop.xpath(u'div[1]/p[@class="tel"]/span[3]/text()').re("\d+\-\d+\-\d+")[0] \
                if shop.xpath(u'div[1]/p[@class="tel"]/span[3]/text()') else '-'
            item_new['saleregion'] = shop.xpath(u'div[1]/p[@class="tel"]/span[3]/span[2]/@title').extract_first() \
                if shop.xpath(u'div[1]/p[@class="tel"]/span[3]/span[2]/@title') else '-'
            ####location
            item_new['location']=shop.xpath(u'div[1]/p[@class="add"]/span[2]/text()').extract_first() \
                if shop.xpath(u'div[1]/p[@class="add"]/span[2]/text()') else '-'
            item_new['locationurl'] = shop.xpath(u'div[1]/p[@class="add"]/a/@href').extract_first() \
                if shop.xpath(u'div[1]/p[@class="add"]/a/@href') else '-'
            ####promotion
            item_new['promotion'] = shop.xpath(u'div[1]/p[@class="promote"]/a/text()').extract_first() \
                if shop.xpath(u'div[1]/p[@class="promote"]/a/text()') else '-'
            item_new['promotionurl'] = shop.xpath(u'div[1]/p[@class="promote"]/a/@href').extract_first() \
                if shop.xpath(u'div[1]/p[@class="promote"]/a/@href') else '-'
            #price
            item_new['price'] = shop.xpath(u'div[2]/div/div/h3/a/em/text()').extract_first().replace(u'万','') \
                if shop.xpath(u'div[2]/div/div/h3/a/em/text()') else '-'
            try:
                city_and_disrtict = shop.xpath(u'div[2]/div/div/p[@class="add"]/text()').extract_first().split(" ")
            except Exception as e:
                print(e)
                item_new['price_city'] = "-"
                item_new['price_district'] = "-"
            if len(city_and_disrtict) == 1:
                item_new['price_city'] = city_and_disrtict[0]
                item_new['price_district'] = "-"
            elif len(city_and_disrtict) == 2:
                item_new['price_city'] = city_and_disrtict[0]
                item_new['price_district'] = city_and_disrtict[1]
            # item_new['price_city'] = shop.xpath(u'div[2]/div/div/p[@class="add"]/text()').extract_first().split(" ") \
            #     if shop.xpath(u'div[2]/div/div/p/text()') else '-'
            # item_new['price_district'] = shop.xpath(u'div[2]/div/div/p[@class="add"]/text()').extract_first().split(" ") \
            #     if shop.xpath(u'div[2]/div/div/p/text()') else '-'
            ####normal infor
            item_new['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item_new['website'] = website
            item_new['status'] = item_new['url']+'-'+item_new['shopid']+'-'+item['modelid']+'-'+time.strftime('%Y-%m', time.localtime())+'-' +item_new['price']
            item_new=dict(item_new,**item)
            print(item_new)
            yield item_new
        pagenext=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if pagenext:
            url=response.urljoin(pagenext)
            yield scrapy.Request(url,
                                 meta={'familydata': response.meta['familydata'],
                                       'type': response.meta['type']},
                                 callback=self.parse_price)