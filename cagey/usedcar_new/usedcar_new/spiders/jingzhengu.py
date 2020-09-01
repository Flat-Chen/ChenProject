# -*- coding: utf-8 -*-
import scrapy
import time
import json
from usedcar_new.items import GanjiItem
import re


class JingzhenguSpider(scrapy.Spider):
    name = 'jingzhengu'
    allowed_domains = ['buycar.jingzhengu.com']
    # start_urls = ['http://buycar.jingzhengu.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(JingzhenguSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'jingzhengu_online',
        'WEBSITE': 'jingzhengu',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'jingzhengu',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.GanjiPipeline': 300,
        },

    }

    def start_requests(self):
        url = "http://buycar.jingzhengu.com/ershouche/"
        yield scrapy.Request(
            url=url,
            dont_filter=True
        )

    def parse(self, response):
        # page_num = response.xpath("//p[@class='num-info']/em[2]/text()").get()
        page_num = response.xpath("//*[contains(text(),'共')]/following-sibling::em[1]/text()").get()
        for page in range(1, int(page_num)+1):
            list_url = f"http://buycar.jingzhengu.com/ershouche/o1-f1-w{page}/"
            print(list_url)
            # yield scrapy.Request(
            #     url=list_url,
            #     dont_filter=True,
            #     callback=self.parse_list_url
            # )

    def parse_list_url(self, response):
        li_div_list = response.xpath("//*[@id='zw_across_list_clearfix']/li")
        for li in li_div_list:
            detail_url = li.xpath(".//div[@class='zw_ac_tit']/a/@href").get()
            if detail_url:
                detail_url = response.urljoin(detail_url)
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail_url,
                )

    def parse_detail_url(self, response):
        item = GanjiItem()
        item["carid"] = re.findall("-(.*?).html", response.url)[0]
        item["shortdesc"] = response.xpath("//p[@class='w_cardescot_hed']/text()").get()
        item["price1"] = response.xpath("//p[@class='w_itemoffer_my']/span/text()").get().replace("¥", "").replace(" ", "").replace("\n", "").replace("\r", "")
        item["mileage"] = response.xpath("//p[contains(text(),'行驶里程')]/following-sibling::p/text()").get()
        # item["change_times"] = response.xpath("//li[@class='iNew-hu']//i/text()").get()
        item["car_source"] = 'jingzhengu'
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["parsetime"] = item["grab_time"]
        item["pagetitle"] = response.xpath("//title/text()").get().replace(" ", "").replace("\n", "").replace("\r", "")
        item["url"] = response.url
        item["brand"] = response.xpath("//div[@class='bread clearfix mt16']/a[2]//text()").get().split('二手')[1]
        item["series"] = response.xpath("//div[@class='bread clearfix mt16']/a[3]//text()").get().split('二手')[1][len(item["brand"]):]
        item["city"] = response.xpath("//p[contains(text(),'城市')]/following-sibling::p/text()").get()
        # print(item)
        output = response.xpath("//p[contains(text(),'排量')]/following-sibling::p/text()").get()
        item["output"] = re.findall("(.*?)L", output)[0]+'L' if output else None
        item["emission"] = re.findall("(\(.*?)\)", output)[0].replace("(", "") if output else None
        # item["guidepricetax"] = response.xpath("//p[contains(text(),'新车指导价')]/following-sibling::p/text()").get().replace("\n", "").replace(" ", "").replace("\r", "")
        item["registerdate"] = response.xpath("//p[contains(text(),'上牌时间')]/following-sibling::p/text()").get()
        item["post_time"] = response.xpath("//span[@class='w_carpr_titri']//text()").get().split('：')[1] if response.xpath("//span[@class='w_carpr_titri']//text()").get() else None
        item["modelname"] = response.xpath("//div[@class='w_cardetails']//input[@id='modelClassificationName']/@value").get()
        item["newcarid"] = response.xpath("//div[@class='w_cardetails']//input[@id='styleId']/@value").get()
        item["pagetime"] = 'zero'
        item["guideprice"] = response.xpath("//p[contains(text(),'新车指导价')]/following-sibling::p/text()").get().replace("\n", "").replace(" ", "").replace("\r", "")
        item["statusplus"] = item["carid"] + '-' + item["price1"]
        item["status"] = 'sale'
        # item["datasave"] = response.xpath('//html').get()
        # print(item)
        yield item

