#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import GanjiItem
import time

from ganji.spiders.SpiderInit import spider_original_Init

website ='chezhibao'

class CarSpider(RedisSpider):
    # basesetting
    name = website
    # start_urls = [
    #     "https://search.chezhibao.com/auctionHistory/list.htm?page=1&brand=0&mode=0&year=0&mileage=0"
    # ]
    redis_key = 'chezhibao'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/chezhibao.log',
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

    # brand select
    def parse(self, response):
        for href in response.xpath('//div[contains(@class, "_section _section")]/div/div/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select3_parse)

    # age select
    def select3_parse(self, response):
        for href in response.xpath('//ul[@id="carAge_filter"]/li/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select4_parse)

    # mileage select
    def select4_parse(self, response):
        for href in response.xpath('//ul[@id="mileage_filter"]/li/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)


    def list_parse(self,response):

        next_page = response.xpath("//*[@class='_btn _next']/@href").extract_first()
        url = response.urljoin(next_page)
        if 'javascript' not in url:
            yield scrapy.Request(url=url, callback=self.list_parse)

        divs = response.xpath("//*[@class='__loop']")
        for div in divs:
            url = response.urljoin(div.xpath('div[1]/div[1]/a/@href').extract_first())
            yield scrapy.Request(url=url, callback=self.parse_detail)


    def parse_detail(self, response):

        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['pagetime'] = "zero"
        item['datasave'] = [response.xpath('//html').extract_first()]
        yield item

