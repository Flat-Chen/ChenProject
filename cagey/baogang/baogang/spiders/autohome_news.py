# -*- coding: utf-8 -*-
import re
import scrapy
import time
import json
import random
import hashlib
from lxml import etree
from baogang.items import NewsItem


class AutohomeNewsSpider(scrapy.Spider):
    name = 'autohome_news'
    # allowed_domains = ['autohome.com']
    # start_urls = ['http://autohome.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeNewsSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '180.167.80.118',
        'MYSQL_DB': 'baogang',
        'MYSQL_TABLE': 'baogang_news',
        'MYSQL_PORT': 2502,
        'MYSQL_PWD': 'Baogang@2019',
        'MONGODB_SERVER': '180.167.80.118',
        'MONGODB_DB': 'baogang',
        'MONGODB_COLLECTION': 'baogang_news',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0"
        yield scrapy.Request(
            url=url,
        )

    def parse(self, response):
        html_str = response.text.replace('document.writeln("', '').replace('");', '')
        res = etree.fromstring("<root>" + html_str.strip() + "</root>")
        lis = res.xpath("//li")
        for li in lis:
            meta = {
                "brandname": li.xpath("h3/a/text()")[0],
                "brandid": li.xpath("@id")[0].replace("b", "")
            }
            url = li.xpath("h3/a/@href")[0]
            url = response.urljoin(url)
            # eg: 'https://car.autohome.com.cn/price/brand-275.html'
            # print(url)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_fnf)

    def parse_fnf(self, response):
        dls = response.xpath("//*[@class='list-dl']")
        for dl in dls:
            factoryname = dl.xpath("dt/a/text()").extract_first()
            # self.nationp["factoryname"] = factoryname
            furl = dl.xpath("dt/a/@href").extract_first()
            factoryid = re.findall("\-(\d+)\.html", furl)[0]

            family_list = dl.xpath("dd/div[@class='list-dl-text']/a")
            for family in family_list:
                familyname = family.xpath("text()").extract_first()
                family_url = family.xpath("@href").extract_first()
                familyid = re.findall("series\-(\d+)[\-\.].*?html", family_url)[0]
                seriesid = re.findall("pvareaid=(\d+)", family_url)[0]
                meta = {
                    "factoryname": factoryname,
                    "factoryid": factoryid,
                    "familyname": familyname.replace(u" (停售)", ""),
                    "familyid": familyid,
                    "seriesid": seriesid
                }
                news_url = f"https://www.autohome.com.cn/{familyid}/1/0-0-1-0/#pvareaid={seriesid}"
                yield scrapy.Request(
                    url=news_url,
                    meta=dict(meta, **response.meta),
                    callback=self.parse_news_list
                )

    def parse_news_list(self, response):
        meta = response.meta
        item = NewsItem()
        li_list = response.xpath("//div[@class='cont-info']/ul/li")
        b = response.xpath("//div[@class='subnav-title-name']/a/text()").get().split('-')
        item["brand"] = b[0]
        item["series"] = b[1]
        for li in li_list:
            item["title"] = li.xpath("./h3/a/text()").get()
            item["url"] = response.urljoin(li.xpath("./h3/a/@href").get())
            item["postd_date"] = li.xpath("./p[@class='name-tx']/span[2]/text()").get()
            item["view_num"] = li.xpath("./p[@class='name-tx']/span[3]//text()").get()
            item["reply_num"] = li.xpath("./p[@class='name-tx']/span[4]//text()").get()
            item["label"] = li.xpath("./p[@class='car']/a/text()").get()
            item["data_source"] = "汽车之家"
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(item)
            yield item

        next_url = response.xpath("//a[@class='page-item-next']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_news_list,
                meta=meta
            )
