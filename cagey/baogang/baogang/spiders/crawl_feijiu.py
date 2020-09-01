# -*- coding: utf-8 -*-
import io
import json
import re
from copy import deepcopy

import pandas as pd
import pymysql
import scrapy
from PIL import Image
import pytesseract
from uuid import uuid4

from baogang.items import FeijiuItem
# from urllib3.util import retry
import time
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class CrawlFeijiuSpider(RedisCrawlSpider):
    name = 'crawl_feijiu'
    # allowed_domains = ['www.feijiu.net']
    redis_key = 'crawl_feijiu:start_urls'

    # start_urls = ['http://www.feijiu.net/']

    def __init__(self):
        super(CrawlFeijiuSpider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.vip_type = {'http://style.feijiu.net/images/index20180202/pthy.png': '普通会员',
                         'http://style.feijiu.net/images/index20180202/gghy.png': '广告会员',
                         'http://style.feijiu.net/images/index20180202/jchy.png': '基础会员',
                         'http://style.feijiu.net/images/index20180202/hyhy.png': '行业会员',
                         'http://style.feijiu.net/images/index20180202/zxqyhy.png': '中小企业',
                         'http://style.feijiu.net/images/index20180202/viphy.png': 'VIP会员',
                         'http://style.feijiu.net/images/index20180202/bzhy.png': '标准会员',
                         'http://style.feijiu.net/images/index20180202/jtqyhy.png': '集团企业'}

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_COLLECTION': 'feijiu_all',
        'MONGODB_DB': 'baogang',
        'CrawlCar_Num': 1000000,
        'MYSQL_USER': 'baogang',
        'MYSQL_PWD': 'Baogang@2019',
        'MYSQL_SERVER': '192.168.2.120',
        'MYSQL_PORT': 3306,
        'MYSQL_DB': 'baogang',
        # 'CONCURRENT_REQUESTS': 5,
        # 'AUTOTHROTTLE_ENABLED': True,
        # 起始的延迟
        'AUTOTHROTTLE_START_DELAY': 32,
        # 最小延迟
        'DOWNLOAD_DELAY': 0,
        # 最大延迟
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        # 'DOWNLOAD_TIMEOUT': 10,
        # 'RETRY_ENABLED': True,
        # 'RETRY_TIMES': 5,
        # 'DOWNLOAD_FAIL_ON_DATALOSS': True,
    }

    rules = (
        Rule(LinkExtractor(allow=r'-\d+/',
                           restrict_xpaths="//div[@class='page']//a[not(contains(text(),'尾页')) and not(contains(text(),'上一页'))and not(contains(text(),'首页'))and not(contains(text(),'...'))and not(contains(text(),'下一页'))]"),
             callback='parse_list_url'),
        Rule(LinkExtractor(allow=r'-\d+/', restrict_xpaths="//div[@class='page']//a[contains(text(),'...')]"),
             follow=True),
    )
    # def start_requests(self):
    #     url = "http://www.feijiu.net/FeiJinShu/"
    #     return [scrapy.Request(url=url, dont_filter=True, headers=self.headers)]

    def parse_list_url(self, response):
        # item = FeijiuItem()
        # item["list_url"] = response.url
        print(response.url)
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
        # next_url = response.xpath("//a[contains(text(),'下一页')]/@href").get()
        # print("*" * 100)
        # print(next_url)
        # if next_url:
        #     yield scrapy.Request(
        #         url=next_url,
        #         callback=self.parse_list_url,
        #         dont_filter=True,
        #         headers=self.headers
        #     )

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
            item["comName"] = response.xpath("//span[contains(text(),'公司名称')]/text()").get().split('：')[1]
            item["comAddress"] = response.xpath("//span[contains(text(),'市场名称')]/text()").get().split('：')[1]
            item["infoNum"] = response.xpath("//div[@class='words']/span[1]/text()").get().split('：')[1]
            item["type"] = response.xpath("//div[@class='words']/span[2]/text()").get().split('：')[1]
            item["quality"] = response.xpath("//div[@class='words']/span[3]/text()").get().split('：')[1]
            item["number"] = response.xpath("//div[@class='words']/span[4]/text()").get().split('：')[1]
            item["sale_price"] = response.xpath("//div[@class='words']/span[5]/text()").get().split('：')[1]
            item["public_time"] = response.xpath("//div[@class='words']/span[6]/text()").get().split('：')[1]
            item["market"] = response.xpath("//div[@class='words']/span[7]/text()").get().split('：')[1]
            item["comTrade"] = response.xpath("//p[contains(text(),'所属行业')]/text()").get().split('：')[1].replace(
                "\xa0", "")
            item["comProducts"] = response.xpath("//p[contains(text(),'主营产品')]/text()").get().split('：')[1]
        except:
            print("split无信息")
        item["comType"] = response.xpath("//div[@class='dlh_img']/h3/text()").get()
        item["comIndex"] = response.xpath("//a[contains(text(),'进入商铺')]/@href").get()
        item["info"] = response.xpath("//div[@class='p']/text()").get().replace(" ", "").replace("\r", "").replace(
            "\t", "").replace("\n", "")
        auth = response.xpath("//a[@class='sd']/text()").getall()
        item["area_auth"] = response.xpath("//p[contains(text(),'实地认证')]//a/text()").get()
        item["debao_auth"] = response.xpath("//p[contains(text(),'德保认证')]//a/text()").get()
        item["vip_year"] = response.xpath("//div[@class='dlh_message']/p[1]/span/b/text()").get()
        vip_type_image_url = response.xpath("//div[@class='dlh_message']/p[1]/img/@src").get()
        if vip_type_image_url:
            item["vip_type"] = self.vip_type[vip_type_image_url]
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
            mobile_list = []
            ComPhone_list = []
            if data[0]["ComPhone"]:
                comPhone_url = 'http://www.feijiu.net' + re.findall('src=\"(.*?)\"', data[0]["ComPhone"])[0]
                comPhone = self.parse_img(comPhone_url)
                if comPhone:
                    comPhone = re.sub('\.|\‘','', comPhone)
                    if ',' in comPhone:
                        phone_tmp = comPhone.split(',')
                        for phone in phone_tmp:
                            if len(phone) == 11:
                                phone = phone.replace('?', '9').replace('*', '9')
                                mobile_list.append(phone)
                            else:
                                ComPhone_list.append(phone)
                    elif '/' in comPhone:
                        phone_tmp = comPhone.split('/')
                        for phone in phone_tmp:
                            if len(phone) == 11:
                                phone = phone.replace('?', '9')
                                mobile_list.append(phone)
                            else:
                                ComPhone_list.append(phone)
                    elif len(comPhone) == 11 and '-' not in comPhone:
                        phone = comPhone.replace('?', '9')
                        mobile_list.append(phone)
                    elif len(comPhone) == 16 or len(comPhone) == 15:
                          phone = comPhone.split('-')[1].replace('?', '9')
                          mobile_list.append(phone)
                    elif comPhone.startswith('86'):
                        phone = comPhone[-11:].replace('?', '9')
                        mobile_list.append(phone)
                    else:
                        comPhone = comPhone.replace('?', '9')
                        ComPhone_list.append(comPhone)

                    if len(ComPhone_list) > 0:
                        item["comPhone"] = ','.join(ComPhone_list)
                    else:
                        item["comPhone"] = None
            else:
                item["comPhone"] = None

            if data[0]["Mobile"]:
                for url in re.findall('src=\"(.*?)\"', data[0]["Mobile"]):
                    mobile_url = f'http://www.feijiu.net{url}'
                    mobile_list.append(self.parse_img(mobile_url))
                if len(mobile_list) > 0:
                    mobile_list_new = []
                    for mobile in mobile_list:
                        mobile = mobile.replace('‘', '').replace('?', '9').replace('|', '').replace('%', '96').replace('I', '1')
                        if '?' in mobile:
                            mobile = mobile.replace('?', '9')
                        # if '—' not in mobile and '*' not in mobile and mobile.startswith('1'):
                        if all(i not in mobile for i in ['—', '-', '*']) and mobile.startswith('1'):
                            mobile_list_new.append(mobile)
                    mobile_str = ','.join(set(mobile_list_new))
                    item["mobile"] = mobile_str
            else:
                item["mobile"] = None
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["isvip"] = False
            item["_id"] = uuid4().__str__()
            yield item
            # print(item)
        else:
            # vip 才有数据
            item["linkMan"] = None
            item["mobile"] = None
            item["comPhone"] = None
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["isvip"] = True
            item["_id"] = uuid4().__str__()
            yield item
            # print(item)

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
