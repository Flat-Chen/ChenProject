#-*- coding: UTF-8 -*-
import json
import time
import scrapy
import logging
from usedcar.items import Chezhibao2
import redis

from scrapy.utils.project import get_project_settings
settings = get_project_settings()

website ='chezhibao2'

class CarSpider(scrapy.Spider):
    name = website
    # allowed_domains = ["ttpai.cn"]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 8,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        settings.set('WEBSITE', website, priority='cmdline')
        self.counts = 0
        self.r = redis.Redis(host=settings["REDIS_HOST"], db=settings["REDIS_DB"])
        self.cookie = self.r.get('chezhibao_cookie').decode('utf8')
        #self.r.close()
        print(self.cookie)

    def start_requests(self):
        url = "https://www.chezhibao.com/auctionHall/screenTabs.htm"
        yield scrapy.FormRequest(url)

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
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
        data = json.loads(response.body_as_unicode())
        list = data['data']['list']
        if len(list) == 0:
            return
        print(len(list))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            , 'Cookie': f'{self.cookie}'
            #, 'Cookie': 'JSESSIONID=C652F6A90D6CCFE568DA294CF8322360'
            , 'Referer': 'https://www.chezhibao.com/auctionHall/index.htm'
        }

        for car in list:
            url2 = 'https://www.chezhibao.com/czhib_detection/auction/{}/auctionCarId/{}.htm?path=1'.format(car['detectionId'], car['auctionCarId'])
            print(url2)
            print("*"*100)
            item = Chezhibao2()
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

            yield scrapy.Request(url2, headers=headers, meta={'item': item}, callback=self.parse_car)

        url1 = 'https://www.chezhibao.com/auctionHall/auctionCarList.htm'
        formdata = response.meta['formdata']
        formdata['page'] = str(int(formdata['page'])+1)
        # print(formdata)

        yield scrapy.FormRequest(url1, formdata=formdata, meta={'formdata': formdata}, callback=self.parse2)

    def parse_car(self, response):
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

        # item loader
        item = response.meta['item']
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()

        yield item
