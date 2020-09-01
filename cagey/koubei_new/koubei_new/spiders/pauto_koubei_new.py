# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei_new.items import PautoKoubeiItem
# from scrapy.conf import settings
import logging

website = 'pauto_koubei_new'


class PautoKoubeiNewSpider(scrapy.Spider):
    name = website

    # start_urls = ['http://price.pcauto.com.cn/cars/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(PautoKoubeiNewSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'public_opinion',
        'MYSQL_TABLE': 'pauto_koubei_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'koubei',
        'MONGODB_COLLECTION': 'pauto_koubei_new',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://price.pcauto.com.cn/cars/"
        yield scrapy.Request(
            url=url,
            dont_filter=True
        )

    def parse(self, response):
        # logging.log(msg="do the parse step",level=logging.INFO)
        # x=response.xpath('//div[@class="wrap iContent"]/div[@class="main clearfix"]/div[2]/div[@class="modA"]/div[2]/dl/dd/p[1]/a')
        x = response.xpath("//*[@class='tit']")
        for temp in x:
            urlbase = str(temp.xpath('./a/@href').extract_first())
            url = 'http://price.pcauto.com.cn/comment' + urlbase
            yield scrapy.Request(url, self.parse_main_info)

    def parse_main_info(self, response):
        # logging.log(msg="do the parse_main_info step",level=logging.INFO)
        item = PautoKoubeiItem()
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = response.url
        # item['website'] = website
        item['familyname'] = response.xpath('//div[@class="pos-mark"]/a[5]/text()').extract_first()
        item['familynameid'] = response.xpath('//div[@class="pos-mark"]/a[5]/@href').extract_first().replace("/", "")

        item['brand'] = response.xpath('//div[@class="pos-mark"]/a[3]/text()').extract_first()
        x = response.xpath('//div[@class="scollbody"]/div[@class="litDy clearfix"]')
        for temp in x:
            item['spec_id'] = temp.xpath('.//tr/td[1]/div/div[1]/div[2]/a/@href').get()[-6:-1]
            item['buyerid'] = temp.xpath('table/tr/td[1]/div/div[1]/div[1]/p/a/@href').re("\d+")[0]
            item['buyername'] = temp.xpath('table/tr/td[1]/div/div[1]/div[1]/p/a/text()').extract_first()
            for line in temp.xpath('table/tr/td[1]/div/div[1]/div[@class="line"]'):
                line_em = line.xpath("em/text()").extract_first()
                if line_em == "购买车型":
                    item['shortdesc'] = line.xpath('a/text()').extract_first()
                if line_em == "购买时间":
                    item['buy_date'] = line.xpath('text()').extract_first()
                if line_em == "购买地点":
                    item['buy_location'] = line.xpath('text()').extract_first()
                if line_em == "裸车价格":
                    item['buy_pure_price'] = line.xpath('i/text()').extract_first()
                if line_em == "行驶里程":
                    item['mileage'] = line.xpath('text()').extract_first().replace(u"公里", "")
                if line_em == "平均油耗":
                    item['oil_consume'] = line.xpath('i/text()').extract_first()

            score = temp.xpath('table/tr/td[1]/div/div[2]/script/text()').extract_first() if temp.xpath(
                'table/tr/td[1]/div/div[2]/script/text()') else temp.xpath(
                'table/tr/td[1]/div/div[3]/script/text()').extract_first()
            item['score'] = \
            re.findall("new Meter\(\{'id' : 'meter_table_\d+', 'score' : '(.*?)', 'bgColor' : 'g'\}\);", score)[0]
            labels = temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div')
            for label in labels:
                if label.xpath("b/text()").extract_first() == "外观：":
                    item['score_appearance_compare'] = label.xpath('span/text()').extract_first()
                if label.xpath("b/text()").extract_first() == "舒适：":
                    item['score_comfort_compare'] = label.xpath(
                        'span/text()').extract_first()
                if label.xpath("b/text()").extract_first() == "操控：":
                    item['score_control_compare'] = label.xpath(
                        'span/text()').extract_first()
                if label.xpath("b/text()").extract_first() == "油耗：":
                    item['score_fuel_compare'] = label.xpath(
                        'span/text()').extract_first()
                if label.xpath("b/text()").extract_first() == "动力：":
                    item['score_power_compare'] = label.xpath(
                        'span/text()').extract_first()
                if label.xpath("b/text()").extract_first() == "空间：":
                    item['score_space_compare'] = label.xpath(
                        'span/text()').extract_first()
                if label.xpath("b/text()").extract_first() == "内饰：":
                    item['score_trim_compare'] = label.xpath(
                        'span/text()').extract_first()

            item['satisfied'] = temp.xpath(
                'table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[1]/span/text()').extract_first()
            item['unsatisfied'] = temp.xpath(
                'table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[2]/span/text()').extract_first()

            # item['equipment']=temp.xpath('table/tr/td[2]/div/div[@class="dianPing clearfix"]/div[6]/span/text()').extract_first()

            item['score_appearance'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[1]/b/text()').extract_first()
            item['score_comfort'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[8]/b/text()').extract_first()
            item['score_control'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[6]/b/text()').extract_first()
            item['score_fuel'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[7]/b/text()').extract_first()
            item['score_power'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[5]/b/text()').extract_first()
            item['score_space'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[3]/b/text()').extract_first()
            item['score_trim'] = temp.xpath(
                'table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[2]/b/text()').extract_first()

            # item['score_equipment']=temp.xpath('table/tr/td[1]/div[1]/div[@class="fzbox"]/ul/li[4]/b/text()').extract_first()
            item['description'] = None
            item['visitCount'] = None
            item['helpfulCount'] = temp.xpath("//*[@class='good']/em/text()").extract_first().replace("(", "").replace(
                ")", "")
            item['commentCount'] = temp.xpath("//*[@class='huifu answer']/text()").re("\d+")[0]
            item['post_time'] = temp.xpath("table/tr/td[1]/div/div[1]/div[1]/span/a/text()").re("\d+\-\d+\-\d+")[0]
            # item['spec_id'] = None
            item['status'] = response.url + str(x.index(temp)) + "-" + str(item['visitCount']) + "-" + str(
                item['helpfulCount']) + "-" + str(item['commentCount'])
            # print(item)
            yield item

        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url = "http:" + str(next_page[1].extract())
            yield scrapy.Request(url, callback=self.parse_main_info, dont_filter=True)
