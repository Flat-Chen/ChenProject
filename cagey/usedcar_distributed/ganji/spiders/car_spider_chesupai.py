# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy_redis.spiders import RedisSpider
from ganji.items import CheSuPai
import time
import logging
# from spiders.SpiderInit import spider_original_Init
from ganji.spiders.SpiderInit import spider_original_Init

website ='carsupai'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["carsupai.cn"]
    # start_urls = [ "https://www.chesupai.cn/list/sh/", ]
    redis_key = 'carsupai'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/carsupai.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 1500000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    # city select
    def parse(self, response):
        for href in response.xpath('//div[@class="city-all"]/dl[not(@class="c-fore1")]/dd/a/@href').extract():
            city = re.findall(r'domain=(.*?)&', href)[0]
            url = "https://www.chesupai.cn/list/" + city + "/"
            yield scrapy.Request(url, callback=self.select1_parse)

    # car select
    def select1_parse(self, response):
        # print response.url
        # car select
        for href in response.xpath('//ul[@class="gzp-list clearfix"]/li'):
            urlbase = href.xpath("./a/@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"datasave1":datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.select1_parse)

    # get car info
    def parse_car(self, response):
        # print response.body

        # status check
        if response.status==200:
            # count
            self.counts += 1
            logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

            # key and status (sold or sale, price,time)
            status='sale'

            price = response.xpath('//li[@id="current_price_tip"]/span[@class="s-price"]/text()[2]')
            price = price.extract_first() if price else "zero"
            pagetime = "zero"

            # datasave
            if 'datasave1' in response.meta:
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # extra
            accident_desc = ''
            name1 = response.xpath('//div[@class="detectBox clearfix"][1]//td/span[contains(@class, "fc-orange")]/../preceding-sibling::td[1]/text()').extract()
            desc1 = response.xpath('//div[@class="detectBox clearfix"][1]//td/span[contains(@class, "fc-orange")]/text()').extract()
            relt1 = zip(name1, desc1)
            for relt in relt1:
                accident_desc += ''.join(relt) + '/'

            outer_desc = ''
            points = response.xpath('//div[@class="outward fl"]//div[@class="appearance-det"]')
            temp = ['hood', 'fender_fr', 'door_fr', 'door_rr', 'fender_rr', 'trunk_lid',
                    'fender_rl', 'door_rl', 'foot_save', 'door_fl', 'head_save', 'fender_fl', 'roof']
            for point in points:
                position_num = int(point.xpath('./i/text()').extract_first())
                position = temp[position_num]
                desc2 = point.xpath('.//p/text()').extract_first()
                outer_desc += position + ': ' + desc2.strip() + ';'

            safe_desc = ''
            name3 = response.xpath(
                '//div[@class="detectBox clearfix"][4]//td/span[contains(@class, "fc-orange")]/../preceding-sibling::td[1]/text()').extract()
            desc3 = response.xpath(
                '//div[@class="detectBox clearfix"][4]//td/span[contains(@class, "fc-orange")]/text()').extract()
            relt3 = zip(name3, desc3)
            for relt in relt3:
                safe_desc += ''.join(relt) + '/'

            road_desc = ''
            name4 = response.xpath(
                '//div[@class="detectBox clearfix"][position()>4]//td/span[contains(@class, "fc-orange")]/../preceding-sibling::td[1]/text()').extract()
            desc4 = response.xpath(
                '//div[@class="detectBox clearfix"][position()>4]//td/span[contains(@class, "fc-orange")]/text()').extract()
            relt4 = zip(name4, desc4)
            for relt in relt4:
                road_desc += ''.join(relt) + '/'

            # item loader
            item = CheSuPai()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url + "-" + str(price.strip()) + "-" + str(status)+"-" + pagetime
            item['pagetime'] = pagetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

            #  extra
            item['accident_desc'] = accident_desc
            item['outer_desc'] = outer_desc
            item['safe_desc'] = safe_desc
            item['road_desc'] = road_desc

            # yield item
            print(item)