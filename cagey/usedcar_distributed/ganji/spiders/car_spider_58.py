#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import Che58
import time
import logging
from ganji.spiders.SpiderInit import spider_original_Init


website ='che58'

# original
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["58.com"]
    # start_urls = [
    #     "http://www.58.com/ershouche/changecity/"
    # ]
    redis_key = 'che58'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 32,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/che58.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 5000000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'



    # region select
    def parse(self, response):
        print('111111111')
        sblist=['http://hk.58.com/ershouche/','http://am.58.com/ershouche/','http://tw.58.com/ershouche/','http://diaoyudao.58.com/','http://cn.58.com/ershouche/']
        urls = response.xpath('//dl[@id="clist"]/dd/a/@href').extract()
        urls = set(urls)
        for url in urls:
            if url not in sblist:
                yield scrapy.Request(url, self.select2_parse)

    def select2_parse(self, response):
        # print(response.body)
        for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
            url = str(href.xpath('a/@href').extract_first())
            datasave1 = href.extract()
            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.select2_parse)

    # get car info
    def parse_car(self, response):
        #count
        self.counts += 1
        logging.log(msg="download  " + str(self.counts) + "   items", level=logging.INFO)

        # error check
        if not("callback.58.com" in response.url):
            datasave1 = response.meta['datasave1']

            # key and status (sold or sale, price,time)
            status = response.xpath('//a[@class="btn_3"]')
            status = "sold" if status else "sale"

            price = response.xpath('//span[@class="jiage"]/text()')
            price = str(price.extract_first()) if price else "zero"

            datetime =response.xpath('//div[@class="posttime"]/span/text()')
            datetime ="-".join(datetime.re('\d+')) if datetime else "zero"

            #item loader
            item = Che58()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

            # turn over
            chexingId = response.xpath('//input[@id="chexingId"]/@value')

            if chexingId:
                url = 'http://escmse.58.com/carparam/detail?chexing={}&client=0'.format(chexingId.extract_first())
                yield scrapy.Request(url, meta={'meta1': item}, callback=self.parse_car2)

        else:
            logging.log(msg="Response.url:" + response.url +"-"+"Error" , level=logging.INFO)


    def parse_car2(self, response):
        """turn over, go on parse"""
        item = response.meta['meta1']
        # print response.body

        # extra
        fueltype = response.xpath(u'//td[contains(text(), "燃料形式")]/../td[2]/text()')
        if fueltype:
            item['fueltype'] = fueltype.extract_first()
        else:
            item['fueltype'] = '-'

        driverway = response.xpath(u'//td[contains(text(), "驱动方式")]/../td[6]/text()')
        if driverway:
            item['driverway'] = driverway.extract_first()
        else:
            item['driverway'] = '-'

        guideprice = response.xpath(u'//td[contains(text(), "厂商指导价")]/../td[6]/text()')
        if guideprice:
            item['guideprice'] = guideprice.extract_first() + u'万'
        else:
            item['guideprice'] = '-'

        doors = response.xpath(u'//td[contains(text(), "车门数")]/../td[4]/text()')
        if doors:
            item['doors'] = doors.extract_first()
        else:
            item['doors'] = '-'

        seats = response.xpath(u'//td[contains(text(), "车门数")]/../td[6]/text()')
        if seats:
            item['seats'] = seats.extract_first()
        else:
            item['seats'] = '-'

        size = response.xpath(u'//td[contains(text(), "宽")]/../td[6]/text()')
        if size:
            size = size.extract_first()
            item['length'] = size.split(u'×')[0]
            item['width'] = size.split(u'×')[1]
            item['height'] = size.split(u'×')[2]
        else:
            item['length'] = '-'
            item['width'] = '-'
            item['height'] = '-'

        gearnumber = response.xpath(u'//td[contains(text(), "挡位个数")]/../td[4]/text()')
        if gearnumber:
            item['gearnumber'] = gearnumber.extract_first()
        else:
            item['gearnumber'] = '-'

        gear = response.xpath(u'//td[contains(text(), "挡位个数")]/../td[6]/text()')
        if gear:
            item['gear'] = gear.extract_first()
        else:
            item['gear'] = '-'

        weight = response.xpath(u'//td[contains(text(), "整备")]/../td[2]/text()')
        if weight:
            item['weight'] = weight.extract_first()
        else:
            item['weight'] = '-'

        wheelbase = response.xpath(u'//td[contains(text(), "轴距")]/../td[4]/text()')
        if wheelbase:
            item['wheelbase'] = wheelbase.extract_first()
        else:
            item['wheelbase'] = '-'

        fuelnumber = response.xpath(u'//td[contains(text(), "燃油标记")]/../td[6]/text()')
        if fuelnumber:
            item['fuelnumber'] = fuelnumber.extract_first()
        else:
            item['fuelnumber'] = '-'

        lwv = response.xpath(u'//td[contains(text(), "汽缸数")]/../td[2]/text()')
        if lwv:
            item['lwv'] = lwv.extract_first()
        else:
            item['lwv'] = '-'

        lwvnumber = response.xpath(u'//td[contains(text(), "汽缸数")]/../td[6]/text()')
        if lwvnumber:
            item['lwvnumber'] = lwvnumber.extract_first()
        else:
            item['lwvnumber'] = '-'

        maxnm = response.xpath(u'//td[contains(text(), "最大扭矩")]/../td[6]/text()')
        if maxnm:
            item['maxnm'] = maxnm.extract_first()
        else:
            item['maxnm'] = '-'

        maxpower = response.xpath(u'//td[contains(text(), "最大功率")]/../td[2]/text()')
        if maxpower:
            item['maxpower'] = maxpower.extract_first()
        else:
            item['maxpower'] = '-'

        maxps = response.xpath(u'//td[contains(text(), "最大马力")]/../td[6]/text()')
        if maxps:
            item['maxps'] = maxps.extract_first()
        else:
            item['maxps'] = '-'

        frontgauge = response.xpath(u'//td[contains(text(), "前轮距")]/../td[6]/text()')
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
