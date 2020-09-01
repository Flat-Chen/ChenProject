# -*- coding: utf-8 -*-
import io
import json
import re
from copy import deepcopy

import scrapy
from PIL import Image
import pytesseract

from baogang.items import BaogangItem
# from urllib3.util import retry
import time
import requests
# from requests.adapters import HTTPAdapter
from scrapy_redis.spiders import RedisSpider

website = 'feijiu_url'


# class FeijiuSpider(RedisSpider):
class FeijiuSpider(scrapy.Spider):
    name = website

    # allowed_domains = ['feijiu.net']
    # redis_key = "feijiu:start_urls"
    # url = "http://www.feijiu.net/FeiJinShu/"
    # start_urls = ['http://feijiu.net/',]

    def __init__(self):
        super(FeijiuSpider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.count = 0

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'MONGODB_SERVER': '127.0.0.1',
        # 'MONGODB_PORT': 27017,
        'MONGODB_COLLECTION': 'feijiu_fz',
        'MONGODB_DB': 'baogang',
        'CrawlCar_Num': 1000000,
        # 'CONCURRENT_REQUESTS': 6,
        # 'AUTOTHROTTLE_ENABLED': True,
        # 起始的延迟
        'AUTOTHROTTLE_START_DELAY': 32,
        # 最小延迟
        'DOWNLOAD_DELAY': 0,
        # 最大延迟
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        # 'DOWNLOAD_TIMEOUT': 20,
        # 'RETRY_ENABLED': True,
        # 'RETRY_TIMES': 10,
        # 'DOWNLOAD_FAIL_ON_DATALOSS': True,
    }

    def start_requests(self):
        url = "http://www.feijiu.net/FeiZhi/"
        return [scrapy.Request(url=url, dont_filter=True, headers=self.headers)]

    def parse(self, response):
        class_url_list = response.xpath("//div[@class='hy_title']/ul/li/a/@href").getall()
        # class_url_list = ["http://www.feijiu.net/FeiZhi/"]
        for url in class_url_list:
            yield scrapy.Request(
                url=url,
                callback=self.get_last_url,
                dont_filter=True,
                headers=self.headers
            )

    # def get_lable_one_url(self, response):
    #     lable_one_url_list = response.xpath("//*[@class='hy']/div[2]//a/@href").getall()
    #     for lable_one in lable_one_url_list:
    #         if '#' not in lable_one:
    #             yield scrapy.Request(
    #                 url=lable_one,
    #                 callback=self.get_last_url,
    #                 # callback=self.parse_list_url,
    #                 dont_filter=True,
    #                 headers=self.headers
    #             )

    # def get_lable_two_url(self, response):
    #     lable_two_url_list = response.xpath("//div[@class='hy']/div[3]//a/@href").getall()
    #     if len(lable_two_url_list) != 0:
    #         for lable_two in lable_two_url_list:
    #             yield scrapy.Request(
    #                 url=lable_two,
    #                 callback=self.get_count,
    #                 headers=self.headers
    #             )
    #     else:
    #         yield scrapy.Request(
    #             url=response.url,
    #             callback=self.get_count,
    #             headers=self.headers
    #         )

    def get_last_url(self, response):
        item = BaogangItem()
        item["url"] = response.url
        count_url = response.xpath("//div[@class='page']//a[contains(text(),'尾页')]/@href").get()
        if count_url:
            yield scrapy.Request(
                url=count_url,
                callback=self.get_count,
                meta={"item":item},
                dont_filter=True,
                headers=self.headers
            )

    def get_count(self, response):
        item = response.meta["item"]
        count = int(response.xpath("//div[@class='right']//span/text()").get().replace("条", ""))
        item["count"] = count
        yield item

        # if count > 1000:
        #     yield scrapy.Request(
        #         url=response.url,
        #         callback=self.get_area_url,
        #         headers=self.headers,
        #         dont_filter=True,
        #     )
        # else:
        #     item["count"] = count
        #     item["url"] = response.url
        #     yield item

    # def get_area_url(self, response):
    #     area_url_list = response.xpath("//div[@id='area']//span/a/@href").getall()
    #     area_url_list_tmp = area_url_list[::-1]
    #     area_url_list_tmp.pop()
    #     area_url_list = area_url_list_tmp[::-1]
    #     for area_url in area_url_list:
    #         yield scrapy.Request(
    #             url=area_url,
    #             callback=self.get_area_count,
    #             dont_filter=True
    #         )
    #
    # def get_area_count(self, response):
    #     item = BaogangItem()
    #     count = int(response.xpath("//div[@class='right']//span/text()").get().replace("条", ""))
    #     # if count > 1000:
    #     #     yield scrapy.Request(
    #     #         url=response.url,
    #     #         callback=self.get_area_url,
    #     #         headers=self.headers,
    #     #         dont_filter=True,
    #     #     )
    #     # else:
    #     item["count"] = count
    #     item["url"] = response.url
    #     # self.count += item["count"]
    #     # print(self.count)
    #     yield item


#
# def get_lable_three_url(self, response):
#     lable_three_url_list = response.xpath("//div[@class='hy']/div[4]//a/@href").getall()
#     if len(lable_three_url_list) != 0:
#         for lable_two in lable_three_url_list:
#             yield scrapy.Request(
#                 url=lable_two,
#                 callback=self.parse_list_url,
#                 headers=self.headers
#             )
#     else:
#         yield scrapy.Request(
#             url=response.url,
#             callback=self.parse_list_url,
#             headers=self.headers
#         )

