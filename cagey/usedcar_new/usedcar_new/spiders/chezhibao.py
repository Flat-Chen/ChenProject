#-*- coding: UTF-8 -*-
import json
import re
import time

import redis
import scrapy
import logging
from scrapy.utils.project import get_project_settings
from usedcar_new.items import Chezhibao

setting = get_project_settings()

website ='chezhibao2'


class CarSpider(scrapy.Spider):
    name = website
    # allowed_domains = ["ttpai.cn"]
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_TABLE': 'chezhibao2_online',
        'MYSQL_PORT': '3306',
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_USER': 'dataUser94',
        'MYSQL_PWD': '94dataUser@2020',
        'MONGODB_COLLECTION': 'chezhibao2_online',
        'WEBSITE': website,
        'MYSQL_DB': 'people_zb',
        'CrawlCar_Num': 1000000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOADER_MIDDLEWARES': {
            # 'usedcar_new.middlewares.ProxyMiddleware': 700,
            # 'usedcar_new.middlewares.MoGuProxyMiddleware': 700,
            # 'usedcar_new.middlewares.SeleniumIPMiddleware': 701,
            # 'usedcar_new.middlewares.UsedcarNewDownloaderMiddleware': 701,
            # 'usedcar_new.middlewares.MyproxiesSpiderMiddleware': 701,
        },
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.UsedcarNewPipeline': 300,
        },

    }

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.r = redis.Redis(host='192.168.1.92', db=4)
        self.cookie = self.r.get('chezhibao_cookie').decode('utf8')
        self.r.close()
        # self.cookie = "JSESSIONID=4BC6F259AC9911E9963C9305D85C625C"
        self.counts = 0
        print(self.cookie)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            , 'Cookie': f'{self.cookie}'
            # , 'Cookie': 'JSESSIONID=C652F6A90D6CCFE568DA294CF8322360'
            , 'Referer': 'https://www.chezhibao.com/auctionHall/index.htm'
        }

    def start_requests(self):
        url = "https://www.chezhibao.com/auctionHall/screenTabs.htm"
        yield scrapy.FormRequest(url)

    def parse(self, response):
        data = json.loads(response.text)
        tabs = data['data']['tabs']
        print(len(tabs))
        for tab in tabs:
            url = 'https://www.chezhibao.com/auctionHall/auctionCarList.htm'
            formdata = {'tabVersion': data['data']['tabVersion'],
                    'tabId': tab['name'],
                    'page': '1',
                    'orderBy': '0'}

            yield scrapy.FormRequest(url, formdata=formdata, meta={'formdata': formdata}, callback=self.parse2)

    def parse2(self, response):
        # print(response.url)
        data = json.loads(response.text)
        list = data['data']['list']
        # print(list)
        if len(list) == 0:
            return
        print(len(list))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            , 'Cookie': f'{self.cookie}'
            # , 'Cookie': 'JSESSIONID=C652F6A90D6CCFE568DA294CF8322360'
            , 'Referer': 'https://www.chezhibao.com/auctionHall/index.htm'
        }
        # print(headers)
        # print("*"*100)

        for car in list:
            url2 = 'https://www.chezhibao.com/czhib_detection/auction/{}/auctionCarId/{}.htm?path=1'.format(car['detectionId'], car['auctionCarId'])
            item = Chezhibao()
            # print(url2)
            # print("*"*100)
            # item['carid'] = str(car['carId'])
            item['accident_score'] = str(car['accidentCar'])
            item['city'] = car['carCityName']
            # item['totalgrade'] = car['carRating']
            item['emission'] = car['carEnv']
            item['shortdesc'] = car['carType']
            item['pagetitle'] = car['carTitle']
            item['emission'] = car['carEnv']
            item['img_url'] = car['defaultImg']
            item['years'] = str(int(car['age'])+1)
            item['mileage'] = car['carMileage']
            item['registerdate'] = car['carRegist']
            item['carno'] = car['carNo']
            item['series'] = car['carModel']
            # item['bodystyle'] = car['vehicleType']

            yield scrapy.Request(url2, headers=headers, meta={'item': item}, callback=self.parse_car_detail)

        url1 = 'https://www.chezhibao.com/auctionHall/auctionCarList.htm'
        formdata = response.meta['formdata']
        formdata['page'] = str(int(formdata['page'])+1)
        # print(formdata)

        yield scrapy.FormRequest(url1, formdata=formdata, meta={'formdata': formdata}, callback=self.parse2)

    def parse_car_detail(self, response):
        self.counts += 1
        # logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

        # item loader
        item = response.meta['item']
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        # item["pagetime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['statusplus'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()
        item["insurance2_date"] = response.xpath("//th[contains(text(),'商业保险')]/following-sibling::td[1]/text()").get()
        item["carcard"] = response.xpath("//th[contains(text(),'机动车行驶证')]/following-sibling::td[1]/text()").get()

        waiguan_tr = response.xpath("//*[@id='main0']/ul[2]/li/div[2]/div[7]//tr")
        if waiguan_tr:
            waiguan_list = list()
            for tr in waiguan_tr:
                sunshang_dic = dict()
                sunshang_dic["name"] = tr.xpath("./th//text()").get()
                sunshang_dic["content"] = tr.xpath("./td//text()").get().replace(" ", "").replace("\n", "")
                type = tr.xpath("./th/span/@class").get()
                if "bg_yellow" in type:
                    sunshang_dic["type"] = "缺陷项"
                elif "bg_red" in type:
                    sunshang_dic["type"] = "事故项"
                elif "bg_org" in type:
                    sunshang_dic["type"] = "特定项"
                waiguan_list.append(sunshang_dic)
            item["outer_desc"] = str(waiguan_list)

        gujia_tr = response.xpath("//*[@id='main0']/ul[2]/li/div[2]/div[3]//tr")
        gujia_list = list()
        if gujia_tr:
            for tr in gujia_tr:
                sunshang_dic = dict()
                sunshang_dic["name"] = tr.xpath("./th//text()").get()
                sunshang_dic["content"] = tr.xpath("./td//text()").get().replace(" ", "").replace("\n", "")
                type = tr.xpath("./th/span/@class").get()
                if "bg_yellow" in type:
                    sunshang_dic["type"] = "缺陷项"
                elif "bg_red" in type:
                    sunshang_dic["type"] = "事故项"
                elif "bg_org" in type:
                    sunshang_dic["type"] = "特定项"
                gujia_list.append(sunshang_dic)
            item["safe_desc"] = str(gujia_list)

        jicang_tr = response.xpath("//*[@id='main0']/ul[2]/li/div[2]/div[11]//tr")
        dipan_tr = response.xpath("//*[@id='main0']/ul[2]/li/div[2]/div[19]//tr")
        road_list = list()
        if jicang_tr:
            for tr in jicang_tr:
                sunshang_dic = dict()
                sunshang_dic["name"] = tr.xpath("./th//text()").get()
                sunshang_dic["content"] = tr.xpath("./td//text()").get().replace(" ", "").replace("\n", "")
                type = tr.xpath("./th/span/@class").get()
                if "bg_yellow" in type:
                    sunshang_dic["type"] = "缺陷项"
                elif "bg_red" in type:
                    sunshang_dic["type"] = "事故项"
                elif "bg_org" in type:
                    sunshang_dic["type"] = "特定项"
                road_list.append(sunshang_dic)
        if dipan_tr:
            for tr in dipan_tr:
                sunshang_dic = dict()
                sunshang_dic["name"] = tr.xpath("./th//text()").get()
                sunshang_dic["content"] = tr.xpath("./td//text()").get().replace(" ", "").replace("\n", "")
                type = tr.xpath("./th/span/@class").get()
                if "bg_yellow" in type:
                    sunshang_dic["type"] = "缺陷项"
                elif "bg_red" in type:
                    sunshang_dic["type"] = "事故项"
                elif "bg_org" in type:
                    sunshang_dic["type"] = "特定项"
                road_list.append(sunshang_dic)
        if len(road_list) > 0:
            item["road_desc"] = str(road_list)

        neishi_tr = response.xpath("//*[@id='main0']/ul[2]/li/div[2]/div[15]//tr")
        neishi_list = list()
        if neishi_tr:
            for tr in neishi_tr:
                sunshang_dic = dict()
                sunshang_dic["name"] = tr.xpath("./th//text()").get()
                sunshang_dic["content"] = tr.xpath("./td//text()").get().replace(" ", "").replace("\n", "")
                type = tr.xpath("./th/span/@class").get()
                if "bg_yellow" in type:
                    sunshang_dic["type"] = "缺陷项"
                elif "bg_red" in type:
                    sunshang_dic["type"] = "事故项"
                elif "bg_org" in type:
                    sunshang_dic["type"] = "特定项"
                neishi_list.append(sunshang_dic)
            item["inner_desc"] = str(neishi_list)

        special = response.xpath('//*[@id="specialExamMenuTwo"]/@onclick').get()
        if special:
            # print(special)
            special_str = re.findall('\', (.*?)\)', special)[0]
            code_list = special_str.split(',')
            # print(code_list)
            special_url = f"https://www.chezhibao.com/czhib_detection/loadCarMaintenance/{code_list[0]}/{code_list[1]}.htm"
            yield scrapy.Request(
                url=special_url,
                callback=self.parse_special,
                meta={"item": item},
                headers=self.headers
            )
        else:
            yield item
            # print(item)
            # print("-"*100)

    def parse_special(self, response):
        # print("*" * 100)
        # print(response.url)
        item = response.meta["item"]
        # print(response.text)
        data = json.loads(response.text)
        if data["status"]:
            detail_data = data["data"]["aucsMaintainInfoVo"]
            item["repairinfo"] = str(detail_data["detailList"])
            yield item
            # print(item)