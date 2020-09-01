#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init

website ='ygche'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["ygche.com.cn"]
    # start_urls=['http://www.ygche.com.cn/list/0_0_0_0_0_0_0_0_0_1.html']
    redis_key = 'ygche'

    custom_settings = {
        # 并发
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/ygche.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 3000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    # car list parse
    def parse(self,response):
        for href in response.xpath('//div[@class="main-cont"]/div'):
            urlbase = href.xpath('./div[2]/h3/a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)

        nextpage = response.xpath('//a[@class="pl15 forbidden next"]/@href')
        if nextpage:
            url = response.urljoin(nextpage.extract_first())
            yield scrapy.Request(url, callback=self.parse)

    # get car info
    def parse_car(self, response):

        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

        # datasave
        if 'datasave1' in response.meta:
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'

        # key and status (sold or sale, price,time)
        status = response.xpath('//a[@class="already-buy"]')
        status = "sold" if status else "sale"
        price = response.xpath('//em[@id="emprice"]/text()')
        price = str(price.extract_first()) if price else "zero"
        datetime = response.xpath(u'//li[contains(text(),"\u4e0a\u67b6\u65f6\u95f4")]/span/text()')
        datetime = "-".join(datetime.re('\d+')) if datetime else "zero"

        #item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
        yield item
