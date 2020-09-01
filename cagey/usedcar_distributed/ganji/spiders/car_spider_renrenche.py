#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='renrenche'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["renrenche.com"]
    # start_urls = [
    #     "https://www.renrenche.com/sh/ershouche"
    # ]
    redis_key = 'renrenche'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 8,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/renrenche.log',
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

        self.df = 'none'
        self.fa = 'none'

    # region select
    def parse(self, response):
        for href in response.xpath('//div[@class="area-city-letter"]//a[@class="province-item "]/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select_parse)

    # brand
    def select_parse(self, response):
        for href in response.xpath('//div[@id="brand_more_content"]//a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)


    # get car list
    def list_parse(self, response):

        for href in response.xpath('//li[contains(@class, "list-item")]'):
            datasave1= href.extract()
            urlbase = href.xpath('a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)

        next_page = response.xpath('//a[@rrc-event-name="switchright"]/@href').extract_first()
        if not(next_page):
            time.sleep(0.5)
            try:
                page = int(response.xpath('//li[@class="active"]/a[@href="javascript:void(0);"]/text()').extract_first())+1
            except Exception as e:
                print(e)
                yield scrapy.Request(url=response.url, dont_filter=True)
                return
            location=response.url.find("ershouche")+9
            newpage = response.url[0:location]+"/p"+str(page)
            url = response.urljoin(newpage)
        else:
            url = response.urljoin(next_page)

        yield scrapy.Request(url, callback=self.list_parse)

    # get car info
    def parse_car(self, response):

        if response.status == 200:
            # count
            self.counts += 1
            logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

            # datasave
            if 'datasave1' in response.meta:
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            if response.xpath("//*[@id='sold_button']"):
                status = "sold"
            else:
                status = "sale"

            price = response.xpath('//span[@class="price"]/text()').extract_first()
            datetime =time.strftime('%Y-%m-%d %X', time.localtime())

            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item