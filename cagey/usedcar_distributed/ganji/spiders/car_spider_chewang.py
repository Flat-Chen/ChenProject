#-*- coding: UTF-8 -*-
import re
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import CheWang
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='chewang'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["carking001.com"]
    # start_urls = [
    #     "http://www.carking001.com/ershouche"
    # ]
    redis_key = 'chewang'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/chewang.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 500000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'

    # get car list
    def parse(self, response):
        for href in response.xpath('//ul[@class="carList"]/li'):
            urlbase = href.xpath("a/@href").extract_first()
            url = response.urljoin(urlbase)
            datasave1 = href.extract()
            yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)

        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)

    # get car info
    def parse_car(self, response):

        if response.status==200 and len(response.xpath('//html').extract_first())>=20000:
            # count
            self.counts += 1
            logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

            # datasave
            if 'datasave1' in response.meta:
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            status = response.xpath('//a[@class="btn_3"]')
            status = "sold" if status else "sale"

            price = response.xpath('//div[@class="car_details_con_2017"]/span/strong/text()').re('\d+.\d+')[0] \
                if response.xpath('//div[@class="car_details_con_2017"]/span/strong/text()').re('\d+.\d+') else "zero"

            datetime = "zero"

            # extra
            info = response.xpath(u'//p[contains(text(), "新车购入价")]/text()').extract()
            if info:
                guidepricetax = re.findall(r'\d+\.\d+', info[0])[0]
                tax = re.findall(u'含(\d+)', info[0])[0]
                guideprice = str(float(guidepricetax) - float(tax)/10000)
            else:
                guideprice =  "zero"

            # item loader
            item = CheWang()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

            item['guideprice'] = guideprice

            yield item