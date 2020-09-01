#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='iautos'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["iautos.cn"]
    # start_urls = [
    #     "https://so.iautos.cn/quanguo/pasds9vepcatcpbnscac/"
    # ]
    redis_key = 'iautos'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/iautos.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts=0
        self.carnum=1000000
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
        for href in response.xpath('//div[@class="city-li"]/dl/dd/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select2_parse)

    # brand select
    def select2_parse(self, response):
        for href in response.xpath('//ul[@class="brand-list clear"]/li/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select3_parse)

    # price select
    def select3_parse(self, response):
        for href in response.xpath('//div[@class="price-bar bar clear"]/div/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)

    # get car list
    def list_parse(self, response):
        node_list = response.xpath('//ul[@class="car-pic-form-box car-box-list clear"]/li')
        for node in node_list:
            urlbase = node.xpath("a/@href").extract_first()
            urltemp=str(urlbase.strip())
            url="http://"+urltemp[2:len(urltemp)]
            datasave1 = node.extract()
            yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)

        # next page
        next_page = response.xpath(u'//div[@class="pages-box"]/a[contains(text(),"下一页")]/@href')
        if next_page:
            urlbase=str(next_page.extract_first())
            urlbase2="http://so.iautos.cn"
            url = urlbase2+urlbase
            yield scrapy.Request(url, self.list_parse)


    # get car info
    def parse_car(self, response):

        if response.status == 200:
            # count
            self.counts += 1
            logging.log(msg="download   " + str(self.counts) + "  items", level=logging.INFO)

            # datasave
            datasave1 = response.meta['datasave1']

            # key and status (sold or sale, price,time)
            status = response.xpath('//div[@class="sold-out"]')
            status = "sold" if status else "sale"

            price = response.xpath('//strong[@class="z"]/text()')
            price = str(price.extract_first()) if price else "zero"

            datetime = "zero"

            # item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item
