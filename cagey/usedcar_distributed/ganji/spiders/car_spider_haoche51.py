#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='haoche51'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["haoche51.com"]
    # start_urls = [
    #     "http://www.haoche51.com/cn/ershouche/p1.html"
    # ]
    redis_key = 'haoche51'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/haoche51.log',
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
        for href in response.xpath('//a[@class="iunit"]'):
            urlbase = href.xpath("@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)

        # next page
        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.parse)

    # get car info
    def parse_car(self, response):

        if response.status == 200:
            # count
            self.counts += 1
            logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

            datasave1 = response.meta['datasave1']

            # key and status (sold or sale, price,time)
            status = response.xpath('//div[@class="right-sold"]')
            if status:
                status = "sold"
                price = response.xpath('//div[@class="price"]/span[@class="emph"]/text()')
            else:
                status = "sale"
                price = response.xpath('//span[@class="prc-num fzw6"]/text()')

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