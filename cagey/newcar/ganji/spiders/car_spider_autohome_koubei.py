# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomeItem_koubei
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json

website ='autohome_koubei'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls=['http://k.autohome.com.cn/suva01/', ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 5000000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

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
            yield scrapy.Request(url,meta={'familydata': familydata},callback=self.parse_family)
    #get family list
    def parse_family(self, response):
        for familypath in response.xpath('//ul[@class="list-cont"]/li'):
            familydata=dict()
            familydata['familyname'] = familypath.xpath('div[@class="cont-name"]/a/text()').extract_first() \
                if familypath.xpath('div[@class="cont-name"]/a/text()') else '-'
            familydata['familyid'] = familypath.xpath('div[@class="cont-name"]/a/@href').re('\d+')[0] \
                if familypath.xpath('div[@class="cont-name"]/a/@href').re('\d+') else '-'
            familydata['familycount'] = familypath.xpath('div[@class="c999 cont-text"]/a/text()').extract_first() \
                if familypath.xpath('div[@class="c999 cont-text"]/a/text()') else '-'
            familydata['familyscore'] = familypath.xpath('div/a/span[@class="red"]/text()').extract_first() \
                if familypath.xpath('div/a/span[@class="red"]/text()') else '-'
            familydata=dict(familydata,**response.meta['familydata'])
            urlbaselist=[familypath.xpath('div[@class="cont-name"]/a/@href').extract_first(),
                         familypath.xpath('div[@class="cont-name"]/a/@href').extract_first()+'stopselling/',]
            for urlbase in urlbaselist:
                url=response.urljoin(urlbase)
                yield scrapy.Request(url,meta={'familydata':familydata},callback=self.parse_koubei)

    # get car infor
    def parse_koubei(self, response):
        itembase = AutohomeItem_koubei()
        ####normal infor
        itembase['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        itembase['website'] = website
        #### familydata
        itembase['familyname'] = response.meta['familydata']['familyname']
        itembase['familyid'] = response.meta['familydata']['familyid']
        itembase['familycount'] = response.meta['familydata']['familycount']
        itembase['familyscore'] = response.meta['familydata']['familyscore']
        itembase['type'] = response.meta['familydata']['type']
        itembase['typeid'] = response.meta['familydata']['typeid']

        for mount in response.xpath('//div[@class="mouthcon"]'):
            item=AutohomeItem_koubei()
            item['carid'] = mount.xpath(u'div/div[@class="mouthcon-cont-left"]/div[@class="choose-con mt-10"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/@href').re('\d+')[0] \
                if mount.xpath(u'div/div[@class="mouthcon-cont-left"]/div[@class="choose-con mt-10"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/@href').re('\d+') else '-'
            item['salesdesc'] =  mount.xpath(u'div/div[@class="mouthcon-cont-left"]/div[@class="choose-con mt-10"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/span/text()').extract_first() \
                if mount.xpath(u'div/div[@class="mouthcon-cont-left"]/div[@class="choose-con mt-10"]/dl/dt[contains(text(),"车型")]/../dd/a[2]/span/text()') else '-'
            item['user_name'] = mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a[1]/text()').extract_first().strip() \
                if mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a[1]/text()') else '-'
            item['userid'] = mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a[1]/@href').re('\d+')[0] \
                if mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a[1]/@href').re('\d+') else '-'
            userlevel = mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a[1]/i/@class').extract_first() \
                if mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a[1]/i/@class') else '-'
            usercfcar = mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[3]/div[@class="name-text"]/text()').extract_first() \
                if mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[3]/div[@class="name-text"]/text()') else '-'
            usercfcarid = mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[3]/div[@class="name-text"]/a/@href').extract_first() \
                if mount.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con"]/div/div[3]/div[@class="name-text"]/a/@href') else '-'

            url = scrapy.Field()
            status = scrapy.Field()
            post_date = scrapy.Field()
            grabtime = scrapy.Field()
            contentid = scrapy.Field()
            koubeilevel = scrapy.Field()
            ext_dealer = scrapy.Field()
            ext_dealerid = scrapy.Field()
            ext_fuel = scrapy.Field()
            ext_nake_price = scrapy.Field()
            ext_purchase_date = scrapy.Field()
            ext_purchase_place = scrapy.Field()
            ext_purpose = scrapy.Field()
            ext_run = scrapy.Field()
            mouth_content = scrapy.Field()
            mouth_reply_count = scrapy.Field()
            mouth_support_count = scrapy.Field()
            mouth_view_count = scrapy.Field()
            mouth_space = scrapy.Field()
            mouth_power = scrapy.Field()
            mouth_control = scrapy.Field()
            mouth_fuel = scrapy.Field()
            mouth_comfort = scrapy.Field()
            mouth_appearance = scrapy.Field()
            mouth_trim = scrapy.Field()
            mouth_cost_efficient = scrapy.Field()
            score_space = scrapy.Field()
            score_power = scrapy.Field()
            score_control = scrapy.Field()
            score_fuel = scrapy.Field()
            score_comfort = scrapy.Field()
            score_appearance = scrapy.Field()
            score_trim = scrapy.Field()
            score_cost_efficient = scrapy.Field()
            #brand
            item['brandname'] = response.meta['branddata']['brandname']
            item['brandid'] = response.meta['branddata']['brandid']
            #factory
            item['factoryname'] = response.meta['factorydata']['factoryname']
            item['factoryid'] = response.meta['factorydata']['factoryid']
            ####key info
            # item['shopname'] =shop.xpath('ul/li[@class="tit-row"]/a/span/text()').extract_first() \
            #     if shop.xpath('ul/li[@class="tit-row"]/a/span/text()') else '-'
            # item['url']=shop.xpath('ul/li[@class="tit-row"]/a/@href').extract_first() \
            #     if shop.xpath('ul/li[@class="tit-row"]/a/@href') else '-'
            # if shop.xpath('ul/li[@class="tit-row"]/span[@class="green"]'):
            #     item['shoptype'] = shop.xpath('ul/li[@class="tit-row"]/span[@class="green"]/text()').extract_first() \
            #         if shop.xpath('ul/li[@class="tit-row"]/span[@class="green"]/text()') else '-'
            #     item['shopcolor'] = 'green'
            # elif shop.xpath('ul/li[@class="tit-row"]/span[@class="blue"]'):
            #     item['shoptype'] = shop.xpath('ul/li[@class="tit-row"]/span[@class="blue"]/text()').extract_first() \
            #         if shop.xpath('ul/li[@class="tit-row"]/span[@class="blue"]/text()') else '-'
            #     item['shopcolor'] = 'blue'
            # item['shopstar'] = str(int(shop.xpath('ul/li[@class="tit-row"]/span[@class="icon star"]/i/@style').re('\d+')[0])*5/100) \
            #     if shop.xpath('ul/li[@class="tit-row"]/span[@class="icon star"]/i/@style').re('\d+') else '-'
            # ####salemodel and saleprice
            # item['modelnumber']=str(shop.xpath('ul/li[2]/a/text()').re('\d+')[0]) \
            #     if shop.xpath('ul/li[2]/a/text()').re('\d+') else '-'
            # item['mainbrands'] = '-'.join(shop.xpath('ul/li[2]/em/text()').extract()) \
            #     if shop.xpath('ul/li[2]/em/text()') else '-'
            # item['tel'] = shop.xpath('ul/li[3]/span[@class="tel"]/text()').extract_first() \
            #     if shop.xpath('ul/li[3]/span[@class="tel"]/text()') else '-'
            # item['saleregion'] = shop.xpath('ul/li[3]/span[@class="sale-whole"]/span/text()').extract_first() \
            #     if shop.xpath('ul/li[3]/span[@class="sale-whole"]/span/text()') else '-'
            # item['priceurl']=shop.xpath('ul/li[2]/a/@href').extract_first() \
            #     if shop.xpath('ul/li[2]/a/@href') else '-'
            # ####location
            # item['location']=shop.xpath('ul/li[4]/span/text()').extract_first().replace(u'址：','') \
            #     if shop.xpath('ul/li[4]/span/text()') else '-'
            # item['locationurl'] = shop.xpath('ul/li[4]/a/@href').extract_first() \
            #     if shop.xpath('ul/li[4]/a/@href') else '-'
            # ####promotion
            # item['promotion'] = shop.xpath('ul/li[5]/a/text()').extract_first() \
            #     if shop.xpath('ul/li[5]/a/text()') else '-'
            # item['promotionurl'] = shop.xpath('ul/li[5]/a/@href').extract_first() \
            #     if shop.xpath('ul/li[5]/a/text()') else '-'
            # ####img
            # item['imageurl'] = shop.xpath('a/img/@src').extract_first() \
            #     if shop.xpath('a/img/@src') else '-'
            ###normal info
            item['status'] = item['url']
            yield item
        pagenext=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if not(pagenext=='javascript:void(0)'):
            url=response.urljoin(pagenext)
            yield scrapy.Request(url,
                                 meta={'citydata': response.meta['citydata'], 'branddata': response.meta['branddata'],
                                       'factorydata': response.meta['factorydata']},
                                 callback=self.parse_koubei)
        kindnext=response.xpath('//div[@class="tab"]/a[@class="nav"]/@href').extract_first()
        if kindnext:
            if not(kindnext.find('kindId=2')==-1):
                url = response.urljoin(kindnext)
                yield scrapy.Request(url,
                                     meta={'citydata': response.meta['citydata'], 'branddata': response.meta['branddata'],
                                           'factorydata': response.meta['factorydata']},
                                     callback=self.parse_koubei)