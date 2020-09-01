#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='aokangda'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["akd.cn"]
    # start_urls = ['http://www.akd.cn/carlist/o9/',]
    redis_key = 'aokangda'


    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/aokangda.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 250000
        self.num = 1000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'

    def parse(self,response):
        for href in response.xpath('//div[@class="CarList_main"]/a'):
            urlbase = href.xpath("./@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"datasave1":datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)

    # get car infor
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download   " + str(self.counts) + "  items", level=logging.INFO)

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="p-rel nocar-text"]')
        if status:
            status= "sold"
        else:
            status = "sale"

        datetime = "zero"

        price =response.xpath('//p[@class="CarPrice"]/span/text()').extract_first()

        if not price:
            price = "no price"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(status)+"-"+price
        item['pagetime'] = datetime
        item['datasave'] = [response.xpath('//html').extract_first()]
        yield item

