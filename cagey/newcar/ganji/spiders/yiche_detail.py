# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:50:13 2017

@author: Zhenhuachun
"""
import scrapy
import json
import re
from ganji.items import yicheDetailItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5

# i=0
carnum = 200000
website = 'yiche_detail_change'


class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["bitauto.com"]
    start_urls = [
        "http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&pid=0&rt=master&callback=callback#"
        # "http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0"
    ]

    #
    def __init__(self,**kwargs):
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        # Mongo
        settings.set('CrawlCar_Num', carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #
    # #brand select
    # def parse(self, response):
    #     item=response.xpath("//p/text()").extract_first()
    #     brandlist = re.findall(r'\/tree_chexing/mb_\d+',item)
    #     for href in brandlist:
    #         #print href
    #         urlbase="http://car.bitauto.com" + href
    #         #print urlbase
    #         yield scrapy.Request(urlbase, self.select1_parse)

    # #family select
    # def select1_parse(self, response):
    #     for href in response.xpath('//div[@id="divCsLevel_0"]/div/div/div/div/a/@href'):
    #         #print href
    #         url="http://car.bitauto.com" + href.extract()+"koubei/"
    #         print url
    #         yield scrapy.Request(url, self.select2_parse)
    #
    #
    def parse(self, response):  # 综合页面
        x=response.xpath('//p/text()').extract_first()
        temp = re.findall('DataList:(.*)}\)', x)[0]
        data=json.loads(temp)
        length=len(data)
        brandid=[]
        for i in range(0,length):
            brandid.append(data[i]['id'])
        for temp in brandid:
            url="http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=1&pid="+str(temp)+"&rt=serial&callback=callback#"
            yield scrapy.Request(url,self.middle_parse)
        # for href in response.xpath('//a[@id="aTopicListUrl"]/@href').extract():
        #     yield scrapy.Request(href, self.select3_parse)

            # ==============================================================================
            #     def select3_parse(self, response):
            #         global i
            #         for href in response.xpath('//a[@class="more"]/@href').extract():
            #             yield scrapy.Request(href, self.select4_parse)
            #         Pages=response.xpath('//div[@class="the_pages"]/div/a/text()').extract()
            #         if len(Pages)!=0:
            #             maxPages=int(Pages[-2])
            #             print "i"
            #             print i
            #             print "maxpages"
            #             print maxPages
            #             p=maxPages-i
            #             print '\n'
            #             print "page"
            #             print p
            #             i=i+1
            #             if p>1:
            #                 next_page=re.sub("\d-10\.html",str(p)+"-10.html",response.url)
            #                 print next_page
            #                 yield scrapy.Request(next_page, callback=self.select3_parse)
            # ==============================================================================


    def middle_parse(self,response):
        x=response.xpath('//p/text()').extract_first()
        try:
            temp = re.findall('child:(.*)}]\)', x)[0]
            data = json.loads(temp)
            length = len(data)
            for i in range(0, length):
                urlbase = data[i]['urlSpell']
                url = "http://car.bitauto.com/" + str(urlbase) + "/koubei/"
                yield scrapy.Request(url, self.select3_parse)
        except:
            jsondata = re.findall('(?<=child:).*?}]', x)
            length1=len(jsondata)
            for i in range(0,length1):
                data1 = json.loads(jsondata[i])
                length2=len(data1)
                for j in range(0,length2):
                    urlbase = data1[j]['urlSpell']
                    url = "http://car.bitauto.com/" + str(urlbase) + "/koubei/"
                    yield scrapy.Request(url, self.select3_parse)


    def select3_parse(self, response):
        url=response.xpath('//a[@id="aTopicListUrl"]/@href').extract_first()
        yield scrapy.Request(url,self.middle3_parse)
        # for href in response.xpath('//a[@class="more"]/@href').extract():
        #     yield scrapy.Request(href, self.select4_parse)
        #
        # currentUrl = response.xpath('//input[@id="hidListUrl"]/@value').extract_first()
        # cp = int(re.findall(r"\d+", re.findall(r"\d+-10\.html", currentUrl)[0])[0])
        # print "cp"
        # print cp
        #
        # Pages = response.xpath('//div[@class="the_pages"]/div/a/text()').extract()
        # if len(Pages) != 0:
        #     maxPages = int(Pages[-2])
        #
        #     np = cp + 1
        #     print "NP"
        #     print np
        #
        #     if np <= maxPages:
        #         next_page = re.sub("\d-10\.html", str(np) + "-10.html", response.url)
        #         print next_page
        #         yield scrapy.Request(next_page, callback=self.select3_parse)

    # ==============================================================================
    #     location-购车地点
    #     date-购车日期
    #     price-裸车价
    #     score-综合评分
    #     shortComment-评论要点
    #     shopDate-购车时间
    #     mileage-当前公里
    #     presentOilWear-当前油耗
    #     impressionRed-好印象
    #     impressionBlue-差印象
    #     isGoodComment-是否完美口碑
    #     score_fuel-油耗评分
    #     score_control-操控评分
    #     score_cost-性价比评分
    #     score_power-动力评分
    #     score_config-配置评分
    #     score_comfort-舒适度评分
    #     score_space-空间评分
    #     score_appearance-外观评分
    #     score_trim-内饰评分
    #     score_summary-总体评分
    #     fuel-油耗评论
    #     control-操控评论
    #     cost-性价比评论
    #     power-动力评论
    #     config-配置评论
    #     comfort-舒适度评论
    #     space-空间评论
    #     appearance-外观评论
    #     trim-内饰评论
    #     summary-总体评论
    # ==============================================================================


    def middle3_parse(self,response):
        x=response.xpath('//a[@class="more"]/@href').extract()
        length=len(x)
        for i in range(0,length-1):
            href=x[i]
            yield scrapy.Request(href, self.select4_parse)
        next_page=response.xpath('//a[@class="next_on"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.middle3_parse)



    def select4_parse(self, response):  # 详细评论页面
        item = yicheDetailItem()
        try:
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = md5(response.url).hexdigest()
            item['website'] = response.xpath('//div[@class="crumbs-txt"]/a[1]/text()').extract_first()

            item['brandname'] = response.xpath('//div[@class="crumbs-txt"]/a[3]/text()').extract_first()
            item['factoryname'] = response.xpath('//div[@class="crumbs-txt"]/a[4]/text()').extract_first()
            item['familyname'] = response.xpath('//div[@class="crumbs-txt"]/a[5]/text()').extract_first()
            item['vehilename'] = response.xpath('//div[@class="con-l"]/h6/text()').extract_first()

            item['location'] = response.xpath('//span[@class="addredd"]/em/text()').extract_first()
            item['date'] = response.xpath('//span[@class="time"]/em/text()').extract_first()
            temp = response.xpath('//div[@class="price"]/span/em[@class="red"]')
            item['price'] = temp.xpath('string(.)').extract()[0]
            item['score'] = response.xpath('//div[@class="pf-box"]/p/text()').extract_first()
            item['shortComment'] = response.xpath('//div[@class="main-box"]/h6/text()').extract_first()
            item['shopDate'] = response.xpath('//span[@class="date"]/text()').extract_first()
            item['mileage'] = response.xpath('//div[@class="explain"]/span[2]/em/text()').extract_first()
            item['presentOilWear'] = response.xpath('//div[@class="explain"]/span[3]/em/text()').extract_first()
            item['impressionRed'] = response.xpath('//div[@class="tag-keyword"]/a[@class="red"]/text()').extract()
            item['impressionBlue'] = response.xpath('//div[@class="tag-keyword"]/a[@class="blue"]/text()').extract()
            item['isCoodComment'] = response.xpath('//div[@class="main-box"]/span/@class').extract_first()

            ###Score
            item['score_fuel'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u6cb9")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_control'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u64cd")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_cost_efficient'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u6027")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_power'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u52a8")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_config'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u914d")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_comfort'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u8212")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_space'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u7a7a")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_appearance'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u5916")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_trim'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u5185")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            item['score_summary'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u7efc")]/div[@class="start0-box inline-b"]/div/em/@style').extract_first()
            ###comment#
            item['fuel'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u6cb9")]/../p/text()').extract_first()
            item['control'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u64cd")]/../p/text()').extract_first()
            item['cost_efficient'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u6027")]/../p/text()').extract_first()
            item['power'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u52a8")]/../p/text()').extract_first()
            item['config'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u914d")]/../p/text()').extract_first()
            item['comfort'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u8212")]/../p/text()').extract_first()
            item['space'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u7a7a")]/../p/text()').extract_first()
            item['appearance'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u5916")]/../p/text()').extract_first()
            item['trim'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u5185")]/../p/text()').extract_first()
            item['summary'] = response.xpath(
                u'//div[@class="item-box"]/div[@class="head"][contains(text(),"\u7efc")]/../p/text()').extract_first()
        except Exception, e:
            print e
        # print item
        yield item


        # ==============================================================================
        #         t=["操","性","动","配"]
        #         for i in t:
        #             print response.xpath(u'//div[@class="item-box"]/div[@class="head"][contains(text(),i)]/../p/text()').extract_first()
        #
        # ==============================================================================


        # response.xpath('//div[@class="crumbs-txt"]/a[1]').extract()

        # response.xpath('//div[@class="crumbs-txt"]/a[1]/text()').extract()
        # item['score']=response.xpath(u'//p[@class="mark"][contains(text(),"\u5206")]/span/text()').extract_first()
        # item['score']=response.xpath(u'//p[@class="mark"]/span[contains(text(),"4.7")]/../text()').extract_first()
        # item["commentCarInfor"]=href.xpath('u//a[contains(text(),"\u67e5\u770b\u66f4\u591a\u70b9\u8bc4&gt;&gt;")]/@href')

