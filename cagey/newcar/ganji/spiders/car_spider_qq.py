# -*- coding: utf-8 -*-
import scrapy
from ganji.items import QQItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import json
import re

website ='qq'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://data.auto.qq.com/car_brand/index.shtml"
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
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        # list value
        jsonlist = response.xpath('//script[contains(text(),"oBrandSerialData")]/text()').re('oBrandSerialData = ([\s\S]*?)\r\n\r\n/*')[0] \
            if response.xpath('//script[contains(text(),"oBrandSerialData")]/text()').re('oBrandSerialData = ([\s\S]*?)\r\n\r\n/*') else '-'
        if jsonlist !='-':
            jsonlist=jsonlist.replace('{', '{"').replace(':', '":').replace(',', ',"').replace(',"{', ',{').replace('http":','http:')
            jsonlist=json.loads(jsonlist)
            for jl in jsonlist['list']:
                for BL in jl[' BrandList']:
                    for mL  in BL['manList']:
                        for sL in mL['serialList']:
                            brandid=BL['brandID']
                            brandname=BL['brandName']
                            factoryid=mL['manID']
                            factoryname=mL['manName']
                            familyname=sL['serialName']
                            familyid=sL['serialID']
                            level = sL['serialLever']
                            url='http://data.auto.qq.com/car_serial/'+str(familyid)+'/modelscompare.shtml'
                            metadata={'brandid':brandid,'brandname':brandname,
                                      'factoryid':factoryid,'factoryname':factoryname,
                                      'familyid': familyid, 'familyname': familyname,'level':level}
                            yield scrapy.Request(url, meta={'metadata': metadata}, callback=self.parse_car)

    # get car infor
    def parse_car(self, response):
        # item loader
        item = QQItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['datasave'] = response.xpath('//html').extract_first()
        #brandname factoryname familyname brandid familyid
        metadata =response.meta['metadata']
        if metadata:
            item['brandname']=metadata['brandname']
            item['brandid'] = metadata['brandid']
            item['factoryname'] = metadata['factoryname']
            item['factoryid']=metadata['factoryid']
            item['familyname'] = metadata['familyname']
            item['familyid'] = metadata['familyid']
        #carlist
        try:
            next=response.meta['page']
            item['url'] = response.url
            item['status'] = response.url
            item['carid'] = re.findall('\d+',response.url)[0] if re.findall('\d+',response.url) else '-'
            item['salesdesc'] = response.xpath('//h1[@class="MTitle_d"]/span/text()').extract_first() \
                if response.xpath('//h1[@class="MTitle_d"]/span/text()') else '-'
            infors=dict()
            for carinfos in response.xpath('//div[@class="MTable_b"]/table/tbody/tr'):
                if carinfos.xpath('td[1]/text()'):
                    name1 =carinfos.xpath('td[1]/text()').extract_first()
                if carinfos.xpath('td[2]/text()'):
                    infor1=carinfos.xpath('td[2]/text()').extract_first()
                    carinfor1={name1:infor1}
                    infors=dict(infors,**carinfor1)
                if carinfos.xpath('td[4]/text()'):
                    name2 =carinfos.xpath('td[4]/text()').extract_first()
                if carinfos.xpath('td[5]/text()'):
                    infor2=carinfos.xpath('td[5]/text()').extract_first()
                    carinfor2={name2:infor2}
                    infors=dict(infors,**carinfor2)
            item['jsonsave'] = infors
            yield item
        except:
            carlist=[]
            for model in response.xpath('//li[contains(@id,"model_name")]'):
                m=dict()
                carid=model.xpath('a/@href').re('\d+')[0] if model.xpath('a/@href').re('\d+') else '-'
                modelurl='http://data.auto.qq.com'+model.xpath('a/@href').extract_first() if model.xpath('a/@href') else '-'
                salesdesc=model.xpath('a/text()').extract_first() if model.xpath('a/text()') else '-'
                m={'carid':carid,'modelurl':modelurl,'salesdesc':salesdesc}
                carlist.append(m)
            namelist=[]
            for name in response.xpath('//ul[@id="config_name"]/li[not(@class="bar")]'):
                if name.xpath('text()'):
                    nametext=name.xpath('text()').extract_first()
                    namelist.append(nametext)
                elif name.xpath('a/text()'):
                    nametext = name.xpath('a/text()').extract_first()
                    namelist.append(nametext)
            i=0
            for car in response.xpath('//li[contains(@class,"car")]'):
                j=0
                if i>=len(carlist):
                    break
                m = carlist[i]
                for carinfo in car.xpath('ul/li[not(@class="bar")]/text()'):
                    if j>=len(namelist):
                        break
                    info=carinfo.extract()
                    name =namelist[j]
                    info_dict={name:info}
                    m=dict(m,**info_dict)
                    j+=1
                carlist[i]=m
                i+=1
            for car in carlist:
                itemnew=QQItem()
                itemnew['url']=car['modelurl']
                itemnew['status']=itemnew['url']
                itemnew['carid'] = car['carid']
                itemnew['salesdesc'] = car['salesdesc']
                car.pop('modelurl')
                car.pop('carid')
                car.pop('salesdesc')
                itemnew['jsonsave']=car
                itemnew=dict(itemnew,**item)
                yield itemnew
            for modelnext in response.xpath('//div[@id="models_TCountList"]/div[@class="subItemList"]/div/a/@href'):
                model=modelnext.extract()
                url=response.urljoin(model)
                yield scrapy.Request(url, meta={'metadata': metadata,'page':'next'}, callback=self.parse_car)



