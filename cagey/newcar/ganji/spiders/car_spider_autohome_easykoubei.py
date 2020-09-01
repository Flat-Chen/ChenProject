# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomeItem_easykoubei
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random

website ='autohome_easykoubei'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 100000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        #family list
        self.familylist=['2767','3267','465','89','90','91','601','2202','543','542','544','566','487','227',
                         '342','2207','380','222','291','23','4072','3872','504','121','3062','521','777','263','503','3048']

    # get family list
    def start_requests(self):
        lists=[]
        url= 'http://k.autohome.com.cn/p1/'
        list = scrapy.Request(url, headers={'Referer': 'http://k.autohome.com.cn/'},callback=self.parse, errback=self.error_parse)

        lists.append(list)
        return lists

    # get family list
    def error_parse(self, response):
        logging.log(msg="Error", level=logging.INFO)

    # get family list
    def parse(self, response):
        for typepath in response.xpath('//div[@class="findcont-choose"]/a'):
            familydata = dict()
            familydata['type'] = typepath.xpath('text()').extract_first() \
                if typepath.xpath('text()') else '-'
            familydata['typeid'] = typepath.xpath('@href').re('/([\s\S]*?)/')[0] \
                if typepath.xpath('/@href').re('/([\s\S]*?)/') else '-'
            urlbase = typepath.xpath('@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,
                                 meta={'familydata': familydata},
                                 callback=self.parse_family)
    #get family list
    def parse_family(self, response):
        for familypath in response.xpath('//ul[@class="list-cont"]/li'):
            familydata=dict()
            familydata['familyname'] = familypath.xpath('div[@class="cont-name"]/a/text()').extract_first() \
                if familypath.xpath('div[@class="cont-name"]/a/text()') else '-'
            familydata['familyid'] =familypath.xpath('div[@class="cont-name"]/a/@href').re('\d+')[0] \
                if familypath.xpath('div[@class="cont-name"]/a/@href').re('\d+') else '-'
            if familydata['familyid'] not in self.familylist:
                continue
            familydata['familycount'] = familypath.xpath('div[@class="c999 cont-text"]/a/text()').extract_first() \
                if familypath.xpath('div[@class="c999 cont-text"]/a/text()') else '-'
            familydata['familyscore'] = familypath.xpath('div/a/span[@class="red"]/text()').extract_first() \
                if familypath.xpath('div/a/span[@class="red"]/text()') else '-'
            familydata=dict(familydata,**response.meta['familydata'])
            urlbaselist=[familypath.xpath('div[@class="cont-name"]/a/@href').extract_first()+'?onlyAppending=True',
                         familypath.xpath('div[@class="cont-name"]/a/@href').extract_first()+'stopselling/?onlyAppending=True',]
            for urlbase in urlbaselist:
                url=response.urljoin(urlbase)
                yield scrapy.Request(url,
                                     meta={'familydata':familydata},
                                     callback=self.parse_koubeipath)

    # get family list
    def parse_koubeipath(self, response):
        for koubeipath in response.xpath('//div[@class="cont-title fn-clear"]/div/b/a/@href'):
                url=koubeipath.extract().split("?")[0] if koubeipath.extract().split("?") else 'http://k.autohome.com.cn/'
                yield scrapy.Request(url,
                                     meta={'familydata': response.meta['familydata']},
                                     callback=self.parse_koubei)

        pagenext = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if not (pagenext == "###"):
            url = response.urljoin(pagenext)
            yield scrapy.Request(url,
                                 meta={'familydata': response.meta['familydata']},
                                 callback=self.parse_koubeipath)
    # get car infor
    def parse_koubei(self, response):
        item = AutohomeItem_easykoubei()
        ####normal infor
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['url'] = response.url
        item['status'] = item['url']
        item['datasave'] = response.xpath('//html').extract_first()
        #### familydata
        item['familyname'] = response.meta['familydata']['familyname']
        item['familyid'] = response.meta['familydata']['familyid']
        item['familycount'] = response.meta['familydata']['familycount']
        item['familyscore'] = response.meta['familydata']['familyscore']
        item['type'] = response.meta['familydata']['type']
        item['typeid'] = response.meta['familydata']['typeid']
        #car infor
        mount = response.xpath('//div[@class="mouth-cont"]')
        item['carid'] = mount.xpath(
            u'div/div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/@href').re(
            '\d+')[0] \
            if mount.xpath(
            u'div/div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/@href').re(
            '\d+') else '-'
        item['salesdesc'] = mount.xpath(
            u'div/div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/text()').extract_first() \
            if mount.xpath(
            u'div/div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/text()') else '-'
        #userinfor
        item['user_name'] = response.xpath('//a[@id="ahref_UserId"]/text()').extract_first() \
            if response.xpath('//input[@id="ahref_UserId"]/text()') else '-'
        item['userid'] = response.xpath('//input[@id="hidAuthorId"]/@value').extract_first() \
                                if response.xpath('//input[@id="hidAuthorId"]/@value') else '-'
        item['EvalId'] = response.xpath('//input[@id="hidEvalId"]/@value').extract_first() \
            if response.xpath('//input[@id="hidEvalId"]/@value') else '-'
        item['EvalCreated'] = response.xpath('//input[@id="hidEvalCreated"]/@value').extract_first() \
            if response.xpath('//input[@id="hidEvalCreated"]/@value') else '-'
        item['LastAppendId'] = response.xpath('//input[@id="hidLastAppendId"]/@value').extract_first() \
            if response.xpath('//input[@id="hidLastAppendId"]/@value') else '-'
        item['LastAppendCreated'] = response.xpath('//input[@id="hidLastAppendCreated"]/@value').extract_first() \
            if response.xpath('//input[@id="hidLastAppendCreated"]/@value') else '-'
        ###repaire info
        addinfor = "".join(response.xpath('//dd[@class="add-dl-text"]/text()').extract()) + u'【'
        addinfor = addinfor.strip().replace(" ", "")
        item['maitenance'] = "-".join(re.findall(u'(【保养[\s\S]*?)【', addinfor)).strip()
        item['fault'] = "-".join(re.findall(u'(【故障[\s\S]*?)【', addinfor)).strip()
        item['complain'] = "-".join(re.findall(u'(【吐槽[\s\S]*?)【', addinfor)).strip()
        yield item