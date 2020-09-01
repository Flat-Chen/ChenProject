#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import GanjiItem
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='cn2che'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["cn2che.com"]
    # start_urls = [
    #     "http://www.cn2che.com/serial.html",
    # ]
    redis_key = 'cn2che'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/cn2che.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 800000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    # get family list
    def parse(self, response):
        # car_item
        for href in response.xpath(u'//div[@class="msglist12"]/dl/dd/a[contains(text(),"二手车")]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_list)

    # get car list
    def parse_list(self, response):
        # car_item
        for href in response.xpath('//div[contains(@class,"cheyuan")]/ul/li'):
            urlbase = href.xpath("span/a/@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)

            # next page
            next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.parse_list)

    # get car info
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "   items",
                    level=logging.INFO)

        datasave1 = response.meta['datasave1']

        # key and status (sold or sale, price,time)
        status = response.xpath('//li[@id="car_state_text"]/@val')
        if status:
            if int(status.extract_first()) == 1:
                status = "sale"
            else:
                status = "sold"
        else:
            status = "sale"

        price = response.xpath('//strong[@id="price"]/text()')
        price = ".".join(price.re('\d+')) if price else "zero"

        pagetime = response.xpath('//li[@class="sendtime"]/text()')
        pagetime = "-".join(pagetime.re('\d+')) if pagetime else "zero"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + pagetime
        item['pagetime'] = pagetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
        yield item