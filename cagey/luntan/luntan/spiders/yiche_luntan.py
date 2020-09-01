# -*- coding: utf-8 -*-
import json
import re
import time
from copy import deepcopy

import scrapy
import string
import uuid

from luntan.items import YicheLuntanItem

website = 'yiche_luntan'


class YicheLuntanSpider(scrapy.Spider):
    name = website

    def __init__(self, *args, **kwargs):
        super(YicheLuntanSpider, self).__init__(**kwargs)
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        self.cookies = {"XCWEBLOG_testcookie": "yes"}
        self.num = 0

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'luntan',
        'MYSQL_TABLE': 'yiche_luntan',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'yiche_luntan',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        for i in list(string.ascii_uppercase):
            url = f'http://baa.bitauto.com/web_forum/api/pc/forum/getcarforums?&param=%7B"initial"%3A"{i}"%7D'
            yield scrapy.Request(
                url=url,
                headers=self.headers
            )

    def parse(self, response):
        data = json.loads(response.text)
        for i in data["data"]:
            item = YicheLuntanItem()
            item["brand"] = i["master"]
            print(i["master"])
            for s in i["forums"]:
                serise_id = s["id"]
                item["user_car"] = s["name"].replace("论坛", "")
                url = "http://baa.bitauto.com/" + s["forumApp"]
                # print(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_list_page,
                    meta={"item": item},
                    cookies=self.cookies,
                    headers=self.headers,
                )

    def parse_list_page(self, response):
        item = response.meta["item"]
        a_list = response.xpath("//div[@class='power-list-top list-theme']//div[@class='col-panel']/a")
        for a in a_list:
            item["url"] = "http://baa.bitauto.com" + a.xpath("./@href").get()
            item["user_name"] = a.xpath(".//div[@class='tz-item tz-user']/div[1]/text()").get().replace(" ", "").replace("\n", "")
            item["posted_time"] = a.xpath("./div[2]//div[2]//text()").get().replace(" ", "").replace("\n", "")
            item["title"] = a.xpath("./div[1]//span/text()").get().replace(" ", "")
            # item["reply_num"] = a.xpath(".//div[@class='tz-item-txt item-top repNum']/text()").get().replace(" ", "").replace("\n", "")
            tiezi_id = re.findall("\-(.*?)\.", item["url"])[0]
            detail_url = f'https://mapi.yiche.com/app_forum/api/post/get?param=%7B"postId"%3A"{tiezi_id}"%2C"isChoice"%3A"0"%2C"postType"%3A1%7D'
            # print(detail_url)
            # print(item)
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                meta={"item": deepcopy(item)},
            )
        next_page_url = response.xpath("//a[@class='link-btn next pg-item']/@href").get()
        if next_page_url:
            next_page = "http://baa.bitauto.com" + response.xpath("//a[@class='link-btn next pg-item']/@href").get()
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_list_page,
                cookies=self.cookies,
                headers=self.headers,
                meta={"item": item},
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        json_data = json.loads(response.text)["data"]
        if json_data:
            content_list = json_data["contentList"]
            message_list = []
            for i in content_list:
                message = i["message"].replace(" ", "").replace("\u3000", "")
                message_list.append(message)
            item["content"] = ",".join(message_list)
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["click_num"] = json_data["viewsNum"]
            item["reply_num"] = json_data["repliesNum"]
            item["statusplus"] = str(response.url+item["posted_time"])
            yield item
            # print(item)

