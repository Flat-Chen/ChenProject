#-*- coding: UTF-8 -*-
import logging
import scrapy
import time
from scrapy_redis.spiders import RedisSpider
from ganji.items import GanjiItem
from ganji.spiders.SpiderInit import spider_original_Init


website ='xcar'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["used.xcar.com.cn"]
    # start_urls = ['http://used.xcar.com.cn/search/100-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0/?sort=createtime']
    redis_key = 'xcar'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/xcar.log',
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

    def parse(self, response):

        next_page = response.xpath('//*[@class="page_down"]')
        if next_page:
            yield scrapy.Request(response.urljoin(next_page.xpath("@href").extract_first()))

        lis = response.xpath("//ul[@class='cal_ul clearfix']/li")
        for li in lis:
            url = response.urljoin(li.xpath("a/@href").extract_first())
            yield scrapy.Request(url=url, callback=self.parse_car)

    # get car info
    def parse_car(self, response):

        # print(response.body)
        if response.status==200 and response.url.find('confirm.php') == -1:
            # count
            self.counts += 1
            logging.log(msg="download   " + str(self.counts) + "  items", level=logging.INFO)

            datasave1 = 'zero'

            # key and status (sold or sale, price,time)
            status = "sale"
            price = response.xpath('//span[@class="cost"]/text()').extract_first()
            datetime ="-".join(response.xpath('//span[@class="time"]/text()').re('\d+'))

            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item