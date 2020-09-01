# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import os
import random
import requests

from luntan.items import LuntanItem
from fontTools.ttLib import TTFont
from luntan.font import get_be_p1_list, get_map

from scrapy_redis.spiders import RedisSpider

website = "autohome_luntan"


class AutohomeLuntanSpider(RedisSpider):
# class AutohomeLuntanSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['autohome.com']
    # start_urls = ["https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter"]

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeLuntanSpider, self).__init__(**kwargs)
        self.counts = 0
        self.word_list = ['呢', '近', '八', '着', '更', '短', '三', '少', '是', '大', '好', '上', '十', '低', '不', '的', '六', '很', '坏', '长', '右', '高', '四', '五', '一', '二', '了', '下', '左', '得', '多', '远', '七', '九', '地', '小', '和', '矮']
        self.font_map = {}
        self.headers = {'Referer': 'https://club.autohome.com.cn/',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        self.be_p1 = get_be_p1_list()

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'luntan',
        'MYSQL_TABLE': 'autohome_luntan_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'autohome_luntan',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES': {
           # 'luntan.middlewares.SeleniumMiddleware': 543,
           'luntan.middlewares.RotateUserAgentMiddleware': 542,
        }
    }

    def start_requests(self):
        url = "https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter"
        yield scrapy.Request(
            url=url,
            headers=self.headers
        )

    # 实现翻页，并且进入下一个循环
    def parse(self, response):
        car_url_dict = json.loads(response.text)["result"]
        random.shuffle(car_url_dict)
        for car_url_list in car_url_dict:
            car_urls = car_url_list["bbsBrand"]
            for car_url in car_urls:
                brand = car_url["bbsBrandName"]
                bbslit = car_url["bbsList"]
                for car in bbslit:
                    car_id = car["bbsId"]
                    user_car = car["bbsName"]
                    meta = {
                        "id": car_id,
                        "user_car": user_car,
                        "brand": brand
                    }
                    url = "https://club.autohome.com.cn/frontapi/topics/getByBbsId?pageindex=1&pagesize=100&bbs=c&bbsid={}&fields=topicid%2Ctitle%2Cpost_memberid%2Cpost_membername%2Cpostdate%2Cispoll%2Cispic%2Cisrefine%2Creplycount%2Cviewcount%2Cvideoid%2Cisvideo%2Cvideoinfo%2Cqainfo%2Ctags%2Ctopictype%2Cimgs%2Cjximgs%2Curl%2Cpiccount%2Cisjingxuan%2Cissolve%2Cliveid%2Clivecover%2Ctopicimgs&orderby=topicid-".format(car_id)
                    # eg: "https://club.autohome.com.cn/frontapi/topics/getByBbsId?pageindex=1&pagesize=100&bbs=c&bbsid=3237&fields=topicid%2Ctitle%2Cpost_memberid%2Cpost_membername%2Cpostdate%2Cispoll%2Cispic%2Cisrefine%2Creplycount%2Cviewcount%2Cvideoid%2Cisvideo%2Cvideoinfo%2Cqainfo%2Ctags%2Ctopictype%2Cimgs%2Cjximgs%2Curl%2Cpiccount%2Cisjingxuan%2Cissolve%2Cliveid%2Clivecover%2Ctopicimgs&orderby=topicid-"
                    yield scrapy.Request(
                        url=url,
                        callback=self.page_num,
                        meta=meta,
                        headers=self.headers,
                        dont_filter=True
                    )

    def page_num(self, response):
        pinglun_url_dict = json.loads(response.text)
        if pinglun_url_dict['result']:
            pagecount = pinglun_url_dict['result']["pagecount"]
            # 只能拿到前1000页的数据
            pagecount = 999 if pagecount > 1000 else pagecount
            for next_page_num in range(1, pagecount+1):
                url = f"https://club.autohome.com.cn/frontapi/topics/getByBbsId?pageindex={next_page_num}&pagesize=100&bbs=c&bbsid={response.meta['id']}&fields=topicid%2Ctitle%2Cpost_memberid%2Cpost_membername%2Cpostdate%2Cispoll%2Cispic%2Cisrefine%2Creplycount%2Cviewcount%2Cvideoid%2Cisvideo%2Cvideoinfo%2Cqainfo%2Ctags%2Ctopictype%2Cimgs%2Cjximgs%2Curl%2Cpiccount%2Cisjingxuan%2Cissolve%2Cliveid%2Clivecover%2Ctopicimgs&orderby=topicid-"
                yield scrapy.Request(
                    url=url,
                    callback=self.page_turning,
                    meta=response.meta,
                    headers=self.headers
                )

    def page_turning(self, response):
        pinglun_url_dict = json.loads(response.text)
        if pinglun_url_dict["result"]:
            for pinglun_url in pinglun_url_dict["result"]["list"]:
                l_list = pinglun_url["url"].split('bbs')
                # 老页面url
                url = l_list[0]+'o/bbs'+l_list[1]
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_luntan,
                    headers=self.headers,
                    meta=response.meta
                )

    def parse_luntan(self, response):
        item = LuntanItem()
        item["information_source"] = website
        item["brand"] = response.meta["brand"]
        title = response.xpath("//div[@class='maxtitle']/text()").get()
        if title:
            item["title"] = title
        else:
            item["title"] = response.xpath("//div[@id='consnav']/span[4]/text()").get()
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content_list = response.xpath("//div[@class='conttxt']")
        content_list = content_list.xpath("string(.)").getall()
        item["content"] = "".join(content_list).replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', '')
        item["url"] = response.url
        item["user_name"] = response.xpath("//a[@xname='uname']/text()").get().replace(' ', '').replace('\r', '').replace('\n', '')
        item["posted_time"] = response.xpath("//span[@xname='date']/text()").get()
        item["user_car"] = response.xpath("//div[@id='consnav']/span[2]/a/text()").get().strip("论坛")
        province = response.xpath("//ul[@class='leftlist']/li[6]/a/text()").get()
        if province:
            province = province.split()
            if len(province) == 2:
                item["province"] = province[0]
                item["region"] = province[1]
            else:
                item["province"] = province[0]
                item["region"] = None
        try:
            tieziid = re.findall(r"/(\d*)-1.html", response.url)[0]
        except:
            item["click_num"] = 0
        else:
            item["click_num"] = self.get_click_num(tieziid)
        item["reply_num"] = response.xpath("//font[@id='x-replys']/text()").get()
        item["content_num"] = response.xpath("//a[@title='查看']/text()").get().split("帖")[0]
        # # 处理content
        TFF_text_url = response.xpath("//style[@type='text/css']/text()").get()
        url = re.findall(r"format\('embedded-opentype'\),url\('(.*?)'\) format\('woff'\)", TFF_text_url)
        if url:
            font_map = self.text_ttf("https:" + url[0]) if "k3.autoimg.cn" in url[0] else self.text_ttf("https://k3.autoimg.cn" + url[0])
            if font_map:
                for font in font_map:
                    old = (r"\u" + font["key"].strip("uni").lower())
                    item["content"] = re.sub(old, font["value"], item["content"])
                    # print(item)
            else:
                print("*"*100)
                print(item["content"])
        else:
            print("-" * 100)
            print(item["content"])

        item["statusplus"] = str(item["url"]) + str(item["posted_time"])
        # print(item)
        # print(item)
        yield item
        

    def text_ttf(self, url):
        User_Agent = self.headers
        try:
            text = requests.get(url=url, headers=User_Agent)
        except:
            return 0
        else:
            path = os.path.abspath('./')
            with open(path+"/luntan/tools/text2.ttf", "bw")as f:
                f.write(text.content)
            font = TTFont(path+"/luntan/tools/text2.ttf")
            font.saveXML(path+"/luntan/tools/text2.xml")
            font_map = get_map(self.be_p1, self.word_list)
            return font_map

    def get_click_num(self, data):
        url = "https://clubajax.autohome.com.cn/Detail/LoadX_Mini?topicId={}".format(data)
        text = requests.get(url=url, headers=self.headers).json()
        try:
            a = text["topicClicks"]["Views"]
        except:
            a = 0
        return a