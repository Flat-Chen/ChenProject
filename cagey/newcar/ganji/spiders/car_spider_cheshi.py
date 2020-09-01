# -*- coding: utf-8 -*-
import scrapy
from ganji.items import cheshiItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import json
import re
import logging

website ='cheshi_new'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["cheshi.com"]


    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 100000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #start request
    def start_requests(self):
        carlist=[]
        for i in range(65,91):
            tag=chr(i)
            url='http://product.cheshi.com/static/selectcar/'+tag+'.html'
            car=scrapy.Request(url)
            carlist.append(car)
        return carlist

    # family select
    def parse(self, response):
            for brandhref in response.xpath('//div[@class="list_nr"]'):
                brandname = brandhref.xpath('div[@class="list_left"]/a/span/text()').extract_first()
                brandid = 'logo_' + str(brandhref.xpath('div[@class="list_left"]/a/@href').re('\d+')[0]) \
                    if brandhref.xpath('div[@class="list_left"]/a/@href') else '-'

                for factoryhref in brandhref.xpath('div[@class="list_right"]/dl'):
                    factoryname = factoryhref.xpath('dt/a/text()').extract_first()
                    factoryid = 'brand_' + str(factoryhref.xpath('dt/a/@href').re('\d+')[0]) \
                        if factoryhref.xpath('dt/a/@href').re('\d+') else ''

                    for familyhref in factoryhref.xpath('dd/div/h4/a'):
                        familyname = familyhref.xpath('@title').extract_first()
                        familyid = str(familyhref.xpath('@href').re('\d+')[0]) \
                            if familyhref.xpath('@href').re('\d+') else ''
                        href = familyhref.xpath('@href').extract_first()
                        metadata = {"brandname": brandname, "brandid": brandid,
                                    "factoryname": factoryname, "factoryid": factoryid,
                                    "familyname": familyname, "familyid": familyid, }
                        yield scrapy.Request(href, meta={"metadata": metadata}, callback=self.year_parse)
    #series year
    def year_parse(self, response):
        for yearlist in response.xpath('//li[@class="navli02"]/a'):
            urlbase=yearlist.xpath('@href').extract_first()
            makeyear=yearlist.xpath('text()').re('\d+')[0] if yearlist.xpath('text()').re('\d+')  else '-'
            url=response.urljoin(urlbase)
            metadata=response.meta['metadata']
            metadata['makeyear']=makeyear
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.modellist_parse)
        for yearlist in response.xpath('//ul[@class="stoplist"]/li/a'):
            urlbase=yearlist.xpath('@href').extract_first()
            makeyear=yearlist.xpath('text()').re('\d+')[0] if yearlist.xpath('text()').re('\d+')  else '-'
            url=response.urljoin(urlbase)
            metadata=response.meta['metadata']
            metadata['makeyear']=makeyear
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.modellist_parse)

    # model list
    def modellist_parse(self, response):
        urlbase =response.xpath('//a[@class="describe"]/@href').extract_first() if response.xpath('//a[@class="describe"]/@href') else '-'
        urlbase =urlbase + 'param.html'
        url = response.urljoin(urlbase)
        metadata = response.meta['metadata']
        yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_car)

    # get car infor
    def parse_car(self, response):
        # item loader
        item = cheshiItem()
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
            item['makeyear'] = metadata['makeyear']
        #carlist
        if response.xpath('//dl[@class="tb_tit"]/dd'):
            cars=[]
            for keyinfo in response.xpath('//dl[@class="tb_tit"]/dd'):
                car =dict()
                car['url'] = keyinfo.xpath('div[2]/label/p/a/@href').extract_first() \
                    if keyinfo.xpath('div[2]/label/p/a/@href') else '-'
                car['status'] = car['url']
                car['carid'] = 'model_'+keyinfo.xpath('div[2]/label/p/a/@href').re('\d+')[0] \
                    if keyinfo.xpath('div[2]/label/p/a/@href').re('\d+') else '-'
                car['salesdesc'] = keyinfo.xpath('div[2]/label/p/a/text()').extract_first() \
                    if keyinfo.xpath('div[2]/label/p/a/text()') else '-'
                car['price'] = '.'.join(keyinfo.xpath('div[2]/label/span/label/text()').re('\d+')) \
                    if keyinfo.xpath('div[2]/label/span/label/text()').re('\d+') else '-'
                cars.append(car)
            infors=[]
            for carinfo in response.xpath('//div[@id="param_content"]/dl[not(@name="divposition")]'):
                if carinfo.xpath('dt/a/text()'):
                    name =carinfo.xpath('dt/a/text()').extract_first().replace('.','')
                elif carinfo.xpath('dt/text()'):
                    name =carinfo.xpath('dt/text()').extract_first().replace(u'\uff1a','').replace('.','')
                else:
                    continue
                i =0
                for carinfodetail in carinfo.xpath('dd'):
                    if i >len(cars):
                        break
                    info=carinfodetail.xpath('text()').extract_first() if carinfodetail.xpath('text()') else '-'
                    infodict ={name:info}
                    if i>=len(infors):
                        infors.append(infodict)
                    else:
                        infors[i] = dict(infors[i], **infodict)
                    i=i+1
            i=0
            for car in cars:
                # count
                self.counts += 1
                logging.log(msg="download              " + str(self.counts) + "                  items",level=logging.INFO)
                itemnew=cheshiItem()
                itemnew=dict(item,**car)
                if len(infors)>i:
                    info =infors[i]
                    itemnew['jsonsave']=info
                i =i + 1
                yield itemnew