# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomeItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random

website ='autohome'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]

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
    def start_requests(self):
        cars = []
        for i in range(1, self.carnum):
            url = 'http://car.autohome.com.cn/config/spec/' + str(i) + '.html'
            car = scrapy.Request(url,
                              callback=self.parse)
            cars.append(car)
        return cars


    # get car infor
    def parse(self, response):
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        # item loader
        item = AutohomeItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()
        # familyname
        navi = response.xpath('//div[@class="path"]')
        item['familyname'] = navi.xpath('a[3]/text()').extract_first() \
            if navi.xpath('a[3]/text()') else '-'
        item['familyid'] = navi.xpath('a[3]/@href').re('\d+')[0] \
            if navi.xpath('a[3]/@href') else '-'
        # list value
        jsonlist = json.loads(response.xpath('//script[contains(text(),"config")]/text()').re('config = (.*?);')[0]) \
                if response.xpath('//script[contains(text(),"config")]/text()').re('config = (.*?);') else '-'
        if jsonlist!='-':
            results=jsonlist['result']
            item['jsonsave'] = results
            item['carid']=results['specid']
            namelist=['salesdesc','price','factoryname','type','motor','gear','lengthwh','body','maxspeed',
                      'accelerate','actualaccelerate','actualstop','actualpetrol','petrol','actual_liftoff_distance',
                      'warranty','length','width','height','wheel','frontwheel','backwheel','liftoff_distance',
                      'weight','body','doors','seats','fuelvolumn','baggage','motortype','cylinder','output','method',
                      'lwv','lwvnumber','valve','compress','valve_gear','cylinder_diameter','cylinder_travel','maxps',
                      'maxpower','maxrpm','maxnm','maxtorque','motortechnique','fuletype','fulevolumn','fulemethod',
                      'cylinder_head_material','cylinder_body_material','emission','geardesc','gearnumber','geartype',
                      'driveway','frontgauge','backgauge','assistanttype','body_structure','frontbrake','backbrake',
                      'parking_brake_type','frontwheel','backwheel','sparewheel',]
            id=0
            for i in results['paramtypeitems']:
                for j in i['paramitems']:
                    k = j['valueitems'][0]['value']
                    if j['name']==u"四驱形式" or j['name']==u"中央差速器结构" :
                        continue
                    elif id <66:
                        name=namelist[id]
                        item[name]=k
                        id+=1
        yield item