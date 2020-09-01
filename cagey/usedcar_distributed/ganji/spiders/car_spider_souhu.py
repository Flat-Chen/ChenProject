#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanJi
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='souhu'


class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["sohu.com"]
    # start_urls=['http://2sc.sohu.com/buycar/pg1.shtml',]
    redis_key = 'souhu'


    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 16,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/souhu.log',
    }


    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 3000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'

    # price select
    def parse(self, response):
        for href in response.xpath(u'//div[@class="price-sc clearfix lab_block"]/a[contains(@title, "万")]/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select2_parse)

    # mili select
    def select2_parse(self, response):
        for href in response.xpath(u'//ul[@id="mileage_option_list"]/li/a[contains(text(), "万")]/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)

    # list select
    def list_parse(self,response):
        node_list =response.xpath('//div[@class="carShow"]/div')
        for node in node_list:
            urlbase=node.xpath('a[@class="car-link"]/@href').extract_first()
            url=response.urljoin(urlbase)
            datasave1=node.extract()
            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)

        next_page=response.xpath('//span[contains(text(),">")]/../@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url, self.list_parse)

    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

        # base info
        datasave1 = 'zero'

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="ask-box"]/a')
        status = "sale" if status else "sold"

        price = response.xpath('//span[@class="car-price"]/text()')
        price = ".".join(price.re('\d+')) if price else "zero"

        datetime = response.xpath('//label[@class="message"]/text()')
        datetime = "-".join(datetime.re('\d+')) if datetime else "zero"

        # extra
        gap = response.xpath('//span[@class="car-price-new"]/text()')
        gap = ".".join(gap.re('\d+')) if price else "zero"
        guideprice = float(price) + float(gap)

        # item loader
        item = GanJi()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

        # extract
        item['guideprice'] = str(guideprice)

        yield item