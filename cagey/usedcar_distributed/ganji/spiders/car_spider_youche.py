#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='youche'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["youche.com"]
    # start_urls = [ "https://www.youche.com/ershouche", ]
    redis_key = 'youche'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/youche.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 1000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    def parse(self,response):
        x=response.xpath('//ul[@class="conListUL"]/li')
        for temp in x:
            urlbase = temp.xpath('div/div[3]/div/div/a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,self.parse_car)

        next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url,self.parse, priority=1)

    # get car info
    def parse_car(self, response):

        if response.status == 200:
            # count
            self.counts += 1
            logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

            datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            status = response.xpath('//div[@id="bigImg"]/em/@class')
            if status and status.extract_first()=="tag jijiangksBlue":
                status= "willsale"
            else:
                status = "insale"

            price = response.xpath('//div[@class="newCarPrice"]/span[@class="sp02"]/text()')
            price = price.extract_first() if price else "zero"
            pagetime = time.strftime('%Y-%m-%d %X', time.localtime())

            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)
            item['pagetime'] = pagetime
            item['datasave'] = [datasave1 ,response.xpath('//html').extract_first()]
            yield item