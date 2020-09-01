# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from copy import deepcopy
from luntan.items import LuntanItem

website = "xcar_luntan"


class XcarLuntanSpider(scrapy.Spider):
    name = website

    # allowed_domains = ['xcar.com']
    # start_urls = ['http://xcar.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XcarLuntanSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {'Referer': 'http://www.xcar.com.cn',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'luntan',
        'MYSQL_TABLE': 'xcar_luntan_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'xcar_luntan',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        start_urls = "http://www.xcar.com.cn/bbs/"
        yield scrapy.Request(
            url=start_urls,
            headers=self.headers
        )

    # 实现翻页，并且进入下一个循环
    def parse(self, response):
        tr_list = response.xpath("//table//tbody/tr")
        for tr in tr_list:
            # 车系的名字
            brand = tr.xpath(".//td/a/text()").get()

            luntan_url_list = tr.xpath(".//div[@class='t1203_fbox']//a/@href").getall()
            luntan_name = tr.xpath(".//div[@class='t1203_fbox']//a/text()").getall()
            luntan_dic = dict(zip(luntan_name, luntan_url_list))
            if luntan_url_list:

                for luntan_name, luntan_url in luntan_dic.items():
                    luntan_url = response.urljoin(luntan_url)
                    fid_id = luntan_url.split('=')[-1]
                    url = f"http://www.xcar.com.cn/bbs/xbbsapi/forumdisplay/get_thread_list.php?fid={fid_id}&orderby=lastpost&filter=&ondigest=0&page=1"
                    meta = {
                        "user_car": luntan_name,
                        "page": 1,
                        "fid_id": fid_id,
                        "brand": brand
                    }
                    yield scrapy.Request(
                        url=url,
                        headers=self.headers,
                        meta=meta,
                        callback=self.get_luntan
                    )

    # 翻页操作 并进入下一个页面
    def get_luntan(self, response):
        json_data = json.loads(response.text)
        data = json_data["data"]["data"]
        if data["thread_list"]:
            for t in data["thread_list"]:
                tid = t["tid"]
                item = LuntanItem()
                item["information_source"] = website
                item["brand"] = response.meta["brand"]
                item["title"] = t["subject"]
                item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["content"] = t["description"]
                item["user_name"] = t["author"]
                item["posted_time"] = t["dateline"]
                item["user_car"] = response.meta["user_car"].strip("论坛")
                click_num = str(t["views"])
                click_num = str(int(float(click_num.replace('w+', '')) * 10000)) if 'w' in click_num else click_num
                item["click_num"] = click_num
                item["reply_num"] = t["replies"]
                item["content_num"] = click_num
                url = f"http://www.xcar.com.cn/bbs/viewthread.php?tid={tid}"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_detail_url,
                    headers=self.headers,
                    meta={"item": deepcopy(item)}
                )
            response.meta["page"] += 1
            next_url = f'http://www.xcar.com.cn/bbs/xbbsapi/forumdisplay/get_thread_list.php?fid={response.meta["fid_id"]}&orderby=lastpost&filter=&ondigest=0&page={response.meta["page"]}'
            yield scrapy.Request(
                url=next_url,
                callback=self.get_luntan,
                headers=self.headers,
                meta=response.meta
            )
        else:
            pass

    def parse_detail_url(self, response):
        item = response.meta["item"]
        item["url"] = response.url
        item["province"] = response.xpath("//div[@class='clearfix place']/span[2]/text()").get()
        item["region"] = response.xpath("//div[@class='clearfix place']/span[3]/text()").get()
        item["statusplus"] = str(item["user_name"]) + str(item["title"]) + str(item["posted_time"]) + str(
            item["province"]) + str(item["brand"])

        # print(item)
        yield item
