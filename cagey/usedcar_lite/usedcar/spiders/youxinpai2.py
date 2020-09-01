#-*- coding: UTF-8 -*-
import json
import time
import scrapy
import logging

from usedcar.items import Youxinpai2
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

website ='youxinpai2'


class CarSpider(scrapy.Spider):
    name = website
    # allowed_domains = ["ttpai.cn"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        settings.set('WEBSITE', website, priority='cmdline')
        self.counts = 0

    def start_requests(self):
        print("start_request")
        url = "http://www.youxinpai.com/halfMinUpdateList"
       # yield scrapy.Request(url, method="POST", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',"Referer":"http://www.youxinpai.com/trade"})
        yield scrapy.FormRequest(url, callback=self.parse, headers={
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      "Referer": "http://www.youxinpai.com/index"})


    def parse(self, response):
        print("start_parse")
        data = json.loads(response.body_as_unicode())
        carlist = data['data']['data']['auctionHallResponeList']
        print(len(carlist))
        for car in carlist:
            url = 'http://www.youxinpai.com/home/trade/detail/{}/{}'.format(car['publishID'], car['crykey'])
            yield scrapy.Request(url, callback=self.parse_car)

    def parse_car(self, response):
        print("*"*10)
        print(response.text)
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

        # item loader
        item = Youxinpai2()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()

        times = response.xpath('//*[@id="leftInfoBox"]/table[2]//tr[1]/td[2]/text()')
        #if times:
         #   if times.extract_first() == '�?:
          #     item['change_times'] = '0'
           # else:
            #   item['change_times'] = times.extract_first().strip()
        #else:
        item['change_times'] = ''
        yield item

