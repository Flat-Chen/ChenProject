#-*- coding: UTF-8 -*-
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from scrapy.xlib.pydispatch import dispatcher

from ganji.items import GanjiItem
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='guazi'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["guazi.com"]
    # start_urls = ["http://www.guazi.com/qg/buy",]
    redis_key = 'guazi'

    custom_settings = {
        # 并发
        # 'DOWNLOAD_DELAY': 2.5,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        # 'CONCURRENT_REQUESTS': 4,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/guazi.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 1500000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'

        self.desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        self.desired_capabilities[
            "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])

        # self.browser.start_session(self.desired_capabilities)
        self.browser.set_page_load_timeout(300)

        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()


    def parse(self, response):
        lis = response.xpath("//ul[@class='carlist clearfix js-top']/li")

        for li in lis:
            yield scrapy.Request(response.urljoin(li.xpath("./a/@href").extract_first()), callback=self.parse_car)
            return

        next = response.xpath("//a[@class='next']/@href")
        if next:
            yield scrapy.Request(url=response.urljoin(next.extract_first()), callback=self.parse)
        else:
            if response.url == 'http://www.guazi.com/qg/buy':
                yield scrapy.Request(url='http://www.guazi.com/qg/buy', callback=self.parse, dont_filter=True)
            else:
                print(response.url, 'no next')

    # get car info
    def parse_car(self, response):
        # status check
        if response.status == 200:
            # count
            self.counts += 1
            logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

            # base info
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            status = response.xpath('//*[@class="graybtn"]')
            status = "sold" if status else "sale"
            price = response.xpath('//b[@class="f30 numtype"]/text()')
            price = price.extract_first()[1:] if price else "zero"
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