# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from pprint import pprint
# from .items import A58carPriceSpider Item

website = '58car_price'

class A58carPriceSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['58.com']
    # start_urls = ['http://58.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(A58carPriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.city_code = {'上海': '2',
                         '云南': '18',
                         '内蒙古': '9',
                         '北京': '1',
                         '吉林': '7',
                         '四川': '17',
                         '天津': '3',
                         '宁夏': '13',
                         '安徽': '24',
                         '山东': '23',
                         '山西': '11',
                         '广东': '30',
                         '广西': '31',
                         '成都': '17',
                         '新疆': '14',
                         '武汉': '21',
                         '江苏': '25',
                         '江西': '32',
                         '河北': '8',
                         '河南': '22',
                         '浙江': '26',
                         '海南': '34',
                         '湖北': '21',
                         '湖南': '20',
                         '甘肃': '12',
                         '福建': '33',
                         '西藏': '15',
                         '贵州': '19',
                         '辽宁': '6',
                         '重庆': '4',
                         '陕西': '10',
                         '青岛': '23',
                         '青海': '16',
                         '黑龙江': '5'}
        self.brand = {}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'newcar_price',
        'MYSQL_TABLE': '58car_price',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'newcar_price',
        'MONGODB_COLLECTION': '58car_price',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "https://www.58che.com/brand.html"
        yield scrapy.Request(
            url=url,
            dont_filter=True
        )

    def parse(self, response):
        div_list = response.xpath("//div[@class='main_nr']")
        for div in div_list:
            brand_code = div.xpath("./div[@class='l']//img/@src").get().split("/p")[1].replace('.jpg', '')
            series_code = div.xpath("./div[@class='r']/ul//dt/a/@href").getall()
            series_code = [i.split('/')[-2] for i in series_code]
            # series_name = div.xpath("./div[@class='r']/ul//dt/a/@title").get()
            self.brand[brand_code] = series_code
        for cityname, citycode in self.city_code.items():
            for brand, series_list in self.brand.items():
                for series in series_list:
                    url = f'https://dealer.58che.com/list_p{citycode}_b{brand}_s{series}_t1_n1.html'
                    meta = {
                        "brandid": brand,
                        "seriesid": series,
                        "cityname": cityname,
                        "citycode": citycode
                    }
                    response.meta.update(**meta)
                    yield scrapy.Request(
                        url=url,
                        meta=response.meta,
                        callback=self.parse_dealer_list,
                        dont_filter=True
                    )

    def parse_dealer_list(self, response):
        div_list = response.xpath("//div[@id='rowDealer']/div[@class='rowBox-index clearfix']")
        if len(div_list):
            for div in div_list:
                shopname = div.xpath('.//h3//a/text()').get()
                dealer_url = div.xpath('.//h3//a/@href').get()
                dealer_address = div.xpath(".//div[@class='dealer-brand']//p[@class='dealer-Address']//span/text()").get().replace('　[', '')
                url = response.urljoin(dealer_url)
                meta = {
                    'shopname': shopname,
                    'dealer_address': dealer_address
                }
                response.meta.update(**meta)
                yield scrapy.Request(
                    url=url,
                    meta=response.meta,
                    callback=self.parse_detail_url,
                    # dont_filter=True
                )
            next_url = response.xpath("//a[@class='next']/@href").get()
            if next_url:
                next_url = response.urljoin(next_url)
                yield scrapy.Request(
                    url=next_url,
                    meta=response.meta,
                    callback=self.parse_dealer_list,
                    dont_filter=True
                )


    def parse_detail_url(self, response):
        # print(response.meta)
        brandname = response.xpath("//select[@id='brandId']/option[2]/text()").get()
        seriesname = response.xpath("//select[@id='lineId']/option[2]/text()").get()
        tr_list = response.xpath("//table//tr")
        for tr in tr_list:
            item = dict()
            modelname = tr.xpath("./td[@class='pr80']/a/text()").get()
            if modelname:
                item["url"] = response.urljoin(tr.xpath("./td[@class='pr80']/a/@href").get())
                item["modelid"] = tr.xpath("./td[@class='pr80']/a/@href").get().split('_')[1].replace('.html', '')
                item["shopid"] = tr.xpath("./td[@class='pr80']/a/@href").get().split('_')[0].replace('/detail/', '')
                item["guideprice"] = tr.xpath("./td[2]/text()").get().replace('\r\n', '').replace(' ', '').replace('万', '')
                item["guidesalesprice"] = tr.xpath("./td[3]/a/text()").get()
                item["modelname"] = modelname
                item["brandname"] = brandname
                item["seriesname"] = seriesname
                item["shopname"] = response.meta["shopname"]
                item["dealer_address"] = response.meta["dealer_address"]
                item["brandid"] = response.meta["brandid"]
                item["seriesid"] = response.meta["seriesid"]
                item["cityname"] = response.meta["cityname"]
                item["citycode"] = response.meta["citycode"]
                item["picurl"] = response.xpath("//dt[@class='mr20 l']//img/@src").get()
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['website'] = website
                # print(item)
                yield item



