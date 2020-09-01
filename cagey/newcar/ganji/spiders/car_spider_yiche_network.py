# -*- coding: utf-8 -*-
import scrapy
from ganji.items import yicheItem_network
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re

website ='yiche_network'

class CarSpider(scrapy.Spider):

    name = website
   # allowed_domains = ["bitauto.com"]
    start_urls=['http://api.admin.bitauto.com/city/getcity.ashx?callback=City_Select._$JSON_callback.$JSON&requesttype=json&bizCity=1',]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 100000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'network', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #get region list
    def parse(self, response):
        # list value
        jsonlist = eval(response.xpath('//p/text()').re('JSON\(([\s\S]*?)\);')[0]) \
            if response.xpath('//p/text()').extract_first() else '-'
        print jsonlist

        for region in jsonlist:
            citydata = dict()
            citydata['cityId'] = region['cityId']
            citydata['regionId'] = region['regionId']
            citydata['cityName'] = region['cityName']
            citydata['regionName'] = region['regionName']
            citydata['cityPinYin'] = region['cityPinYin']
            citydata['parentId'] = region['parentId']
            citydata['shortName'] = region['shortName']
            citydata['cityLevel'] = region['cityLevel']
            citydata['navCityId'] = region['navCityId']
            citydata['centerCityId'] = region['centerCityId']
            url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&citycode=' \
                  + citydata['cityPinYin'] + '&cityid=' + citydata['cityId']
            yield scrapy.Request(url,
                                 meta={'citydata': citydata},
                                 callback=self.parse_brand)

            # # list value
        # # x=response.xpath('//p/text()').extract_first()
        # print response.url
        # print response.xpath('//p/text()').extract_first()
        # print response.xpath('//p/text()').re('City_Select\._$JSON_callback\.$JSON\((.*)\)')[0]
        # jsonlist=response.xpath('//p/text()').re('City_Select\._$JSON_callback\.$JSON\((.*)\)')[0]  \
        #     if response.xpath('//p/text()').re('City_Select\._$JSON_callback\.$JSON\((.*)\)') else "-"
        # logging.log(msg=jsonlist,level=logging.INFO)
        # # jsonlist=re.findall('City_Select._.\((.*)\)',x)[0]
        # jsondata=json.loads(jsonlist)
        #         # if response.xpath('//p/text()').extract_first() else '-'
        #
        # for region in jsondata:
        #     citydata=dict()
        #     citydata['cityId'] = region['cityId']
        #     citydata['regionId'] = region['regionId']
        #     citydata['cityName'] = region['cityName']
        #     citydata['regionName'] = region['regionName']
        #     citydata['cityPinYin'] = region['cityPinYin']
        #     citydata['parentId'] = region['parentId']
        #     citydata['shortName'] = region['shortName']
        #     citydata['cityLevel'] = region['cityLevel']
        #     citydata['navCityId'] = region['navCityId']
        #     citydata['centerCityId'] = region['centerCityId']
        #     url='http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&citycode='\
        #         +citydata['cityPinYin'] +'&cityid='+citydata['cityId']
        #     yield scrapy.Request(url,
        #                          meta={'citydata':citydata},
        #                          callback=self.parse_brand)

    # get factory
    def parse_brand(self, response):
        jsonbrand = response.xpath('//p/text()').re('JsonpCallBack\(([\s\S]*?)\)')[0]
        jsonbrand = jsonbrand.replace('{', '{"').replace('SP:01','SP01').replace(':', '":').replace(',', ',"').replace(',"{',',{').replace('http":', 'http:')
        jsonbrand = json.loads(jsonbrand)
        charkeys = jsonbrand['brand'].keys()
        citydata=response.meta['citydata']
        for charkey in charkeys:
            for brand in jsonbrand['brand'][charkey]:
                brandname = brand['name']
                brandid = brand['id']
                brandurl = brand['url']
                brandnum=brand['num']
                urlbase ='http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&objid='\
                        +str(brandid)+'&citycode='+citydata['cityPinYin'] +'&cityid='+citydata['cityId']
                factorydata = {'brandname': brandname, 'brandid': brandid, 'brandurl': brandurl,'brandnum':brandnum}
                yield scrapy.Request(urlbase,meta={'citydata': response.meta['citydata'],
                                                           'factorydata': factorydata},
                                                     callback=self.parse_factory)

    #get factory
    def parse_factory(self, response):
        jsonbrand = response.xpath('//text()').re('JsonpCallBack\(([\s\S]*?}]})\)')[0]
        jsonbrand=jsonbrand.replace('{', '{"').replace('SP:01', 'SP01').replace(':', '":').replace(',', ',"').replace(',"{', ',{').replace('http":','http:')
        jsonbrand=json.loads(jsonbrand)
        charkeys=jsonbrand['brand'].keys()
        brandid_key=response.meta['factorydata']['brandid']
        citypingying=response.meta['citydata']['cityPinYin']
        for charkey in charkeys:
            for brand in jsonbrand['brand'][charkey]:
                brandid =brand['id']
                if brandid_key==brandid:
                    for factory in brand['child']:
                        factoryname=factory['name']
                        factorynum=factory['num']
                        factoryurl = re.findall(citypingying+'([\s\S]*?)/',factory['url'])[0]  \
                            if re.findall(citypingying+'([\s\S]*?)/',factory['url']) else factory['url']
                        factorydata={'factoryname':factoryname,'factorynum':factorynum,'factoryurl':factoryurl}
                        factorydata =dict(factorydata,**response.meta['factorydata'])
                        for i in [1,2,3]:
                            urlbase = 'http://dealer.bitauto.com/'+citypingying+'/'+factoryurl+'/?BizModes='+str(i)
                            yield scrapy.Request(urlbase,
                                             meta={'citydata':response.meta['citydata'],'factorydata':factorydata,'type':str(i)},
                                             callback=self.parse_network)

    # get car infor
    def parse_network(self, response):
        item=yicheItem_network()
        ####metadata:
        #city
        item['cityId'] = response.meta['citydata']['cityId']
        item['regionId'] = response.meta['citydata']['regionId']
        item['cityName'] = response.meta['citydata']['cityName']
        item['regionName'] = response.meta['citydata']['regionName']
        item['cityPinYin'] = response.meta['citydata']['cityPinYin']
        item['parentId'] = response.meta['citydata']['parentId']
        item['shortName'] = response.meta['citydata']['shortName']
        item['cityLevel'] = response.meta['citydata']['cityLevel']
        item['navCityId'] = response.meta['citydata']['navCityId']
        item['centerCityId'] = response.meta['citydata']['centerCityId']
        #brand
        item['brandname'] = response.meta['factorydata']['brandname']
        item['brandid'] = response.meta['factorydata']['brandid']
        item['brandurl'] = response.meta['factorydata']['brandurl']
        item['brandnum'] = response.meta['factorydata']['brandnum']
        item['factoryname'] = response.meta['factorydata']['factoryname']
        item['factorynum'] = response.meta['factorydata']['factorynum']
        item['factoryurl'] = response.meta['factorydata']['factoryurl']
        #key
        item['type'] = response.meta['type']
        ####key info
        for shop in response.xpath('//li[@class="clearfix"]'):
            item_new = yicheItem_network()
            item_new['shopid'] = shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/input/@value').extract_first() \
                if shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/input/@value') else '-'
            item_new['shopname'] =shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/text()').extract_first() \
                if shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/text()') else '-'
            item_new['url']=shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/@href').extract_first() \
                if shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/@href') else '-'
            item_new['shopfullname'] = shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/@title').extract_first() \
                if shop.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/@title') else '-'

            if item['type']=='1':
                item_new['shoptype'] = u'综合店'
            elif item['type']=='2':
                item_new['shoptype'] = u'4S店'
            elif item['type']=='3':
                item_new['shoptype'] = u'特许店'
            ####salemodel and saleprice
            item_new['mainbrands'] = '-'.join(shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"品牌")]/span/text()').extract()) \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"品牌")]/span/text()') else '-'
            item_new['tel'] = shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"电话")]/span/span/text()').extract_first() \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"电话")]/span/span/text()') else '-'
            item_new['saleregion'] = shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"电话")]/span/b/small/a[@class="xiaoshou"]/text()').extract_first() \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"电话")]/span/b/small/a[@class="xiaoshou"]/text()') else '-'
            ####location
            item_new['location']=shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"地址")]/span/text()').extract_first() \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"地址")]/span/text()') else '-'
            item_new['locationurl'] = shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"地址")]/span/a/@href').extract_first() \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"地址")]/span/a/@href') else '-'
            ####promotion
            item_new['promotion'] = shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"促销")]/span/a/text()').extract_first() \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"促销")]/span/a/text()') else '-'
            item_new['promotionurl'] = shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"促销")]/span/a/@href').extract_first() \
                if shop.xpath(u'div[@class="intro-box"]/p[contains(text(),"促销")]/span/a/@href') else '-'
            ####normal infor
            item_new['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item_new['website'] = website
            item_new['status'] = item_new['url']+'-'+item['factoryurl']
            item_new=dict(item_new,**item)
            yield item_new
        pagenext=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if pagenext:
            url=response.urljoin(pagenext)
            yield scrapy.Request(url,
                                 meta={'citydata': response.meta['citydata'], 'factorydata': response.meta['factorydata'],
                                       'type': response.meta['type']},
                                 callback=self.parse_network)