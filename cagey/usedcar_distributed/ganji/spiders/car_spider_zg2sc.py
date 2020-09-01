#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='zg2sc'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["zg2sc.cn"]
    # start_urls=['http://www.zg2sc.cn/usedcar/search_result.do',]
    redis_key = 'zg2sc'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        # 'DOWNLOAD_TIMEOUT': 60,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/zg2sc.log',

        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
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

    def parse(self, response):
        # print(response.body.decode('gbk'))
        for href in response.xpath('//div[@class="search_car_lb"]/dl'):
            urlbase = href.xpath('./dt/a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)

        next_page= response.xpath(u'//a[contains(text()," >> ")]')
        if next_page:
            nexturl = next_page.xpath('@href').extract_first()
            url = response.urljoin(nexturl)
            yield scrapy.Request(url, callback=self.parse)

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
        status = response.xpath(u'//p[contains(text(),"在售")]')
        status = "sale" if status else "sold"

        price = response.xpath('//input[@id="price"]/@value')
        price = str(price.extract_first()) if price else "zero"

        datetime =response.xpath('//div[@class="carfile_xinxi_text_right"]/dl/dd[2]/text()')
        datetime =datetime.extract_first() if datetime else "zero"

        if price !="zero":
            # count
            self.counts += 1
            logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item
        else:
            pass