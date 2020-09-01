# -*- coding: utf-8 -*-

import scrapy
from ganji.items import PcautoWeiboItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import pymongo
import urllib2
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

website = 'pcauto_weibo_f'

class CarSpider(scrapy.Spider):

    name = website

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

    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["network"]
        collection = db["pcauto_dealer"]

        start_num = 0
        end_num = 100
        shoplist = []
        for temp in collection.find().skip(start_num).limit(end_num):
            if temp['shopname']:
                shoplist.append(temp['shopname'])
                # print temp['shopname']

        for shopname in shoplist:
            print(shopname)
            url = "http://s.weibo.com/user/" + shopname + "&auth=org_vip"
            #url = "http://s.weibo.com/user/%E4%B8%8A%E6%B1%BD%E5%A4%A7%E4%BC%97&auth=org_vip"
            metadata = {"shopname": shopname}
            print url
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse)

    def parse(self, response):
        print "do parse"
        metadata = response.meta['metadata']
        url = response.url
        #print url

        # driver = webdriver.PhantomJS(r"/root/phantomjs/bin/phantomjs")
        driver = webdriver.PhantomJS(r"D:\phantomjs.exe")
        driver.get(url)  # 把url送入浏览器
        html = driver.page_source   #获取页面源码
        driver.quit()      #如果不及时关闭，后果很严重，服务器必死！！！

        units = scrapy.Selector(text=html).xpath('//div[@class="person_detail"]')
        print(units)
        for unit in units:
            username = unit.xpath('p/a[1]/@title').extract_first()
            # print username

            companynamebase = unit.xpath('p[@class="person_card"]').extract_first()
            companyname = companynamebase.replace('<p class="person_card">', "").replace('<em class="red">',"").replace('</em>',"").replace('</p>',"")
            companyname = companyname.strip()
            #print companyname.strip()

            follower = unit.xpath('p[@class="person_num"]/span[2]/a/text()').extract_first()  # 粉丝
            #print follower

            weibonum = unit.xpath('p[@class="person_num"]/span[3]/a/text()').extract_first()  # 微博
            #print weibonum

            following = unit.xpath('p[@class="person_num"]/span[1]/a/text()').extract_first()  # 关注
            #print following

            location = unit.xpath('p[@class="person_addr"]/span[2]/text()').extract_first()     #地址
            #print location

            officialweb = unit.xpath('p[@class="person_addr"]/a/@href').extract_first()     #官网
            #print officialweb

            labelbase = unit.xpath('p[@class="person_label"]/a/text()').extract()  # 标签
            flag = 0
            label = "-"
            for labeltemp in labelbase:
                if flag == 0:
                    label = labeltemp.strip()
                    flag = 1
                else:
                    label += " + " + labeltemp.strip()
            #print label

            item = PcautoWeiboItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = url
            item['website'] = website
            item['status'] = url
            item['shopname'] = metadata['shopname']
            item['username'] = username
            item['companyname'] = companyname
            item['follower'] = follower
            item['weibonum'] = weibonum
            item['following'] = following
            item['location'] = location
            item['officialweb'] = officialweb
            item['label'] = label
            yield item
