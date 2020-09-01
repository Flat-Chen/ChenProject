# -*- coding: utf-8 -*-
import scrapy
import time
import json
import redis
from scrapy_redis.spiders import RedisSpider
# from che300_new.items import Che300_Big_Car_evaluate_Item
from scrapy_redis.utils import bytes_to_str
import io
import base64
import re
import pytesseract
from PIL import Image

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=14)
con = redis.Redis(connection_pool=pool)
website = 'che300_big_car_evaluate_sh_city'


class Che300BigCarEvaluateShCitySpider(RedisSpider):
    name = website
    # redis_key = "che300_big_car_evaluate_sh_city:start_urls"
    redis_key = "che300_price_daily:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(Che300BigCarEvaluateShCitySpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Cookie": "pcim=8b7c7256db284e01a54442e53d1cb896d0ca6d7b",
        }
        self.c = con.client()

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        meta = self.structure_http(url)
        now_time = str(time.time()).split('.')[0]
        new_url = f"https://www.che300.com/pinggu/v{meta['prov']}c{meta['city']}m{meta['model']}r{meta['registerDate']}g{meta['mile']}?click=homepage&rt={now_time}"
        return self.make_requests_from_url(new_url, meta)

    def make_requests_from_url(self, url, meta):
        """ This method is deprecated. """
        return scrapy.Request(url, headers=self.headers, dont_filter=True, meta=meta)

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'che300',
        'MYSQL_TABLE': 'che300_price_daily',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_price_daily',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.2.149:6379/15',
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 1,
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            'che300_new.middlewares.SeleniumMiddleware': 401,
            # 'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }

    }
    def structure_http(self, result):
        # 'https://m.che300.com/partner/result.php?prov=3&city=3&brand=50&series=569&model=23438&registerDate=2015-1&mileAge=0.1&intention=0&partnerId=wechat_01&unit=1&sld=sh'
        meta = dict()
        brand = re.search(r'brand=(.*?)&', result).group(1)
        series = re.search(r'series=(.*?)&', result).group(1)
        model = re.search(r'&model=(.*?)&', result).group(1)
        mile = re.search(r'&mileAge=(.*?)&', result).group(1)
        city = re.search(r'&city=(.*?)&', result).group(1)
        prov = re.search(r'prov=(.*?)&', result).group(1)
        registerDate = re.search(r'registerDate=(.*?)&', result).group(1)
        meta['brand'] = brand
        meta['series'] = series
        meta['model'] = model
        meta['registerDate'] = registerDate
        meta['mile'] = mile
        meta['city'] = city
        meta['prov'] = prov
        return meta

    def decode_image(self, src):
        # 1、信息提取
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")

        else:
            raise Exception("Do not parse!")
            return '0'
        # 2、base64解码
        img = base64.urlsafe_b64decode(data)
        image = Image.open(io.BytesIO(img))
        img_str = pytesseract.image_to_string(image)
        return img_str

    def parse(self, response):
        # print("*"*100)
        # print(response.text)
        meta = response.meta
        item = dict()
        price_list = []
        url_list = response.xpath("//div[@id='excellent']//img/@src").getall()
        for url in url_list:
            price = self.decode_image(url)
            print(price)
            price_list.append(price)
        if len(url_list) > 0:
            print(price_list)
            item["price1"] = price_list[3]
            item["price2"] = price_list[0]
            item["price3"] = price_list[4]
            item["price4"] = price_list[1]
            item["price5"] = price_list[5]
            item["price6"] = price_list[2]
            item["price7"] = price_list[6]
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["brand"] = meta["brand"]
            item["series"] = meta["series"]
            item["salesdescid"] = meta["model"]
            item["regDate"] = meta["registerDate"]
            item["cityid"] = meta["city"]
            item["prov"] = meta["prov"]
            item["mile"] = meta["mile"]
            # print(item)
            yield item
        # data = json.loads(response.text)
        # if "eval_prices" in data["data"]:
        #     data_dict = data["data"]["eval_prices"]
        # else:
        #     print(data)
        #     if not data["data"]:
        #         self.c.lpush('che300_big_car_evaluate_sh_city:start_urls', response.url)
        #         print("push url in redis again!")
        #         return
        #     else:
        #         data_dict = data["data"]["eval_prices"]
        # item = Che300_Big_Car_evaluate_Item()
        # item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # item["url"] = response.url
        # mile = re.search(r'mile=(.*)', response.url).group(1)
        # item["goods_type"] = None
        # item["mile"] = mile
        # brand_id = re.search(r'brand_id=(.*?)&', response.url).group(1)
        # series_id = re.search(r'series_id=(.*?)&', response.url).group(1)
        # model_id = re.search(r'model_id=(.*?)&', response.url).group(1)
        # prov_id = re.search(r'prov_id=(.*?)&', response.url).group(1)
        # city_id = re.search(r'city_id=(.*?)&', response.url).group(1)
        # reg_date = re.search(r'&reg_date=(.*)', response.url).group(1)
        # item["brand_id"] = brand_id
        # item["series_id"] = series_id
        # item["model_id"] = model_id
        # item["prov_id"] = prov_id
        # item["city_id"] = city_id
        # item["reg_date"] = reg_date
        # item["default_car_condition"] = data["data"]["default_car_condition"]
        # for i in data_dict:
        #     ci = i["condition"]
        #     item["{}_dealer_high_buy_price".format(ci)] = i["dealer_high_buy_price"]
        #     item["{}_dealer_low_buy_price".format(ci)] = i["dealer_low_buy_price"]
        #     item["{}_dealer_high_sold_price".format(ci)] = i["dealer_high_sold_price"]
        #     item["{}_dealer_buy_price".format(ci)] = i["dealer_buy_price"]
        #     item["{}_dealer_low_sold_price".format(ci)] = i["dealer_low_sold_price"]
        #     item["{}_dealer_sold_price".format(ci)] = i["dealer_sold_price"]
        #
        # item["statusplus"] = response.text + item["url"]
        # yield item
        #
        # # print(item)
        # next_url = self.c.lpop('che300_big_car_evaluate_sh_city:start_urls')
        # print("*" * 100+'next_url')
        # if next_url:
        #     next_url = bytes.decode(next_url)
        #     yield scrapy.Request(
        #         url=next_url,
        #         callback=self.parse,
        #         dont_filter=True
        #     )
