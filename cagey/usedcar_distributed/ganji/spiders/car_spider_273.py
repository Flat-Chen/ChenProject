#-*- coding: UTF-8 -*-
import re
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import Che273
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='che273'

# original
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["273.cn"]
    # start_urls = [
    #     "http://www.273.cn/car/city.html"
    # ]
    redis_key = 'che273'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/che273.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 1000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    # region select
    def parse(self, response):
        for href in response.xpath('//div[@id="citychange"]/ul[2]/li/dd/span/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, self.parse_list)

    # parse list
    def parse_list(self, response):
        for href in response.xpath('//div[@class="mod-carlist-list"]//div[@data-jslink]'):
            urlbase = href.xpath('@data-jslink').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)

            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//*[@id="js_page_next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.parse_list)

    # get car info
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

        # base info
        if 'datasave1' in response.meta:
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'

        # key and status (sold or sale, price,time)
        status = response.xpath('//*[@class="tips_shelf"]')
        status = "sold" if status else "sale"
        if status == "sold":
            price = "zero"
        else:
            price = response.xpath('//strong[@class="main_price"]/text()')
            price = price.extract_first() if price else "zero"

        datetime = response.xpath('//div[@class="time"]/span/text()')
        datetime = datetime.extract_first() if datetime else "zero"

        # extra
        guideprice = response.xpath(u'//p[contains(text(), "出厂报价")]/strong[1]/text()')
        if guideprice:
            guideprice = guideprice.extract_first()

            tax = response.xpath(u'//p[contains(text(), "出厂报价")]/strong[2]/text()')
            p1 = re.findall(r'\d+\.\d+', tax.extract_first())[0]
            p2 = re.findall(r'\d+\.\d+', guideprice)[0]
            guidepricetax = str(float(p1) + float(p2)) + u'万'
        else:
            guideprice = '-'
            guidepricetax = '-'

        # item loader
        item = Che273()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + str(datetime)
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

        # extra
        item['guideprice'] = guideprice
        item['guidepricetax'] = guidepricetax

        yield item