# -*- coding: utf-8 -*-
import scrapy
from ganji.items import newcar2017Item
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium.webdriver import DesiredCapabilities

website='newcar_2017'
class CarSpider(scrapy.Spider):
    name=website

    def __init__(self,**kwargs):
        super(CarSpider, self).__init__(**kwargs)

        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=2000000
        #MonGo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        for i in range(1,13):
            if i < 6:
                yield scrapy.Request(url="http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/20170%d.htm" % i)
            elif i >= 6 < 10:
                yield scrapy.Request(url="http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/20170%d.html" % i)
            else:
                yield scrapy.Request(url="http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/2017%d.html" % i)

    def parse(self, response):
        divs = response.xpath("//*[@id='divBody']")
        for div in divs:
            td = div.xpath("./div[@id='divContent']/table/tbody/tr/td[1]/table[2]/tbody/tr/td[2]")[0]
            item = newcar2017Item()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            if td.xpath("./div[3]/strong/text()").extract_first():
                item['title'] = td.xpath("./div[3]/strong/text()").extract_first()
            else:
                item['title'] = td.xpath("./div[1]/strong/text()").extract_first()
            for j in range(1, len(td.xpath("./table/tbody/tr[1]/td"))):
                item['id'] = td.xpath(
                    "./table/tbody/tr[1]/td[%d]/div/font/strong/text()" % (j + 1)).extract_first().replace("配置ID：", "").strip()
                trs = td.xpath("./table/tbody/tr")
                for tr in trs:
                    if trs.index(tr) != 0:
                        if tr.xpath("./th/text()").extract_first().find("外廓尺寸长") >= 0:
                            item['length'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr)+1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("外廓尺寸宽") >= 0:
                            item['width'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("外廓尺寸高") >= 0:
                            item['height'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("总质量") >= 0:
                            item['weight'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("整备质量") >= 0:
                            item['gear_weight'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("最高车速") >= 0:
                            item['speed'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("续驶里程") >= 0:
                            item['miles'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("Ekg单位载质量能量消耗量") >= 0:
                            item['ekg'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("电池系统总质量占整车整备质量比例") >= 0:
                            item['battery_weight_ratio'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("电池系统能量密度") >= 0:
                            item['energy_density'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("储能装置种类") >= 0:
                            item['restore_type'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("驱动电机类型") >= 0:
                            item['electricity_machine_type'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("驱动电机峰值功率/转速/转矩") >= 0:
                            item['electricity_machine_detail'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                        if tr.xpath("./th/text()").extract_first().find("储能装置总储电量") >= 0:
                            item['store_energy'] = td.xpath(
                                "./table/tbody/tr[%d]/td[%d]/text()" % (trs.index(tr) + 1, j)).extract_first().strip()
                item['status'] = item['url'] + item['id']
                yield item


                # index = 2
                # item['id'] = td.xpath("./table/tbody/tr[1]/td[%d]/div/font/strong/text()" % (j+1)).extract_first().replace("配置ID：", "").strip()
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("外廓尺寸长"):
                #     item['length'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()"% (index)).find("外廓尺寸宽"):
                #     item['width'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("外廓尺寸高"):
                #     item['height'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("总质量"):
                #     item['weight'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("整备质量"):
                #     item['gear_weight'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("最高车速"):
                #     item['speed'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("续驶里程"):
                #     item['miles'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("Ekg单位载质量能量消耗量"):
                #     item['ekg'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("电池系统总质量占整车整备质量比例"):
                #     item['battery_weight_ratio'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("电池系统能量密度"):
                #     item['energy_density'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("储能装置种类"):
                #     item['restore_type'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("驱动电机类型"):
                #     item['electricity_machine_type'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("驱动电机峰值功率/转速/转矩"):
                #     item['electricity_machine_detail'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                #     index = index + 1
                # if td.xpath("./table/tbody/tr[%d]/th/text()" % (index)).find("储能装置总储电量"):
                #     item['store_energy'] = td.xpath("./table/tbody/tr[%d]/td[%d]/text()" % (index, j)).extract_first().strip()
                # item['status'] = item['url'] + item['id']
                # yield item



