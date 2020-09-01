# -*- coding: utf-8 -*-
import scrapy
from ganji.items import Autohome_koubei_all
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website = 'autohome_koubei_all'


class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["autohome.com.cn"]

    def __init__(self, **kwargs):
        # problem report
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 1010000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'commentCar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    # def start_requests(self):
    #     cars = []
    #     i=0
    #     while i < self.carnum:
    #         i += 1
    #         url = 'http://car.autohome.com.cn/config/spec/' + str(i) + '.html'
    #         if i == 1000:
    #             i = i + 959999
    #         car = scrapy.Request(url, callback=self.parse)
    #         cars.append(car)
    #     return cars

    def start_requests(self):
        cars = []
        for i in range(1, self.carnum):
            if 40000 < i < 1000000:
                pass
            else:
                url = 'http://k.autohome.com.cn/spec/' + str(i) + '/index_1.html'
                yield scrapy.Request(url, callback=self.parse_koubei)
        #         car = scrapy.Request(url, callback=self.parse_koubei)
        #         cars.append(car)
        #         print i
        # return cars

    # def start_requests(self):
    #     cars = []
    #     for i in range(27436, 27437):
    #         url = 'http://k.autohome.com.cn/spec/'+str(i)+'/index_1.html'
    #         car = scrapy.Request(url,callback=self.parse_koubei)
    #         cars.append(car)
    #     return cars

    def parse_koubei(self, response):

        picurl = response.xpath('//dl[@class="appraise-cont-dl fn-left"]/dt/a/img/@src').extract_first()
        for info in response.xpath('//ul[@class="list-ul font-14"]/li'):
            guideprice = info.xpath('span[@class="font-arial"]/a/text()').extract_first()
            score_star = info.xpath('span[contains(span/@class,"score-con")]/span/span/b/@style').extract_first()
            score = info.xpath('span/span[2]/text()').extract_first()
            commment_people = info.xpath('span[@class="font-arial red font-16"]/text()').extract_first()
            data = info.xpath('../li[3]')
            fuel = data.xpath('string(.)').extract()[0].strip()
        for info in response.xpath('//div[@class="fn-clear"]'):
            for data in info.xpath('ul[@class="date-ul fn-left"]'):

                score_space = data.xpath('li[2]/div[2]/text()').extract_first().strip()\
                    if data.xpath('li[2]/div[2]/text()').extract_first() else "-"
                score_power = data.xpath('li[3]/div[2]/text()').extract_first().strip() \
                    if data.xpath('li[3]/div[2]/text()').extract_first() else "-"
                score_control = data.xpath('li[4]/div[2]/text()').extract_first().strip() \
                    if data.xpath('li[4]/div[2]/text()').extract_first() else "-"
                score_fuel = data.xpath('li[5]/div[2]/text()').extract_first().strip() \
                    if data.xpath('li[5]/div[2]/text()').extract_first() else "-"

                # try:
                #     score_space_compare = data.xpath('li[2]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[2]/div[3]/i/@class').extract_first().strip()
                #     score_power_compare = data.xpath('li[3]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[3]/div[3]/i/@class').extract_first().strip()
                #     score_control_compare = data.xpath('li[4]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[4]/div[3]/i/@class').extract_first().strip()
                #     score_fuel_compare = data.xpath('li[5]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[5]/div[3]/i/@class').extract_first().strip()
                # except Exception, e:
                #     pass

                try:
                    score_space_compare = data.xpath('li[2]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[2]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_space_compare = "-"
                try:
                    score_power_compare = data.xpath('li[3]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[3]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_power_compare = "-"
                try:
                    score_control_compare = data.xpath('li[4]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[4]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_control_compare = "-"
                try:
                    score_fuel_compare = data.xpath('li[5]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[5]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_fuel_compare = "-"

            for data in info.xpath('ul[2]'):
                score_comfort = data.xpath('li[2]/div[2]/text()').extract_first().strip()\
                    if data.xpath('li[2]/div[2]/text()').extract_first() else "-"
                score_appearance = data.xpath('li[3]/div[2]/text()').extract_first().strip()\
                    if data.xpath('li[3]/div[2]/text()').extract_first() else "-"
                score_trim = data.xpath('li[4]/div[2]/text()').extract_first().strip()\
                    if data.xpath('li[4]/div[2]/text()').extract_first() else "-"
                score_cost = data.xpath('li[5]/div[2]/text()').extract_first().strip()\
                    if data.xpath('li[5]/div[2]/text()').extract_first() else "-"

                try:
                    score_comfort_compare = data.xpath('li[2]/div[3]/text()').extract()[1].strip()+ " " + data.xpath('li[2]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_comfort_compare="-"
                try:
                    score_appearance_compare = data.xpath('li[3]/div[3]/text()').extract()[1].strip()+ " " + data.xpath('li[3]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_appearance_compare="-"
                try:
                    score_trim_compare = data.xpath('li[4]/div[3]/text()').extract()[1].strip() + " " + data.xpath('li[4]/div[3]/i/@class').extract_first().strip()
                except Exception, e:
                    score_trim_compare ="-"
                try:
                    score_cost_compare = data.xpath('li[5]/div[3]/text()').extract()[1].strip()+ " " + data.xpath('li[5]/div[3]/i/@class').extract_first().strip()
                except Exception,e:
                    score_cost_compare ="-"




        metadata = {"picurl": picurl, "guideprice": guideprice, "score_star": score_star, "score": score,
                    "commment_people": commment_people, "fuel": fuel, "score_space": score_space,
                    "score_space_compare": score_space_compare, "score_power": score_power,
                    "score_power_compare": score_power_compare,
                    "score_control": score_control, "score_control_compare": score_control_compare,
                    "score_fuel": score_fuel,
                    "score_fuel_compare": score_fuel_compare, "score_comfort": score_comfort,
                    "score_comfort_compare": score_comfort_compare,
                    "score_appearance": score_appearance, "score_appearance_compare": score_appearance_compare,
                    "score_trim": score_trim,
                    "score_trim_compare": score_trim_compare, "score_cost": score_cost,
                    "score_cost_compare": score_cost_compare}
        for turl in response.xpath('//div[@class="title-name name-width-01"]/b'):
            url = response.urljoin(turl.xpath('a/@href').extract_first())
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_koubeidetail, dont_filter=True)

        # 下一页跳转
        autohomeid = response.xpath('//div[@class="subnav-title-name"]/a/@href').re('\d+')[0]
        page = int(response.xpath('//div[@class="page-cont"]/div/a[@class="current"]/text()').extract_first()) \
            if response.xpath('//div[@class="page-cont"]/div/a[@class="current"]/text()') else "-"
        maxpage = response.xpath('//div[@class="page-cont"]/div/span/text()').re('\d+')[0] \
            if response.xpath('//div[@class="page-cont"]/div/span/text()') else "-"
        if maxpage != "-":
            maxpage = int(maxpage)
            if page <= maxpage:
                pagenext = page + 1
                print "pagenext", pagenext
                nexturl = 'http://k.autohome.com.cn/spec/' + autohomeid + '/index_' + str(pagenext) + '.html'
                print "nexturl", nexturl
                yield scrapy.Request(nexturl, callback=self.parse_koubei)

    def parse_koubeidetail(self, response):
        # item loader
        item = Autohome_koubei_all()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

        ## meta data
        metadata = response.meta['metadata']
        item['picurl'] = metadata["picurl"]
        item['guideprice'] = metadata["guideprice"]
        item['score_star'] = metadata["score_star"]
        item['score'] = metadata["score"]
        item['commment_people'] = metadata["commment_people"]

        item['fuel'] = metadata["fuel"]
        item['score_space'] = metadata["score_space"]
        item['score_space_compare'] = metadata["score_space_compare"]
        item['score_power'] = metadata["score_power"]
        item['score_power_compare'] = metadata["score_power_compare"]
        item['score_control'] = metadata["score_control"]
        item['score_control_compare'] = metadata["score_control_compare"]
        item['score_fuel'] = metadata["score_fuel"]
        item['score_fuel_compare'] = metadata["score_fuel_compare"]
        item['score_comfort'] = metadata["score_comfort"]
        item['score_comfort_compare'] = metadata["score_comfort_compare"]
        item['score_appearance'] = metadata["score_appearance"]
        item['score_appearance_compare'] = metadata["score_appearance_compare"]
        item['score_trim'] = metadata["score_trim"]
        item['score_trim_compare'] = metadata["score_trim_compare"]
        item['score_cost'] = metadata["score_cost"]
        item['score_cost_compare'] = metadata["score_cost_compare"]

        # add
        item['familyname'] = response.xpath('//div[@class="breadnav"]/a[3]/text()').extract_first()
        item['familynameid'] = response.xpath('//div[@class="breadnav"]/a[3]/@href').re("\d+")[0]
        item['shortdesc'] = response.xpath('//div[@class="subnav-title-name"]/a/text()').extract_first()
        item['autohomeid'] = response.xpath('//div[@class="subnav-title-name"]/a/@href').re('\d+')[0]
        # count
        print "response.url", response.url
        self.counts += 1
        print "download              " + str(self.counts) + "                  items"

        ### crawl buyer info
        item['buyername'] = response.xpath('//div[@class="mouth"]/dl/dt/a/img/@title').extract_first()
        item['buyerid'] = response.xpath('//div[@class="mouth"]/dl/dt/a/@href').re("\d+")[0]
        for temp in response.xpath('//div[@class="mouthcon-cont-left"]/div'):
            item['buy_location'] = temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u4e70\u5730\u70b9")]/dd/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u4e70\u5730\u70b9")]/dd/text()') else "-"
            item['buy_date'] = temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u4e70\u65f6\u95f4")]/dd/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u4e70\u65f6\u95f4")]/dd/text()').extract_first() else "-"
            item['buy_pure_price'] = temp.xpath(u'dl[contains(dt/text(),"\u88f8\u8f66\u8d2d\u4e70\u4ef7")]/dd/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u4e70\u65f6\u95f4")]/dd/text()') else "-"
            item['oil_consume'] = temp.xpath(u'dl[contains(dt/p/text(),"\u6cb9\u8017")]/dd/p[1]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/p/text(),"\u6cb9\u8017")]/dd/p[1]/text()') else "-"
            item['mileage'] = temp.xpath(u'dl[contains(dt/p/text(),"\u6cb9\u8017")]/dd/p[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/p/text(),"\u6cb9\u8017")]/dd/p[2]/text()').extract_first() else "-"
            item['score_space'] = temp.xpath(u'dl[contains(dt/text(),"\u7a7a\u95f4")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u7a7a\u95f4")]/dd/span[2]/text()') else "-"

            item['score_power'] = temp.xpath(u'dl[contains(dt/text(),"\u52a8\u529b")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u52a8\u529b")]/dd/span[2]/text()').extract_first() else "-"
            item['score_control'] = temp.xpath(u'dl[contains(dt/text(),"\u64cd\u63a7")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u64cd\u63a7")]/dd/span[2]/text()').extract_first() else "-"
            item['score_fuel'] = temp.xpath(u'dl[contains(dt/text(),"\u6cb9\u8017")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u6cb9\u8017")]/dd/span[2]/text()').extract_first() else "-"
            item['score_comfort'] = temp.xpath(u'dl[contains(dt/text(),"\u8212\u9002\u6027")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u8212\u9002\u6027")]/dd/span[2]/text()').extract_first() else "-"
            item['score_appearance'] = temp.xpath(u'dl[contains(dt/text(),"\u5916\u89c2")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u5916\u89c2")]/dd/span[2]/text()').extract_first() else "-"
            item['score_trim'] = temp.xpath(u'dl[contains(dt/text(),"\u5185\u9970")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u5185\u9970")]/dd/span[2]/text()').extract_first() else "-"
            item['score_cost'] = temp.xpath(u'dl[contains(dt/text(),"\u6027\u4ef7\u6bd4")]/dd/span[2]/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u6027\u4ef7\u6bd4")]/dd/span[2]/text()').extract_first() else "-"
            item['usage'] = temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u8f66\u76ee\u7684")]/dd/p/text()').extract_first().strip() \
                if temp.xpath(u'dl[contains(dt/text(),"\u8d2d\u8f66\u76ee\u7684")]/dd/p/text()').extract_first() else "-"

        # for temp in response.xpath('//div[@class="mouth-main"]/div[1]'):
        data = response.xpath(u'//div[contains(i/text(),"\u8d28\u91cf")]/../div[2]')
        item['quantity'] = data.xpath('string(.)').extract_first().replace(" ", "") \
            if data.xpath('string(.)').extract_first() else "-"
        item['isGoodComment'] = response.xpath('//div[@class="kou-tit"]/a/i/@class').extract_first()
        condata = response.xpath('//div[@class="text-con"]')
        item['commentDetail'] = re.sub(r".*Jggg?|\(function.*", "", condata.xpath('string(.)').extract_first())
        status = item['buyername'].encode('utf-8') + item['buyerid'].encode('utf-8')
        item['status'] = hashlib.md5(status).hexdigest()
        yield item















