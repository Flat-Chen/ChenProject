#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import Auto51
import time
import logging
import re

from ganji.spiders.SpiderInit import spider_original_Init

website ='auto51'

class CarSpider(RedisSpider):
    name = website
    allowed_domains = ["51auto.com"]
    # start_urls =["http://m.51auto.com/quanguo/pabmdcigf"]
    redis_key = 'auto51'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': False,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/auto51.log',
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

        self.df = 'none'
        self.fa = 'none'

        super(CarSpider, self).__init__()

    def parse(self,response):
        x = response.xpath('//div[@class="carlist"]/a')
        if x != []:
            count = response.xpath("//div[@class='pagination_box']/div/div/span/text()").extract_first()
            count = int(re.findall("^1\/(.*?)$", count)[0])
            for i in range(count):
                pageNum = i + 1
                yield scrapy.Request("http://m.51auto.com/quanguo/pabmdcigf?page=%d" % pageNum, callback=self.parse_list)

    def parse_list(self, response):
        x = response.xpath('//div[@class="carlist"]/a')
        for temp in x:
            url = temp.xpath('@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_car)


    def parse_car(self,response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="p-rel nocar-text"]')
        if status:
            status= "sold"
            price = response.xpath('//p[@style="text-align: center;color: #EF4C07;font-weight:bold;margin-bottom:12px;"]/text()')
            price = round(float(".".join(price.re('\d+')[:2]))/0.3,2)
        else:
            status = "sale"
            price = response.xpath('//div[@class="grid-c-l car-price"]/strong/text()')
            price = ".".join(price.re('\d+'))
        datetime = "zero"

        # item loader
        item = Auto51()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+ datetime
        item['pagetime'] = datetime
        item['datasave'] = [response.xpath('//html').extract_first()]

        # turn over
        url = response.xpath('//input[@id="vehiclefileinfo"]/@value')

        if url:
            # print url.extract_first()
            yield scrapy.Request(url.extract_first(), meta={'meta1': item}, callback=self.parse_car2)

    def parse_car2(self, response):
        """turn over, go on parse"""

        item = response.meta['meta1']

        guideprice = response.xpath(u'//span[contains(text(), "厂商指导价")]/../span[2]/text()')
        if guideprice:
            item['guideprice'] = guideprice.extract_first().strip()

        factoryname = response.xpath(u'//span[text()="厂商"]/../span[2]/text()')
        if factoryname:
            item['factoryname'] = factoryname.extract_first()

        level = response.xpath(u'//span[text()="级别"]/../span[2]/text()')
        if level:
            item['level'] = level.extract_first()

        geartype = response.xpath(u'//span[text()="变速箱"]/../span[2]/text()')
        if geartype:
            item['geartype'] = geartype.extract_first()

        gearnumber = response.xpath(u'//span[text()="挡位个数"]/../span[2]/text()')
        if gearnumber:
            item['gearnumber'] = gearnumber.extract_first()

        length = response.xpath(u'//span[contains(text(), "长度")]/../span[2]/text()')
        if length:
            item['length'] = length.extract_first()

        width = response.xpath(u'//span[contains(text(), "宽度")]/../span[2]/text()')
        if width:
            item['width'] = width.extract_first()

        height = response.xpath(u'//span[contains(text(), "高度（mm）")]/../span[2]/text()')
        if height:
            item['height'] = height.extract_first()

        bodystyle = response.xpath(u'//span[contains(text(), "车体结构")]/../span[2]/text()')
        if bodystyle:
            item['bodystyle'] = bodystyle.extract_first()

        wheelbase = response.xpath(u'//span[contains(text(), "轴距")]/../span[2]/text()')
        if wheelbase:
            item['wheelbase'] = wheelbase.extract_first()

        doors = response.xpath(u'//span[contains(text(), "车门数")]/../span[2]/text()')
        if doors:
            item['doors'] = doors.extract_first()

        seats = response.xpath(u'//span[contains(text(), "座位数")]/../span[2]/text()')
        if seats:
            item['seats'] = seats.extract_first()

        frontgauge = response.xpath(u'//span[contains(text(), "轮距")]/../span[2]/text()')
        if frontgauge:
            item['frontgauge'] = frontgauge.extract_first().strip().split('/')[0]

        lwvnumber = response.xpath(u'//span[contains(text(), "汽缸数")]/../span[2]/text()')
        if lwvnumber:
            item['lwvnumber'] = lwvnumber.extract_first()

        maxpower = response.xpath(u'//span[contains(text(), "最大功率")]/../span[2]/text()')
        if maxpower:
            item['maxpower'] = maxpower.extract_first()

        maxnm = response.xpath(u'//span[contains(text(), "最大扭矩")]/../span[2]/text()')
        if maxnm:
            item['maxnm'] = maxnm.extract_first()

        fueltype = response.xpath(u'//span[contains(text(), "燃料形式")]/../span[2]/text()')
        if fueltype:
            item['fueltype'] = fueltype.extract_first()

        fuelnumber = response.xpath(u'//span[contains(text(), "燃油标号")]/../span[2]/text()')
        if fuelnumber:
            item['fuelnumber'] = fuelnumber.extract_first()

        driverway = response.xpath(u'//span[contains(text(), "驱动方式")]/../span[2]/text()')
        if driverway:
            item['driverway'] = driverway.extract_first()

        yield item
