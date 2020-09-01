#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import GanjiItem
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='haoche99'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["99haoche.com"]
    # start_urls = [
    #     "http://www.99haoche.com/quanguo/all/"
    # ]
    redis_key = 'haoche99'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/haoche99.log',
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

    # get car list
    def parse(self, response):
        # car_item
        for href in response.xpath('//ul[@class="carlist-content"]/li'):
            datasave1 = href.extract()
            urlbase = href.xpath('a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)

        # next page
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url, self.parse)

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
            status = response.xpath('//span[@class="sold-info"]/text()')
            status = "sold" if status else "sale"

            price = response.xpath('//em[@id="priceNum"]/text()')
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