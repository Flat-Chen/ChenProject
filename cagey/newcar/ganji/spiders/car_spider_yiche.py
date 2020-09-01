# -*- coding: utf-8 -*-
import scrapy
from ganji.items import GanjiItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
from pybloom import BloomFilter


website ='yiche'
spidername ='yiche'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["bitauto.com",
                       "yiche.com"]
    start_urls = [
        "http://car.m.yiche.com/brandlist.html",
    ]

    def __init__(self,**kwargs):
        #args
        super(CarSpider, self).__init__(**kwargs)
        #carnum
        self.carnum = 200000
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        self.df = BloomFilter(capacity=self.carnum*1.1,error_rate=0.001)

    # brand select
    def parse(self, response):
        for href in response.xpath('//a[@data-action="car"]/@data-id'):
            urlbase = "http://car.bitauto.com/tree_chexing/mb_" + href.extract()
            yield scrapy.Request(urlbase, self.family_parse)

    # family select
    def family_parse(self, response):
        for href in response.xpath('//div[@class="col-xs-3"]/div/div/a/@href'):
            url = response.urljoin(href.extract()+'peizhi/')
            yield scrapy.Request(url, self.parse_car,dont_filter=True)

    #get car infor
    def parse_car(self, response):
        #more car
        if self.counts>=25000:
            for i in range(1,self.carnum):
                returndf = self.df.add(md5(str(i)).hexdigest())
                if not(returndf):
                    url ="http://car.bitauto.com/boluo/m"+str(i)+"/peizhi/"
                    yield scrapy.Request(url, self.parse_car,dont_filter=True)
        #item loader
        itembase = GanjiItem()
        # base infor
        itembase['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        itembase['website'] = website
        itembase['datasave'] = response.xpath('//html').extract_first()
        #list carinfo
        jsonlistall=eval(response.xpath('//script[contains(text(),"carCompareJson")]/text()').re('carCompareJson = (.*?);')[0]) \
            if response.xpath('//script[contains(text(),"carCompareJson")]/text()').re('carCompareJson = (.*?);') else '-'
        if jsonlistall!='-':
            for jsonlist in jsonlistall:
                # counts
                self.counts += 1
                logging.log(msg="download              " + str(self.counts) + "                  items",
                            level=logging.INFO)
                # item loader
                item = GanjiItem()
                num=0
                for i in jsonlist:
                    name= 'carinfo'+str(num)
                    if num>=17:
                        break
                    item[name]=i
                    num = num +1
                #df check
                returndf = self.df.add(md5(item['carinfo0'][0]).hexdigest())
                if not(returndf):
                    #most important
                    #brandname,factoryname,familyname,salesdesc
                    navi=response.xpath('//div[@class="car_navigate"]/div')
                    item['brandname']=navi.xpath('a[3]/text()').extract_first()\
                                    if navi.xpath('a[3]/text()') else '-'
                    item['brandid'] = navi.xpath('a[3]/@href').re('/(.*?)/')[0] \
                        if navi.xpath('a[3]/@href') else '-'
                    item['factoryname'] = navi.xpath('a[4]/text()').extract_first() \
                        if navi.xpath('a[4]/text()') else '-'
                    item['factoryid'] = navi.xpath('a[4]/@href').re('/(.*?)/')[0] \
                        if navi.xpath('a[4]/@href') else '-'
                    item['familyname'] = item['carinfo0'][4]
                    item['familyid'] = item['carinfo0'][6]
                    item['salesdesc'] = item['carinfo0'][1]
                    item['carid'] =item['carinfo0'][0]
                    #baseinfo
                    item['makeyear'] = item['carinfo0'][7]
                    item['producestatus'] = item['carinfo0'][8]
                    item['salestatus'] = item['carinfo0'][9]
                    item['type'] = item['carinfo0'][12]
                    item['price'] = item['carinfo1'][0]
                    item['output'] = item['carinfo1'][5]
                    item['geartype'] = item['carinfo1'][7]
                    item['gearnum'] = item['carinfo1'][6]
                    #body
                    item['length'] = item['carinfo2'][0]
                    item['width'] = item['carinfo2'][1]
                    item['height'] = item['carinfo2'][2]
                    item['wheel'] = item['carinfo2'][3]
                    item['weight'] = item['carinfo2'][6]
                    #motor
                    item['method'] = item['carinfo3'][4]
                    item['maxps'] = item['carinfo3'][13]
                    item['emission'] = item['carinfo3'][25]
                    item['fueltype'] = item['carinfo3'][19]
                    item['fuelnumber'] = item['carinfo3'][20]
                    item['fuelmethod'] = item['carinfo3'][21]
                    #assitanttype
                    item['assitanttype'] = item['carinfo5'][2]
                    item['backhang'] = item['carinfo5'][9]
                    item['url'] = 'http://car.bitauto.com/m'+item['carid']+'/peizhi/'
                    status = item['salestatus'] + item['producestatus']
                    item['status'] = 'm'+item['carid'] + "-" + md5(status).hexdigest()
                    #merge
                    item = dict(item,**itembase)
                    yield item
        else:
            # counts
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # item loader
            item = GanjiItem()
            item['url'] = response.url
            item['status'] = response.url+ "-" + 'none'
            self.df.add(md5(item['status']).hexdigest())
            item = dict(item, **itembase)
            yield item

        #year select
        for href in response.xpath('//div[@class="class forecast"]/a/text()').re('\d+'):
            urlbase = response.url.split('peizhi')[0] if response.url.split('peizhi') else '-'
            url = urlbase+'peizhi/'+href+'/'
            yield scrapy.Request(url, self.parse_car)

        for href in response.xpath('//dl[@id="bt_car_spcar"]/dd/a/text()').re('\d+'):
            urlbase = response.url.split('peizhi')[0] if response.url.split('peizhi') else '-'
            url = urlbase + 'peizhi/' + href + '/'
            yield scrapy.Request(url, self.parse_car)