# -*- coding: utf-8 -*-
import logging
import re
import scrapy
import time
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
from ganji.spiders.SpiderInit import spider_original_Init


website ='anxinpai'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["haicj.com"]
    # start_urls = [ "http://www.haicj.com/bidcar", ]
    redis_key = 'anxinpai'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/anxinpai.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 15000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

    def parse(self, response):
        ids = response.xpath(u'//*[@id="auction_list"]/option[contains(text(), "安心拍")]/@value').extract()

        baseurl = 'http://www.haicj.com/bidcar?px=&id='
        for id in ids:
            url = baseurl + id
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        lis = response.xpath('//*[@id="buycarList"]/dl/dd/a/@href').extract()
        for li in lis:
            url = response.urljoin(li)
            yield scrapy.Request(url, callback=self.parse_car)

        # next page
        next_page = response.xpath(u'//a[contains(text(), "下一页")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            if url != response.url:
                yield scrapy.Request(url, self.parse_list)

    def parse_car(self, response):
        # print response.url
        # count
        self.counts += 1
        logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="sold"]')
        status = "sold" if status else "sale"

        price = response.xpath('//div[@class="carshowJgBox"]/strong/text()')
        price = re.findall(r'(\d.*)', price.extract_first()) if price else "zero"

        datetime = "zero"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + str(datetime)
        item['pagetime'] = datetime
        item['datasave'] = [response.xpath('//html').extract_first()]

        yield item
