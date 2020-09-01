# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import copy
from luntan.items import LuntanItem

# from scrapy_redis.spiders import RedisSpider

website = 'pcauto_luntan'


# class PcautoLuntanSpider(RedisSpider):
class PcautoLuntanSpider(scrapy.Spider):
    name = website

    # allowed_domains = ['pcauto.com']
    start_urls = ['http://www.pcauto.com.cn/forum/sitemap/pp/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(PcautoLuntanSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'Referer': 'https://bbs.pcauto.com.cn',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            # "Cookie": "visitedfid=17957D20685D22418D20697D23985D23585D17913D17608D17504D17329",
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'luntan',
        'MYSQL_TABLE': 'pcauto_luntan_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'pcauto_luntan',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES': {
            'luntan.middlewares.ProxyMiddleware': 543,
            # 'luntan.middlewares.RotateUserAgentMiddleware': 542,
        }

    }

    # def start_requests(self):
    #     url = "http://www.pcauto.com.cn/forum/sitemap/pp/"
    #     yield scrapy.Request(
    #         url=url,
    #         headers=self.headers,
    #         dont_filter=True
    #     )

    def parse(self, response):
        print('执行parse函数')
        tr_list = response.xpath("//td[@class='tdCon']/..")
        for tr in tr_list:
            brand = tr.xpath(".//td[@class='tdTit']/i/text()").get()
            brand_url = tr.xpath(".//a[@class='hei']/@href").getall()
            print(brand_url, 'brand_url')
            if brand_url:
                for url in brand_url:
                    forumId = re.findall('forum-(.*?).html', url)[0]
                    json_url = f"https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/bbs/forums.xsp?forumId={forumId}&pageNo=1&pageSize=20"
                    print(json_url, '第一个url')
                    yield scrapy.Request(
                        url=json_url,
                        callback=self.brand_parse,
                        headers=self.headers,
                        meta={"brand": brand, "forumId": forumId},
                        dont_filter=True
                    )

    def brand_parse(self, response):
        print('执行brand_parse函数')
        forumId = response.meta["forumId"]
        json_data = json.loads(response.text)
        data_num = int(json_data["total"])
        print(data_num, 'data_num')
        for page_num in range(1, int(data_num / 20) + 1):
            print(page_num, 'page_num')
            json_url = f"https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/bbs/forums.xsp?forumId={forumId}&pageNo={page_num}&pageSize=20"
            yield scrapy.Request(
                url=json_url,
                headers=self.headers,
                callback=self.parse_list_url_new,
                meta=response.meta,
                dont_filter=True
            )

    def parse_list_url_new(self, response):
        print('执行parse_list_url函数')
        print('这是倒数第二的url', response.url)
        pass
        # json_data = json.loads(response.text)
        # data_list = json_data["topicList"]
        # for data in data_list:
        #     item = LuntanItem()
        #     item["brand"] = response.meta["brand"]
        #     item["title"] = data["title"]
        #     item["reply_num"] = data["replyCount"]
        #     # item["content_num"] = data["view"]
        #     item["click_num"] = data["view"]
        #     item["information_source"] = website
        #     item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     item["user_name"] = data["author"]["name"]
        #     item["region"] = data["author"]["cityName"] if data["author"]["cityName"] else None
        #     createAt = data["createAt"]
        #     item["posted_time"] = deal_time(createAt)
        #     topicId = data["topicId"]
        #     datail_url = f"https://magear.pcauto.com.cn/p/bbs.pcauto.com.cn/wxapi/1/topic.do?tid={topicId}"
        # yield scrapy.Request(
        #     url=datail_url,
        #     headers=self.headers,
        #     callback=self.parse_detail_url,
        #     meta={"item": copy.deepcopy(item)}
        # )

    # def parse_detail_url(self, response):
    #     print('这是最后的url', response.url)
    #     item = response.meta["item"]
    #     json_data = json.loads(response.text)
    #     data = json_data["data"]
    #     content_list = data["content"]
    #     txt_list = list()
    #     for content in content_list:
    #         if content["type"] == 2:
    #             txt_list.append(content["txt"])
    #     contents = "".join(txt_list).replace('&nbsp', '').replace(' ', '').replace('\u3000', '').replace('<br/>',
    #                                                                                                      '').replace(
    #         '\t', '').replace(';', '')
    #     item["content"] = contents
    #     item = response.meta["item"]
    #     item["url"] = response.url
    #     item["user_car"] = data["forumName"].replace("论坛", "")
    #     item["statusplus"] = str(item["user_name"]) + str(item["title"]) + str(item["posted_time"]) + str(
    #         item["brand"]) + str(item["reply_num"])
    #     print(item)
    #     # yield item


def deal_time(sold_time):
    timeStamp = sold_time / 1000
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime, '这是otherStyleTime')
    return otherStyleTime
