# -*- coding: utf-8 -*-
import json
import time

import scrapy
import uuid
import copy

from scrapy_splash import SplashRequest, SplashFormRequest
from baogang.items import OuyeelItem

website = 'ouyeel_test'


class OuyeelSpider(scrapy.Spider):
    name = website
    allowed_domains = ['ouyeel.com']

    # start_urls = ['www.baidu.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'MONGODB_SERVER': "192.168.1.94",
        # 'MONGODB_SERVER': "127.0.0.1",
        'SPLASH_URL': 'http://127.0.0.1:8050',
        'MONGODB_SERVER': '180.167.80.118',
        # 端口号，默认是27017
        'MONGODB_PORT': 2502,
        'MONGODB_DB': 'baogang',
        'MONGODB_COLLECTION': 'ouyeel_test',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'INFO',
        # 'REDIS_URL': 'redis://192.168.1.241:6379'
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            # 'baogang.middlewares.SeleniumMiddleware': 300,
        },
    }

    def __init__(self, **kwargs):
        super(OuyeelSpider, self).__init__(**kwargs)
        self.detail_url = 'https://www.ouyeel.com/buyer-ng/resource/resourceData?resourceType=10&resId=1392404789'
        self.shopcode = {'昌敬实业': 'T00605', '上海凡川': 'T06309', '上海冠山': 'T14216', '凯德嘉瑞': 'T110110', '上海钢红': 'T06458',
                         '上海福然德': 'T11698', '上海博冶': 'T08747', '上海泽图': 'T17104', '上海浙萧': 'T12959', '君博钢材': 'T15970',
                         '马钢慈湖加工': 'T26479', '首钢上海': 'T24179', '马钢现货中心': 'T10400', '广州首钢': 'T31180', '宝钢钢贸': 'T02217',
                         '山东首钢': 'T31978', '上海本钢': 'T104491', '广州宝钢': 'T04083', '宁波钢铁': 'T15790', '邯钢恒生': 'T100806',
                         '邯钢': 'T268699'}
        self.script = """
                function main(splash, args)
                  assert(splash:wait(2))
                  splash:set_custom_headers({
                    ['Accept'] = '*/*',
                    ['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    ['Cache-Control'] = 'max-age=0',
                    ['Connection'] = 'keep-alive',
                    ['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
                  })
                  splash.private_mode_enabled = false
                  assert(splash:go(args.url))
                  assert(splash:wait(5))
                  return {
                    html = splash:html(),
                  }
                end
                """

    def start_requests(self):
        # url = "http://192.168.1.172:8050"
        url = 'https://car.autohome.com.cn/config/spec/24355.html#pvareaid=3454541'
        # url = "https://k.autohome.com.cn/detail/view_01dtyfsp7n68w3cd9s70tg0000.html?st=14&piap=0|3170|0|0|1|0|0|0|0|0|1#pvareaid=2112108"
        # url = "https://www.ouyeel.com/search-ng/shop/T00605/search/?"
        yield SplashRequest(
            url=url,
            endpoint='execute',
            # args={'lua_source': self.script, 'wait': 1},
            args={'lua_source': self.script, 'images': 0, 'wait': 1},
            dont_filter=True,
        )
        # yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        print(response.text)
        # # self.shop_url = f"https://www.ouyeel.com/search-ng/shop/{}/search/?"
        # for k, v in self.shopcode.items():
        #     shop_data = dict()
        #     # time.sleep(0.5)
        #     print(k)
        #     shop_data["shop_name"] = k
        #     shop_data["shop_code"] = v
        #     # shop_url = f"https://www.ouyeel.com/search-ng/shop/{v}/search/?"
        #     shop_data["url"] = f"https://www.ouyeel.com/search-ng/shop/{v}/search/?"
        # yield SplashRequest(
        #     url=shop_data["url"],
        #     endpoint='execute',
        #     callback=self.get_page_num,
        #     meta={"shop_data": shop_data},
        #     # args={'lua_source': self.script, 'wait': 1},
        #     args={'lua_source': self.script, 'images': 0, 'wait': 1},
        #     dont_filter=True,
        # )

    def get_page_num(self, response):
        shop_data = response.meta["shop_data"]
        shop_data_num = response.xpath("//*[@id='totalCount']//text()").get()
        jj_status = ",".join(response.xpath("//span[@class='sp_add_cart_status']/text()").getall())
        shop_data["jj_status"] = True if "竞价" in jj_status else False
        shop_data["data_num"] = shop_data_num
        shop_data["page_num"] = int(int(shop_data_num) / 20) + 1 if int(int(shop_data_num) / 20) != 0 else 0
        shop_data[
            "data_url"] = f"https://www.ouyeel.com/jk-mobile/search/main-search/?page=1&shop={shop_data['shop_code']}"
        print(shop_data)
        # for num in range(1, shop_data["page_num"]+1):
        #     detail_url = f"https://www.ouyeel.com/jk-mobile/search/main-search/?page={num}&shop={shop_data['shop_code']}"
        #     # print(detail_url)
        #     yield scrapy.Request(
        #         url=detail_url,
        #         callback=self.parse_data,
        #         meta={"shop_data": shop_data},
        #     )

    def parse_data(self, response):
        # item = OuyeelItem()
        shop_data = response.meta["shop_data"]
        data = json.loads(response.text)
        if len(data["data"]) != 0:
            for i in data["data"]:
                # item = OuyeelItem()
                item = dict()
                item["_id"] = uuid.uuid4().__str__()
                item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["resourceId"] = i["id"]
                item["provider_code"] = i["provider_code"]
                item["provider_name"] = i["provider_name"]
                item["packCode"] = i["pack_code"]
                # item["shop_data"] = shop_data
                # item["balance_weight"] = i["balance_weight"]
                # item["unit_weight"] = i["unit_weight"]
                # item["manufacturer"] = i["manufacturer"]
                # item["shop_sign"] = i["shop_sign"]
                # item["resource_type"] = i["resource_type"]
                # yield item
                pc_detail_url = ""
                yield scrapy.Request(
                    url=pc_detail_url,
                    callback=self.pc_detail_url,
                )
                # print(item)

    def pc_detail_url(self, response):
        item = response["item"]
        data = json.loads(response.text)
        item["sellerScore"] = data["sellerScore"]
        resourceinfo = data["resourceInfo"]
        item["ownerCode"] = resourceinfo["ownerCode"]
        item["ownerName"] = resourceinfo["ownerName"]
        item["publishDate"] = resourceinfo["publishDate"]
        item["basicPrice"] = resourceinfo["basicPrice"]
        item["publishPrice"] = resourceinfo["publishPrice"]
        item["minPrice"] = resourceinfo["minPrice"]
        item["maxPrice"] = resourceinfo["maxPrice"]
        item["productTypeCode"] = resourceinfo["productTypeCode"]
        item["productTypeName"] = resourceinfo["productTypeName"]
        item["productCode"] = resourceinfo["productCode"]
        item["productName"] = resourceinfo["productName"]
        item["packType"] = resourceinfo["packType"]
        item["lengthStdType"] = resourceinfo["lengthStdType"]
        item["weightUnit"] = resourceinfo["weightUnit"]
        item["quantityUnit"] = resourceinfo["quantityUnit"]
        item["unitWeight"] = resourceinfo["unitWeight"]
        item["weight"] = resourceinfo["weight"]
        item["balanceWeight"] = resourceinfo["balanceWeight"]
        item["quantity"] = resourceinfo["quantity"]
        item["balanceQuantity"] = resourceinfo["balanceQuantity"]
        item["shopSign"] = resourceinfo["shopSign"]
        item["refShopSign"] = resourceinfo["refShopSign"]
        item["qualityGrade"] = resourceinfo["qualityGrade"]
        item["spec"] = resourceinfo["spec"]
        item["spec1"] = resourceinfo["spec1"]
        item["spec2"] = resourceinfo["spec2"]
        item["spec3"] = resourceinfo["spec3"]
        item["spec4"] = resourceinfo["spec4"]
        item["spec5"] = resourceinfo["spec5"]
        item["spec6"] = resourceinfo["spec6"]
        item["spec7"] = resourceinfo["spec7"]
        item["spec8"] = resourceinfo["spec8"]
        item["spec9"] = resourceinfo["spec9"]
        item["spec10"] = resourceinfo["spec10"]
        item["specialComments"] = resourceinfo["specialComments"]
        item["manufactureCode"] = resourceinfo["manufactureCode"]
        item["manufactureName"] = resourceinfo["manufactureName"]
        item["warehouseCode"] = resourceinfo["warehouseCode"]
        item["warehouseName"] = resourceinfo["warehouseName"]
        item["location"] = resourceinfo["location"]
        item["storeCityCode"] = resourceinfo["storeCityCode"]
        item["createDate"] = resourceinfo["createDate"]
        item["contactQq"] = resourceinfo["contactQq"]
        item["contactPhone"] = resourceinfo["contactPhone"]
        item["shopShortName"] = resourceinfo["shopShortName"]
        item["longitude"] = resourceinfo["longitude"]
        item["latitude"] = resourceinfo["latitude"]
        item["sellerLevel"] = resourceinfo["sellerLevel"]
        item["promiseTime"] = resourceinfo["promiseTime"]
        item["color"] = resourceinfo["color"]
        # item["factoryResCode"] = resourceinfo["factoryResCode"]
        # item["estimatePrice"] = resourceinfo["estimatePrice"]
        # item["packingTypeCode"] = resourceinfo["packingTypeCode"]
        # item["packingTypeName"] = resourceinfo["packingTypeName"]
        # item["edgeMorphology"] = resourceinfo["edgeMorphology"]
        # item["techStandard"] = resourceinfo["techStandard"]
        # item["surfaceQuality"] = resourceinfo["surfaceQuality"]
        # item["surfaceStructure"] = resourceinfo["surfaceStructure"]
        # item["qualityScore"] = resourceinfo["qualityScore"]
        # item["hasFreightSubsidy"] = resourceinfo["hasFreightSubsidy"]
        # item["hasQualityCert"] = resourceinfo["hasQualityCert"]
        # item["hasFreight"] = resourceinfo["hasFreight"]
        # item["putinDate"] = resourceinfo["putinDate"]
        # item["manufactureDate"] = resourceinfo["manufactureDate"]
        # item["surfaceDispose"] = resourceinfo["surfaceDispose"]
        # item["estimatePrice"] = resourceinfo["estimatePrice"]
        # item["claddingSnWeight"] = resourceinfo["claddingSnWeight"]
        # item["claddingZnLayer"] = resourceinfo["claddingZnLayer"]
        # item["claddingZnWeight"] = resourceinfo["claddingZnWeight"]
        # item["paintType"] = resourceinfo["paintType"]
        # item["bastingWeight"] = resourceinfo["bastingWeight"]
        # item["coatingType"] = resourceinfo["coatingType"]
        # item["coatingStructure"] = resourceinfo["coatingStructure"]
        # item["surfaceMorphology"] = resourceinfo["surfaceMorphology"]
        # item["surfaceProcess"] = resourceinfo["surfaceProcess"]
        # item[""] = resourceinfo[""]

    def app_detail_url(self, response):
        pass
