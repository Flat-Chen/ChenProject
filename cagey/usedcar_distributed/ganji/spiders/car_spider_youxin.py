#-*- coding: UTF-8 -*-
import redis
import scrapy
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
import time
import logging
import re
# from ganji.spiders.SpiderInit import spider_original_Init


redis_client2 = redis.Redis(settings['REDIS_SERVER'], port=6379, db=settings['REDIS_DB'])
website ='youxin'

# main
class CarSpider(RedisSpider):



    # basesetting
    name = website
    allowed_domains = ["xin.com"]
    # start_urls=['https://www.xin.com/quanguo/']
    redis_key = 'youxin'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 32,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': False,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/youxin.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 15000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    def parse(self, response):
        node_list = response.xpath('//li[@class="con caritem conHeight"]')
        if not node_list:
            redis_client2.lrem('youxin', response.url)
            print('sorry page, del the url----------', response.url)
            return
        for node in node_list:
            datasave1=node.extract()
            urlbase = node.xpath('.//a[@class="aimg"]/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,meta={"datasave1":datasave1}, callback=self.parse_car)

        next_page= response.xpath(u'//a[contains(text(),"下一页")]')
        if next_page:
            urlbase = response.xpath('./@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,self.parse)

    # get car info
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

        # base info
        datasave1 = "zero"

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[contains(@class,"d-photo")]/em')
        status = "sold" if status else "sale"

        if response.xpath('//span[@class="cd_m_info_jg"]/b/text()'):
            price = response.xpath('//span[@class="cd_m_info_jg"]/b/text()').extract_first()
        else:
            price = "zero"

        datetime =response.xpath('//li[@class="br"]/em/text()')
        datetime = datetime.extract_first() if datetime else "zero"

        #item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+str(datetime)
        print(item['status'])
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, re.sub(r'\s+', ' ', response.xpath('//html').extract_first())]
        yield item