def parse_list_url(self, response):
    # item = FeijiuItem()
    # item["list_url"] = response.url
    detail_url_list = response.xpath("//div[@class='pro_lists']//div[@class='pro_message']//a/@href").getall()
    if len(detail_url_list) != 0:
        for detail_url in detail_url_list:
            # print(detail_url)
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                meta={"list_url": response.url},
                # dont_filter=True,
                headers=self.headers
            )
    next_url = response.xpath("//a[contains(text(),'下一页')]/@href").get()
    print("*" * 100)
    print(next_url)
    if next_url:
        yield scrapy.Request(
            url=next_url,
            callback=self.parse_list_url,
            dont_filter=True,
            headers=self.headers
        )


def parse_detail_url(self, response):
    item = FeijiuItem()
    item["list_url"] = response.meta["list_url"]
    item["url"] = response.url
    item["kind"] = response.xpath("//div[@class='details_top']//a[2]/text()").get()
    a = response.xpath("//div[@class='details_top']//a[3]/text()").get()
    b = response.xpath("//div[@class='details_top']//a[4]/text()").get()
    item["label_one"] = a
    item["label_two"] = b
    item["title"] = response.xpath("//div[@class='words']/h3//text()").get()
    try:
        item["infoNum"] = response.xpath("//div[@class='words']/span[1]/text()").get().split('：')[1]
        item["type"] = response.xpath("//div[@class='words']/span[2]/text()").get().split('：')[1]
        item["quality"] = response.xpath("//div[@class='words']/span[3]/text()").get().split('：')[1]
        item["number"] = response.xpath("//div[@class='words']/span[4]/text()").get().split('：')[1]
        item["sale_price"] = response.xpath("//div[@class='words']/span[5]/text()").get().split('：')[1]
        item["public_time"] = response.xpath("//div[@class='words']/span[6]/text()").get().split('：')[1]
        item["market"] = response.xpath("//div[@class='words']/span[7]/text()").get().split('：')[1]
        item["comTrade"] = response.xpath("//p[contains(text(),'所属行业')]/text()").get().split('：')[1].replace("\xa0", "")
        item["comProducts"] = response.xpath("//p[contains(text(),'主营产品')]/text()").get().split('：')[1]
    except:
        print("split无信息")
    item["comType"] = response.xpath("//div[@class='dlh_img']/h3/text()").get()
    item["comIndex"] = response.xpath("//a[contains(text(),'进入商铺')]/@href").get()
    item["info"] = response.xpath("//div[@class='p']/text()").get().replace(" ", "").replace("\r", "").replace("\t",
                                                                                                               "").replace(
        "\n", "")
    auth = response.xpath("//a[@class='sd']/text()").getall()
    try:
        item["area_auth"] = auth[0]
        item["debao_auth"] = auth[1]
    except:
        pass
    item["vip_year"] = response.xpath("//div[@class='dlh_message']/p[1]/span/b/text()").get()
    item["vip_type"] = response.xpath("//div[@class='dlh_message']/p[1]/img/@src").get()

    # vip才能看联系方式
    # item["isvip"] = response.xpath("//a[contains(text(),'点此查看联系方式')]/text()").get()
    # if item["isvip"]:
    #     yield item
    phone_url = f'http://www.feijiu.net/infolist/handle.ashx?handType=1&gqid={item["infoNum"]}&doAction=3'
    yield scrapy.Request(
        url=phone_url,
        callback=self.parse_img_url,
        meta={"item": deepcopy(item)},
        dont_filter=True,
        headers=self.headers
    )


def parse_img_url(self, response):
    item = response.meta["item"]
    # print(response.text)
    data = json.loads(response.text)
    if len(data[0]) > 1:
        item["linkMan"] = data[0]["LinkMan"]
        item["comName"] = data[0]["ComName"]
        item["comAddress"] = data[0]["ComAddress"]
        if data[0]["ComPhone"]:
            comPhone_url = 'http://www.feijiu.net' + re.findall('src=\"(.*?)\"', data[0]["ComPhone"])[0]
            item["comPhone"] = self.parse_img(comPhone_url)
        if data[0]["Mobile"]:
            mobile_list = []
            for url in re.findall('src=\"(.*?)\"', data[0]["Mobile"]):
                mobile_url = f'http://www.feijiu.net{url}'
                mobile_list.append(self.parse_img(mobile_url))
            item["mobile"] = mobile_list
        # print(item)
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["isvip"] = False
        yield item
        # print(item)
    else:
        # vip 才有数据
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["isvip"] = True
        yield item
        # print(item)
        # print("*"*100)
        # print(item["url"])


def parse_img(self, img_url):
    # s = requests.Session()
    # s.mount('http://', HTTPAdapter(max_retries=3))
    # # s.mount('https://', HTTPAdapter(max_retries=3))
    # data = s.get(url=img_url, timeout=1).content
    print(img_url)
    # proxy = getProxy()
    # proxies = {"http": proxy}
    # data = requests.get(url=img_url, proxies=proxies, verify=False, headers=self.headers).content
    data = requests.get(url=img_url, verify=False, headers=self.headers).content
    image = Image.open(io.BytesIO(data))
    x, y = image.size
    try:
        # (alpha band as paste mask).
        p = Image.new('RGBA', image.size, (0, 0, 0))
        p.paste(image, (0, 0, x, y), image)
        # p.show()
        # p.save('test.png')
    except:
        pass
    vcode = pytesseract.image_to_string(p, lang='eng').strip().replace(" ", "")
    return vcode


def getProxy():
    url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy
