#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='ttpai'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["ttpai.cn"]
    redis_key = 'ttpai'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/ttpai.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 600000
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
        datacheck = len(response.xpath("//html").extract_first())
        if datacheck > 20000:
            # as list
            for href in response.xpath('//li[@class="item"]'):
                urlbase = href.xpath("a/@href").extract_first()
                datasave1 = href.extract()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)

    # get car info
    def parse_car(self, response):
        if response.status == 200:
            # count
            self.counts += 1
            logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

            # datasave
            if 'datasave1' in response.meta:
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            status = "sold"
            price = response.xpath('//strong[@class="s-orange"]/text()')
            price = ".".join(price.re('\d+')) if price else "zero"
            datetime ="zero"

            # item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+str(datetime)
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item
