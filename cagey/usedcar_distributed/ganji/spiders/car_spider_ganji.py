#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='ganji'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["ganji.com"]
    # start_urls = [
    #     "http://www.ganji.com/index.htm",]
    redis_key = 'ganji'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/ganji.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 50000000
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
        for href in response.xpath('//div[@class="all-city"]/dl/dd/a/@href'):
            url = response.urljoin(href.extract() + "ershouche/")
            yield scrapy.Request(url, self.select2_parse)

    def select2_parse(self, response):
        for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
            urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.select2_parse)

    # get car info
    def parse_car(self, response):

        if response.status == 200 and response.url.find('confirm.php') == -1:
            # count
            self.counts += 1
            logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

            # datasave
            datasave1 = response.meta['datasave1']

            # key and status (sold or sale, price,time)
            status = "sale"
            price = response.xpath('//i[@class="arial fc-org f20"]/text()')
            price = str(price.extract_first()) if price else "zero"
            datetime =response.xpath('//i[@class="f10 pr-5"]/text()')
            datetime = str(datetime.extract_first()) if datetime else "zero"

            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item
