# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import redis
from usedcar_new.items import GuaziItem
import time
import logging

website = 'auto51'


class Auto51Spider(scrapy.Spider):
    name = website

    # allowed_domains = ['auto51.com']
    # start_urls = ['http://auto51.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Auto51Spider, self).__init__(**kwargs)
        self.r = redis.Redis(host='192.168.1.92', db=4)
        self.cookie = self.r.get('auto51_cookie').decode('utf8')

        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            'Cookie': f'{self.cookie}'
        }
        print(self.headers)
        print("*" * 100)

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'auto51_online',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'auto51',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.GanjiPipeline': 300,
        },

    }

    def start_requests(self):
        url = "http://m.51auto.com/quanguo/pabmdcigf?ordering=publishTime&direction=2"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):
        x = response.xpath('//div[@class="carlist"]/a/@href').getall()
        if x:
            count = response.xpath("//div[@class='pagination_box']/div/div/span/text()").extract_first()
            count = int(re.findall("^1\/(.*?)$", count)[0])
            for i in range(count):
                pageNum = i + 1
                url = "http://m.51auto.com/quanguo/pabmdcigf?page=%d" % pageNum
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_list,
                    headers=self.headers
                )

    def parse_list(self, response):
        x = response.xpath('//div[@class="carlist"]/a')
        for temp in x:
            url = temp.xpath('@href').extract_first()
            # print(url)
            yield scrapy.Request(url, callback=self.parse_car, headers=self.headers)

    def parse_car(self, response):
        status = response.xpath('//div[@class="p-rel nocar-text"]')
        if status:
            status = "sold"
        else:
            status = "sale"
        price = response.xpath("//span[@class='price']/text()").get()
        datetime = "zero"

        # item loader
        item = GuaziItem()
        item['url'] = response.url
        item['grab_time'] = time.strftime('%Y-%m-%d %X', time.localtime())
        # item['website'] = website
        item['status'] = status
        item["statusplus"] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
        item['pagetime'] = datetime
        try:
            item["price1"] = price.replace('￥', '')
        except:
            pass
        # item['datasave'] = [response.xpath('//html').extract_first()]
        item["car_source"] = website
        item["parsetime"] = item['grab_time']
        item["carid"] = response.xpath("//input/@value").get()
        item["shortdesc"] = response.xpath('//div[@class="dt-car-title"]/span/text()').get()
        item["pagetitle"] = response.xpath('//title/text()').get()
        item["brand"] = response.xpath('//div[@class="breadcrumb"]/a[3]/text()').get()
        item["series"] = response.xpath('//div[@class="breadcrumb"]/a[4]/text()').get()
        makeyear = response.xpath('//div[@class="dt-car-title"]/span/text()').get()
        item["makeyear"] = re.findall('\d{4}', makeyear)[0] if re.findall('\d{4}', makeyear) else None
        item["registeryear"] = response.xpath('//div[@class="dt-car-base-info"]//li[2]/p/text()').get().split('-')[0]
        item["output"] = response.xpath('//p[contains(text(), "\u6392\u91cf")]/../p/text()').get()
        item["emission"] = response.xpath('//p[contains(text(),"\u6392\u653e\u6807\u51c6")]/../p/text()').get()
        item["generation"] = item["makeyear"]
        item["city"] = response.xpath('//meta[@name="location"]/@content').get().split(';')[1].replace('city=', '')
        item["prov"] = response.xpath('//meta[@name="location"]/@content').get().split(';')[0].replace('province=', '')
        item["contact_company"] = response.xpath('//div[@class="dt-seller-info"]//span/text()').get()
        item["contact_url"] = response.xpath('//div[@class="dt-seller-info"]//a/@href').get()
        item["carno"] = response.xpath('//p[contains(text(), "车源所有地")]/../p[1]/text()').get()
        item["desc"] = response.xpath('//p[@id="ds-infos"]/text()').get().replace(' ', '').replace('\n', '').replace(
            '\t', '')
        item["registerdate"] = response.xpath('//div[@class="dt-car-base-info"]//li[2]/p/text()').get()
        item["post_time"] = response.xpath('//div[@class="dt-car-con"]//p/span[3]/text()').get().replace('发布', '')
        item["mileage"] = response.xpath('//p[contains(text(),"公里")]/text()').get().replace(' ', '').replace('\n',
                                                                                                             '').replace(
            '\t', '').replace('万公里', '')

        # turn over
        gd = response.xpath("//a[@id='btn_carP']/span[contains('更多',text())]/text()").get()
        if gd:
            pz_url = response.xpath('//input[@id="vehiclefileinfo"]/@value').get()
            yield scrapy.Request(pz_url, meta={'meta1': item}, callback=self.parse_car2, headers=self.headers)
        else:
            yield item

    def parse_car2(self, response):
        """turn over, go on parse"""
        print(response.url)
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
        # print(item)
