#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='taoche'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["taoche.com"]
    # start_urls = [
    #     "http://quanguo.taoche.com/all/?orderid=5&direction=2&onsale=0#pagetag"
    # ]
    redis_key = 'taoche'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/taoche.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 2000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'


    # city select
    def parse(self, response):
        for href in response.xpath('//div[@class="header-city-province-text"]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select2_parse)

    # brand select
    def select2_parse(self, response):
        for href in response.xpath('//a[@logwt="bylistindex_sxq_brand"]/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.select3_parse)

    # price select
    def select3_parse(self, response):
        for href in response.xpath('//a[contains(@logwt, "bylistindex_sxq_jiage_click")]/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.list_parse)

    # get car list
    def list_parse(self, response):
        # car_item
        for href in response.xpath('//div[@id="container_base"]/ul/li'):
            url = href.xpath('.//div[@class="item_img"]/a[1]/@href').extract_first()
            datasave1 = href.extract()
            yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="pages-next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url,callback=self.list_parse)

    # get car info
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

        # datasave
        if 'datasave1' in response.meta:
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="detail-over-btn clearfix"]/em')
        status = "sold" if status else "sale"

        price = response.xpath('//input[@id="hidPrice"]/@value')
        price = str(price.extract_first()) if price else "zero"

        datetime = response.xpath('//div[@class="tab-menu margin-md"]/i/text()')
        datetime = str(datetime.extract_first()[5:]) if datetime else "zero"

        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
        yield item
