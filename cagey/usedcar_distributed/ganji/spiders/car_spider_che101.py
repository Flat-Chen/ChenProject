#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import Che101
import time
import logging
from hashlib import md5

from ganji.spiders.SpiderInit import spider_original_Init

website ='che101'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["che101.com"]
    # start_urls = [
    #     "http://www.che101.com/buycar/",
    # ]
    redis_key = 'che101'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/che101.log',
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

    # get car list
    def parse(self, response):

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.parse, priority=1)

        # car_item
        for href in response.xpath('//ul[@class="carList_286 cf"]/li'):
            urlbase=href.xpath('./a/@href').extract_first()
            pagetime= href.xpath('./a/span[@class="lastest"]/text()').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={'datasave1':datasave1, 'pagetime':pagetime}, callback=self.parse_car)

    # get car info
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

        # base info
        datasave1 = response.meta['datasave1']
        pagetime = response.meta['pagetime']

        # key and status (sold or sale, price,time)
        status = "sale"
        price = response.xpath('//span[@id="total_price"]/text()')
        price = str(price.extract_first()) if price else "zero"

        # item loader
        item = Che101()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + md5(pagetime.encode("utf-8")).hexdigest()
        item['pagetime'] = pagetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

        # turn over
        more_page = response.xpath('//div[@class="btn_more"]/a/@href')

        if more_page:
            link = response.urljoin(more_page.extract_first())
            yield scrapy.Request(link, meta={'meta1': item}, callback=self.parse_car2)
        else:
            yield item

    def parse_car2(self, response):
        """turn over, go on parse"""
        item = response.meta['meta1']

        # extra
        fueltype = response.xpath(u'//td[contains(text(), "燃料类型")]/../td[2]/text()')
        if fueltype:
            item['fueltype'] = fueltype.extract_first()
        else:
            item['fueltype'] = '-'

        doors = response.xpath(u'//td[contains(text(), "车门数")]/../td[2]/text()')
        if doors:
            item['doors'] = doors.extract_first()
        else:
            item['doors'] = '-'

        seats = response.xpath(u'//td[contains(text(), "乘员人数")]/../td[4]/text()')
        if seats:
            item['seats'] = seats.extract_first()
        else:
            item['seats'] = '-'

        length = response.xpath(u'//td[contains(text(), "车长")]/../td[4]/text()')
        if length:
            item['length'] = length.extract_first()
        else:
            item['length'] = '-'

        width = response.xpath(u'//td[contains(text(), "车宽")]/../td[2]/text()')
        if width:
            item['width'] = width.extract_first()
        else:
            item['width'] = '-'

        height = response.xpath(u'//td[contains(text(), "车高")]/../td[4]/text()')
        if height:
            item['height'] = height.extract_first()
        else:
            item['height'] = '-'

        gearnumber = response.xpath(u'//td[contains(text(), "档位数")]/../td[2]/text()')
        if gearnumber:
            item['gearnumber'] = gearnumber.extract_first()
        else:
            item['gearnumber'] = '-'

        weight = response.xpath(u'//td[contains(text(), "整备质量")]/../td[4]/text()')
        if weight:
            item['weight'] = weight.extract_first()
        else:
            item['weight'] = '-'

        wheelbase = response.xpath(u'//td[contains(text(), "轴距")]/../td[2]/text()')
        if wheelbase:
            item['wheelbase'] = wheelbase.extract_first()
        else:
            item['wheelbase'] = '-'

        lwv = response.xpath(u'//td[contains(text(), "气缸排列")]/../td[4]/text()')
        if lwv:
            item['lwv'] = lwv.extract_first()
        else:
            item['lwv'] = '-'

        lwvnumber = response.xpath(u'//td[contains(text(), "汽缸数")]/../td[2]/text()')
        if lwvnumber:
            item['lwvnumber'] = lwvnumber.extract_first()
        else:
            item['lwvnumber'] = '-'

        maxnm = response.xpath(u'//td[contains(text(), "最大扭矩")]/../td[4]/text()')
        if maxnm:
            item['maxnm'] = maxnm.extract_first()
        else:
            item['maxnm'] = '-'

        maxpower = response.xpath(u'//td[contains(text(), "最大功率")]/../td[4]/text()')
        if maxpower:
            item['maxpower'] = maxpower.extract_first()
        else:
            item['maxpower'] = '-'

        frontgauge = response.xpath(u'//td[contains(text(), "前轮距")]/../td[4]/text()')
        if frontgauge:
            item['frontgauge'] = frontgauge.extract_first()
        else:
            item['frontgauge'] = '-'

        compress = response.xpath(u'//td[contains(text(), "压缩比")]/../td[4]/text()')
        if compress:
            item['compress'] = compress.extract_first()
        else:
            item['compress'] = '-'

        yield item