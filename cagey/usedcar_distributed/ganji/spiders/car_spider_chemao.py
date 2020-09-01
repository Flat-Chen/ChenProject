#-*- coding: UTF-8 -*-
from lxml import etree
import redis
import requests
import scrapy
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy_redis.spiders import RedisSpider
from ganji.items import CheMao
import time
from ganji.spiders.SpiderInit import spider_original_Init
redis_client2 = redis.Redis(settings['REDIS_SERVER'], port=6379, db=settings['REDIS_DB'])

website ='chemao'

# main
class CarSpider(RedisSpider):
    # basesetting
    name = website
    allowed_domains = ["chemao.com"]
    # start_urls = ["https://www.chemao.com/", ]
    redis_key = 'chemao'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 1.5,
        # 'CONCURRENT_REQUESTS': 2,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        # "RETRY_TIMES": 4,
        'DOWNLOAD_TIMEOUT': 600,


        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/chemao.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 3000000
        self.counts = 0
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'

    def parse(self, response):
        # is exist
        sorry = response.xpath('//p[@class="sorry"]/text()').extract()
        if sorry:
            redis_client2.lrem('chemao', response.url)
            print('sorry page, del the url----------', response.url)
            return

        for href in response.xpath('//div[@id="carPicList"]/div[@class="list"]'):
            urlbase = href.xpath("./div/a/@href").extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, callback=self.parse_car, dont_filter=True)

        # next page
        next_page = response.xpath('//a[@class="page-next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)

    # get car info
    def parse_car(self, response):
        status = response.xpath('//div[@class="shelf-wram"] | //div[@class="car-status"]')
        if status:
            status = "sold"
            price = ".".join(response.xpath('//span[@class="p"]/text()').re('\d+'))
        else:
            status = "sale"
            price = ".".join(response.xpath('//span[@class="s4"]/text()').re('\d+'))

        datetime = response.xpath('//span[@class="Tahoma"]/text()').extract_first()

        # item loader
        item = CheMao()
        if response.xpath('//*[@id="det_title"]/text()'):
            trade_id = response.xpath('//input[@id="trade_id"]/@value').extract_first()
            url = 'https://www.chemao.com/index.php?app=show&act=show_more&id=' + trade_id
            res = requests.get(url)
            print(res.status_code)
            html = etree.HTML(res.content.decode('gb2312'))
            # print res.content.decode('gb2312')

            # extra
            body = html.xpath(u'//td[contains(text(), "车身型式")]/../td[2]/text()')
            if body:
                item['body'] = body[0].strip()
            else:
                item['body'] = '-'

            bodystyle = html.xpath(u'//td[contains(text(), "车身型式")]/../td[2]/text()')
            if bodystyle:
                if len(bodystyle[0].split(u'座')) > 1:
                    item['bodystyle'] = bodystyle[0].split(u'座')[1].strip()
                else:
                    item['bodystyle'] = '-'
            else:
                item['bodystyle'] = '-'

            gear = html.xpath(u'//td[text()="变速箱"]/../td[2]/text()')
            if gear:
                item['gear'] = gear[0].strip()
            else:
                item['gear'] = '-'

            gearnumber = html.xpath(u'//td[contains(text(), "档位数")]/../td[2]/text()')
            if gearnumber:
                item['gearnumber'] = gearnumber[0].strip()
            else:
                item['gearnumber'] = '-'

            doors = html.xpath(u'//td[contains(text(), "车身型式")]/../td[2]/text()')
            if doors:
                if len(doors[0].split(u'门')) > 1:
                    item['doors'] = doors[0].split(u'门')[0].strip()
                else:
                    item['doors'] = '-'
            else:
                item['doors'] = '-'

            seats = html.xpath(u'//td[contains(text(), "车身型式")]/../td[2]/text()')
            if seats:
                if len(seats[0].split(u'门')) > 1:
                    item['seats'] = seats[0].split(u'门')[1][0]
                else:
                    item['seats'] = '-'
            else:
                item['seats'] = '-'

            size = html.xpath(u'//td[contains(text(), "长宽高")]/../td[2]/text()')
            if size:
                temp = size[0].split('*')
                if len(temp) == 3:
                    item['length'] = temp[0]
                    item['width'] = temp[1]
                    item['height'] = temp[2]
                else:
                    item['length'] = '-'
                    item['width'] = '-'
                    item['height'] = '-'
            else:
                item['length'] = '-'
                item['width'] = '-'
                item['height'] = '-'

            fueltype = html.xpath(u'//td[contains(text(), "燃料类型")]/../td[2]/text()')
            if fueltype:
                item['fueltype'] = fueltype[0]
            else:
                item['fueltype'] = '-'

            fuelnumber = html.xpath(u'//td[contains(text(), "燃料标号")]/../td[2]/text()')
            if fuelnumber:
                item['fuelnumber'] = fuelnumber[0]
            else:
                item['fuelnumber'] = '-'

            maxnm = html.xpath(u'//td[contains(text(), "最大扭矩")]/../td[2]/text()')
            if maxnm:
                item['maxnm'] = maxnm[0]
            else:
                item['maxnm'] = '-'

            maxpower = html.xpath(u'//td[contains(text(), "最大功率")]/../td[2]/text()')
            if maxpower:
                item['maxpower'] = maxpower[0]
            else:
                item['maxpower'] = '-'

            maxps = html.xpath(u'//td[contains(text(), "最大马力")]/../td[2]/text()')
            if maxps:
                item['maxps'] = maxps[0]
            else:
                item['maxps'] = '-'

            lwv = html.xpath(u'//td[contains(text(), "气缸排列形式")]/../td[2]/text()')
            if lwv:
                item['lwv'] = lwv[0]
            else:
                item['lwv'] = '-'

            lwvnumber = html.xpath(u'//td[contains(text(), "气缸数")]/../td[2]/text()')
            if lwvnumber:
                item['lwvnumber'] = lwvnumber[0]
            else:
                item['lwvnumber'] = '-'

            compress = html.xpath(u'//td[contains(text(), "压缩比")]/../td[2]/text()')
            if compress:
                item['compress'] = compress[0]
            else:
                item['compress'] = '-'

            driverway = html.xpath(u'//td[contains(text(), "驱动方式")]/../td[2]/text()')
            if driverway:
                item['driverway'] = driverway[0]
            else:
                item['driverway'] = '-'


        else:

            item['body'] = '-'

            item['bodystyle'] = '-'

            item['gear'] = '-'

            item['gearnumber'] = '-'

            item['doors'] = '-'

            item['seats'] = '-'

            item['length'] = '-'
            item['width'] = '-'
            item['height'] = '-'

            item['fueltype'] = '-'

            fuelnumber = response.xpath(u'//dt[contains(text(),"燃油标号")]/../dd/text()')
            if fuelnumber:
                item['fuelnumber'] = fuelnumber.extract_first()
            else:
                item['fuelnumber'] = '-'

            item['maxnm'] = '-'

            item['maxpower'] = '-'

            item['maxps'] = '-'

            item['lwv'] = '-'

            item['lwvnumber'] = '-'

            item['compress'] = '-'

            driverway = response.xpath(u'//dt[contains(text(), "驱动方式")]/../dd/text()')
            if driverway:
                item['driverway'] = driverway.extract_first()
            else:
                item['driverway'] = '-'

        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
        item['pagetime'] = datetime
        item['datasave'] = [response.xpath('//html').extract_first()]

        yield item