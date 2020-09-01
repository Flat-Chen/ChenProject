#-*- coding: UTF-8 -*-
import scrapy
from ganji.items import Haicjcar
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import csv
import datetime

website='haicj_car_all_p'

class CarSpider(scrapy.Spider):

    name=website

    def __init__(self,**kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=10000

        #Mongo setting
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        with open('blm/'+'newcar'+'/car_type.csv','rb') as csvfile:
            reader = csv.DictReader(csvfile)
            haicjtypelist=[row for row in reader]
        for temp in haicjtypelist:
            Num=temp['No']
            cartype=temp['car_type']
            # cartype=re.findall('\w+',temp['car_type'])[0]
            # cartype=temp['car_type'].re('\w+')[0] \
            #     if temp['car_type'].re('\w+') else "_"
            metadata={"No":Num,"Cartype":cartype}
            url='http://www.haicj.com/carinfo.jsp?clxh='+cartype+'&typeid=2'
            yield scrapy.Request(url,meta={"metadata": metadata},callback=self.parse,dont_filter=True)

    def parse(self,response):
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        metadata = response.meta['metadata']
        item=Haicjcar()
        item['No']=metadata['No']
        item['Cartype']=metadata['Cartype']
        item['url']=response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = metadata['No']+metadata['Cartype']
        # item['datasave'] = response.xpath('//html').extract_first()
        item['salesdesc']=response.xpath('//div[@class="header"]/i/text()').extract_first()
        item['price'] = response.xpath('//td[@id="zdjg"]/text()').extract_first() \
            if response.xpath('//td[@id="zdjg"]/text()').extract_first() else "-"
        yield item


