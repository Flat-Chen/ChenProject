# -*- coding: utf-8 -*-
import scrapy
from ganji.items import yicheLocalPriceItem
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

website='yiche_local_city_price_new'
class CarSpider(scrapy.Spider):
    name=website
    # city_id_list = [0, 21, 5, 15, 10, 9, 30, 25, 1, 13, 12, 3, 22, 2401, 29, 23, 17, 201, 16, 4, 6, 7, 18, 2601, 28, 14, 3101, 11, 19, 20, 8, 29]



    def __init__(self,**kwargs):
        super(CarSpider, self).__init__(**kwargs)

        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=2000000
        #MonGo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        with open("blm/"+settings['MONGODB_DB']+"/yiche_city.txt") as f:
            content = f.read()
            f.close()
        obj = json.loads(content)
        self.city_id_list = []
        for city in obj:
            self.city_id_list.append(city['cityId'])

        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities[
            "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

        self.browser = webdriver.PhantomJS(executable_path="/home/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=desired_capabilities)
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs", desired_capabilities=desired_capabilities)
        self.browser.set_page_load_timeout(10)
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self):
        self.browser.quit()


    def start_requests(self):

        with open("blm/"+settings['MONGODB_DB']+"/yiche.log", "r") as f:
            file_content = f.read()
            f.close()

        cat_obj = json.loads(file_content)
        for i in range(0, len(cat_obj)):
            if cat_obj[str(i)]['brand_name'] in [u"凯迪拉克",u"别克",u"雪佛兰"]:
                for j in range(0, len(cat_obj[str(i)]["family"])):
                    print("http://car.bitauto.com" + cat_obj[str(i)]["family"][str(j)]["family_url"])
                    yield scrapy.Request(url="http://car.bitauto.com" + cat_obj[str(i)]["family"][str(j)]["family_url"])

    def parse(self, response):
        url = response.xpath("//div[@class='card-layout ']/div[2]/div[1]/a/@href").extract_first()
        if not url:
           url = response.xpath("//div[@class='card-layout unsale']/div[2]/div[1]/a/@href").extract_first()
        url = response.urljoin(url+"peizhi")
        print(url)
        yield scrapy.Request(url=url, callback=self.parse_list)
    # def start_requests(self):
    #     cars=[]
    #     for i in range(1,self.carnum):
    #         url="http://car.bitauto.com/xinyatu/m"+str(i)+"/"
    #         car=scrapy.Request(url,callback=self.parse)
    #         cars.append(car)
    #     return cars

    def parse_list(self, response):

        # with open("blm/"+settings['MONGODB_DB']+"/yiche_city.txt") as f:
        #     content = f.read()
        #     f.close()
        # obj = json.loads(content)
        # city_id_list = []
        # for city in obj:
        #     city_id_list.append(city['cityId'])

        # print(response.body)
        tds = response.xpath("//*[@id='CarCompareContent']/table/tbody/tr[1]/td")
        print(tds)
        for td in tds:
            # print(td.xpath("./div/div/div[1]/div/dl/dd[1]/a/@href").extract_first())
            url = response.urljoin(td.xpath("./div/div/div[1]/div/dl/dd[1]/a/@href").extract_first())

            for city_id in self.city_id_list:
                # print(url + "jiangjia/" + "c%s" % city_id)
                yield scrapy.Request(url=url+"jiangjia/"+"c%s" % city_id, callback=self.parse_detail)

    def parse_detail(self,response):
        item = yicheLocalPriceItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['location'] = response.xpath("//div[@class='desc']/div[2]/div[1]/em/text()").extract_first().replace("最高降幅", "")
        item['location_id'] = response.url.split("/")[5]
        item['discount'] = response.xpath("//div[@class='desc']/div[2]/div[1]/h5/text()").extract_first()
        item['model_id'] = response.url.split("/")[4]
        item['family_id'] = response.url.split("/")[3]
        item['title'] = response.xpath("//*[@id='btnDropCar']/text()").extract_first()
        item['family_name'] = response.xpath("//div[@class='section-header header1']/div[1]/h2/text()").extract_first()
        yield item
