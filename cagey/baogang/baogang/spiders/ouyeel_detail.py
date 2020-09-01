# -*- coding: utf-8 -*-
import json
import time

import scrapy
import uuid
import pymongo
from lxml import html
from baogang.items import OuyeelDetailItem
from scrapy_redis.spiders import RedisSpider

website = 'ouyeel_detail'


# class OuyeelDetailSpider(scrapy.Spider):
class OuyeelDetailSpider(RedisSpider):
    name = website
    allowed_domains = ['ouyeel.com']
    redis_key = "ouyeel_detail_bg:start_urls"
    # start_urls = ['https://www.ouyeel.com/search-ng/shop/ygjNwEDV/search/?',]

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_USER': 'baogang',
        'MYSQL_PWD': 'Baogang@2019',
        'MYSQL_SERVER': '192.168.2.120',
        'MYSQL_PORT': 3306,
        'MYSQL_DB': 'baogang',
        'REDIS_URL': 'redis://192.168.1.241:6379/10',
        'SCHEDULER_PERSIST': False,
        # 'MONGODB_SERVER': '180.167.80.118',
        'MONGODB_SERVER': '192.168.1.92',
        # 端口号，默认是27017
        # 'MONGODB_PORT': 1206,
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'baogang',
        'MONGODB_COLLECTION': 'ouyeel_new_bg',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        # 'LOG_LEVEL': 'INFO',
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            # 'baogang.middlewares.SeleniumMiddleware': 300,
            # 'baogang.middlewares.SeleniumFirefoxMiddleware': 301,

        },
    }

    def __init__(self, **kwargs):
        super(OuyeelDetailSpider, self).__init__(**kwargs)
        self.detail_url = 'https://www.ouyeel.com/buyer-ng/resource/resourceData?resourceType=10&resId=1392404789'
        self.k = []

    # def start_requests(self):
    #     settings = self.settings
    #     uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
    #     connection = pymongo.MongoClient(uri)
    #     db = connection[settings['MONGODB_DB']]
    #     collection_tmp = db["ouyeel_data_num_tmp"]
    #     data_list = collection_tmp.find()
    #     for data in data_list:
    #         shop_data = data
    #         if shop_data["jj_status"]:
    #             # for num in range(1, shop_data["jj_page_num"]+1):
    #             #     status = 1
    #             #     jj_url = f"https://www.ouyeel.com/jk-mobile/search/main-search/?page={num}&shop={shop_data['shop_code']}&salesMethod=20"
    #             #     yield scrapy.Request(
    #             #         url=jj_url,
    #             #         meta={"shop_data": shop_data, "status": status},
    #             #         # callable=self.parse_jj_data,
    #             #         dont_filter=True
    #             #     )
    #             for num in range(1, int(shop_data["page_num"] - shop_data["jj_page_num"] + 1)):
    #                 status = 0
    #                 gp_url = f"https://www.ouyeel.com/jk-mobile/search/main-search/?page={num}&shop={shop_data['shop_code']}&salesMethod=10"
    #                 yield scrapy.Request(
    #                     url=gp_url,
    #                     meta={"shop_data": shop_data, "status": status},
    #                     dont_filter=True
    #                 )
    #         else:
    #             for num in range(1, shop_data["page_num"] + 1):
    #                 status = 0
    #                 resource_list_url = f"https://www.ouyeel.com/jk-mobile/search/main-search/?page={num}&shop={shop_data['shop_code']}"
    #                 yield scrapy.Request(
    #                     url=resource_list_url,
    #                     meta={"shop_data": shop_data, "status": status},
    #                     dont_filter=True
    #                 )

    def parse(self, response):
        # shop_data = response.meta["shop_data"]
        # status = response.meta["status"]
        list_data = json.loads(response.text)
        if len(list_data["data"]) != 0:
            for data in list_data["data"]:
                item = OuyeelDetailItem()
                for k, v in data.items():
                    try:
                        item[k] = v
                    except KeyError as e:
                        print(e)
                app_detail_url = f"https://www.ouyeel.com/jk-mobile/zy/get-package-detail/?package_id={item['id']}"
                yield scrapy.Request(
                    url=app_detail_url,
                    callback=self.parse_app_detail_url,
                    meta={"item": item},
                    dont_filter=True,
                )

    def parse_app_detail_url(self, response):
        item = response.meta["item"]
        detail_data = json.loads(response.text)
        data_dic = detail_data["package"][0]
        for k, v in data_dic.items():
            if k in gp_field_list:
                item[k] = v
        item["_id"] = uuid.uuid4().__str__()
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield item

        # print(data)
        # item["sellerScore"] = data["sellerScore"]
        # resourceinfo = data["resourceInfo"]
        # item["ownerCode"] = resourceinfo["ownerCode"]
        # item["ownerName"] = resourceinfo["ownerName"]
        # item["publishDate"] = resourceinfo["publishDate"]
        # item["basicPrice"] = resourceinfo["basicPrice"]
        # item["publishPrice"] = resourceinfo["publishPrice"]
        # item["minPrice"] = resourceinfo["minPrice"]
        # item["maxPrice"] = resourceinfo["maxPrice"]
        # item["productTypeCode"] = resourceinfo["productTypeCode"]
        # item["productTypeName"] = resourceinfo["productTypeName"]
        # item["productCode"] = resourceinfo["productCode"]
        # item["productName"] = resourceinfo["productName"]
        # item["packType"] = resourceinfo["packType"]
        # item["lengthStdType"] = resourceinfo["lengthStdType"]
        # item["weightUnit"] = resourceinfo["weightUnit"]
        # item["quantityUnit"] = resourceinfo["quantityUnit"]
        # item["unitWeight"] = resourceinfo["unitWeight"]
        # item["weight"] = resourceinfo["weight"]
        # item["balanceWeight"] = resourceinfo["balanceWeight"]
        # item["quantity"] = resourceinfo["quantity"]
        # item["balanceQuantity"] = resourceinfo["balanceQuantity"]
        # item["shopSign"] = resourceinfo["shopSign"]
        # item["refShopSign"] = resourceinfo["refShopSign"]
        # item["qualityGrade"] = resourceinfo["qualityGrade"]
        # item["spec"] = resourceinfo["spec"]
        # item["spec1"] = resourceinfo["spec1"]
        # item["spec2"] = resourceinfo["spec2"]
        # item["spec3"] = resourceinfo["spec3"]
        # item["spec4"] = resourceinfo["spec4"]
        # item["spec5"] = resourceinfo["spec5"]
        # item["spec6"] = resourceinfo["spec6"]
        # item["spec7"] = resourceinfo["spec7"]
        # item["spec8"] = resourceinfo["spec8"]
        # item["spec9"] = resourceinfo["spec9"]
        # item["spec10"] = resourceinfo["spec10"]
        # item["specialComments"] = resourceinfo["specialComments"]
        # item["manufactureCode"] = resourceinfo["manufactureCode"]
        # item["manufactureName"] = resourceinfo["manufactureName"]
        # item["warehouseCode"] = resourceinfo["warehouseCode"]
        # item["warehouseName"] = resourceinfo["warehouseName"]
        # item["location"] = resourceinfo["location"]
        # item["storeCityCode"] = resourceinfo["storeCityCode"]
        # item["createDate"] = resourceinfo["createDate"]
        # item["contactQq"] = resourceinfo["contactQq"]
        # item["contactPhone"] = resourceinfo["contactPhone"]
        # item["shopShortName"] = resourceinfo["shopShortName"]
        # item["longitude"] = resourceinfo["longitude"]
        # item["latitude"] = resourceinfo["latitude"]
        # item["sellerLevel"] = resourceinfo["sellerLevel"]
        # item["promiseTime"] = resourceinfo["promiseTime"]
        # item["color"] = resourceinfo["color"]
        # ----------------------------------------------------------
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
gp_field_list = ['_id',
 'abholung',
 'active_date',
 'allow_buy',
 'balanceQuantity',
 'balance_quantity',
 'balance_weight',
 'baoyou',
 'bid_status',
 'buyerFlag',
 'canCompensateFlag',
 'can_bargaining',
 'cangfeikuaijie',
 'claddingZnLayer',
 'close_status',
 'coatingType',
 'coating_type',
 'color',
 'contact_name',
 'contact_phone',
 'daiyunbutie',
 'depositAmt',
 'edgeMorphology',
 'estimate_price',
 'estimate_unit_price',
 'factoryResCode',
 'factory_res_code',
 'factory_send',
 'flag_dingjin',
 'flag_gongyinglian',
 'flag_manlijian',
 'flag_new_resources',
 'flag_redeem',
 'flag_rongzi',
 'flag_targeting_resources',
 'flag_yinpiao',
 'flag_youhuiquan',
 'flag_zhibaoshu',
 'gongfangdaiyun',
 'grabtime',
 'has_pic',
 'has_zhibaoshu',
 'houjiesuan',
 'id',
 'invoiceFromNameList',
 'is_in_cart',
 'is_quickly_delivery',
 'is_subsidy',
 'is_weighed',
 'jewel_status',
 'location',
 'manufactureName',
 'manufacture_date',
 'manufacturer',
 'merge_grade',
 'morgage_type',
 'negativeRange',
 'out_fee',
 'packCode',
 'packComment1',
 'packType',
 'pack_code',
 'pack_comments',
 'pack_comments2',
 'pack_type',
 'packingTypeName',
 'paintType',
 'penaltyAmt',
 'penaltyAmtRate',
 'pieces',
 'price',
 'prodCat',
 'productTypeCode',
 'productTypeName',
 'product_code',
 'product_name',
 'production_date',
 'promise_time',
 'providerCode',
 'provider_code',
 'provider_name',
 'putin_date',
 'qualityType',
 'quality_grade',
 'quickInvoicingFlag',
 'res_status',
 'resource_type',
 'rongzizhifu',
 'salesMethod',
 'sales_method',
 'sales_mode',
 'shopLevel',
 'shopLogoUrl',
 'shopName',
 'shopType',
 'shop_sign',
 'shop_sign2',
 'shop_type',
 'show_tel',
 'sort_score',
 'spec',
 'spec1',
 'spec3',
 'special',
 'splitable',
 'star',
 'storage_site',
 'storate_freedays',
 'storate_rate',
 'store_city_code',
 'store_city_name',
 'surfaceDispose',
 'surfaceQuality',
 'surfaceStructure',
 'toShopUrl',
 'unit_weight',
 'video_inspection_flag',
 'warehouse_code',
 'warehouse_name',
 'warehouse_score',
 'weight',
 'weightMethod']

