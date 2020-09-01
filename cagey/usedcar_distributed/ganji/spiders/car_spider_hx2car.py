# #-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import GanjiItem
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='hx2car'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["hx2car.com"]
    # start_urls = [
    #     "http://www.hx2car.com/quanguo/soa1"
    # ]
    redis_key = 'hx2car'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/hx2car.log',
    }


    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 300000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    # city select
    def parse(self, response):
        for href in response.xpath('//div[@class="city"]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select2_parse)

    # brand select
    def select2_parse(self, response):
        for href in response.xpath('//div[@class="brand_r"]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)

    # get car list
    def list_parse(self, response):
        # car_item
        for href in response.xpath('//div[@class="Datu_cars"]/div'):
            urlbase = href.xpath('div/a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="num"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.list_parse)


    # get car infor
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "  items",level=logging.INFO)

        # datasave
        datasave1 = response.meta['datasave1']

        # key and status (sold or sale, price,time)
        status = response.xpath(u'//span[@class="num" and contains(text(),"过期")]')
        status = "sold" if status else "sale"

        price = response.xpath('//span[@class="cf60 price"]/span/text()')
        price = ".".join(price.re('\d+')) if price else "zero"

        pagetime = response.xpath('//div[@class="title_infoL"]/span[1]/i[2]/text()')
        pagetime = pagetime.extract_first() if pagetime else "zero"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + pagetime
        item['pagetime'] = pagetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
        yield item