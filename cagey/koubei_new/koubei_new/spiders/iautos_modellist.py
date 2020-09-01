# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from koubei_new.items import IautosFamilyItem


class IautosModellistSpider(scrapy.Spider):
    name = 'iautos_modellist'
    # allowed_domains = ['iauto.com']
    # start_urls = ['http://iauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(IautosModellistSpider, self).__init__(**kwargs)
        self.counts = 0
        self.miss_list = [2380,1782,1537,1544,1546,1548,1712,1881,1883,1886,1888,1889,2128,2240,1894,2243,2203,1934,2202,1817,5,4447,2252,1822,2253,2251,2249,1275,1650,2388,2389,1418,1218,1653,2460,2472,2775,1318,2522,2525,2528,2529,2533,2539,2541,1307,1313,1341,921,2569,1042,1388,2576,2580,2583,2584,2587,2405,2590,2593,2594,1317,2599,2600,2602,2603,2606,2609,2612,2611,2617,2616,2619,2621,2620,2623,2638,2640,2639,2641,1464,2378,1488,2644,2662,2665,2664,2672,1329,1324,1338,2680,1344,2688,1305,1880,1871,2364,1294,3088,2613,2699,2859,1079,4296,2787,2788,41,2889,2861,2906,2909,2911,2929,3624,4202,44,3050,3051,3078,3149,3160,4201,4204,3245,3252,3255,3296,3299,3303,3318,4331,3844,3375,3376,3382,3592,3381,3383,4389,3388,4442,4301,3427,3394,4109,3397,3639,3398,3401,3380,3402,3420,3441,3405,3406,3407,4221,3409,3410,3411,4791,4792,3413,3422,3415,3982,3416,3418,3419,3421,3425,3424,3423,3426,3429,3430,3431,3432,3433,4443,3435,3436,3625,3437,3990,3439,3408,3440,3442,3443,3444,3445,3448,3449,3450,3451,3623,3452,3453,4272,3456,3457,3458,4793,3460,3462,3463,4436,3513,3469,3470,3471,3473,4295,3476,3477,3478,3479,4438,3641,3480,3481,3484,3485,3489,3487,3490,3494,4129,3496,4006,3642,3474,3508,3512,3515,3521,3522,4290,4105,4434,3530,3164,3536,3537,4203,3538,3541,3542,3546,3548,3549,3553,3554,3556,4098,4446,877,779,3558,762,3559,3967,3560,4079,3564,4798,3597,3567,3568,3572,3574,3573,3575,3580,3581,3582,3583,3636,3590,3591,3593,3599,4449,3957,3604,3605,3606,3607,3612,3655,4444,3647,3646,3644,3643,3638,3637,3635,3634,3633,3630,3629,3628,4282,3621,4277,3620,3618,3617,854,3999,3965,4061,4034,4293,4095,4289,4279,4073,3808,3902,4003,4012,4445,4035,4053,4074,3835,4280,3977,4199,3899,4020,3836,4291,4292,4286,4281,4278,4076,4069,4094,3944,4041,4106,3963,3657,3658,3455,934,3523,3663,3664,3668,4026,3678,3686,3689,3699,3703,4273,3705,3622,4205,3704,4038,3709,3710,3711,4285,4015,3716,4275,3717,3719,1003,3727,3728,3729,4078,3735,3736,4065,3741,3742,3744,3745,3746,4045,3756,3757,3760,3764,3765,3766,3767,3768,3770,3773,3780,3782,3790,3792,3798,4439,3803,4223,3805,3806,3807,3809,3817,3818,3819,3821,3823,3715,3827,3829,3830,3671,3831,3833,3838,3839,216,3201,3073,3167,2977,3845,3434,4294,3387,3733,3852,4042,3854,4050,3855,3652,3396,3648,3856,3389,3858,3859,3860,3862,4274,3863,3864,3865,3464,3525,3866,3867,3869,3872,3877,3565,3878,3880,3881,3882,3884,4014,4008,3986,3898,3946,3900,3901,3903,4054,4009,3913,3914,3915,3917,3918,3919,3923,3922,3924,3926,3929,3936,3937,3939,3940,3941,3943,3947,3953,3954,3958,3959,4283,3960,3961,3962,3966,3968,3970,3974,3979,3980,3983,3987,3991,3995,3997,3998,4000,4001,4002,4007,3978,4011,4021,4023,4027,4029,4031,4033,3895,4037,4043,4044,4048,4049,4051,4052,4055,4057,4058,4059,4060,4062,4064,4066,4067,4075,4083,4084,4085,4089,4090,4092,4093,4096,4101,4102,4103,4107,4110,4113,4114,4115,4116,4117,4119,4123,4124,4126,4121,4128,4130,4132,4139,4138,4141,4144,4145,4142,4154,4159,4160,4111,4140,4165,4168,4170,4171,3707,4173,4174,4175,4179,4180,4181,4183,4184,4185,4188,4189,4190,4192,4194,4206,4209,4212,4214,4216,4217,4218,4219,4220,4222,4224,4225,4227,4231,4236,4237,4238,4243,4245,4247,4255,4256,4257,4260,4262,4266,4269,4270,4271,4300,4303,4306,4307,4308,4314,4315,4317,4322,4325,4326,4327,4329,4334,3645,4161,4340,4341,3747,4342,4344,4346,4347,4348,1070,1519,2399,1395,1323,1325,1322,1327,2571,1484,1487,1465,1485,1486,1490,1102,2082,2127,2126,1269,1271,1272,1276,1301,2591,1553,1549,1901,1550,1966,1551,1343,1332,1898,1340,1382,1311,2575,2362,2363,2075,2314,2387,1960,2392,1547,2208,2383,2379,2256,791,2261,1106]
        self.miss_list_new = [4447,4389,4442,4791,4792,4443,4793,4436,4438,4434,4446,4798,4449,4444,4445,4439,4340,4341,4342,4344,4346,4347,4348]
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                # 'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
            }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'koubei',
        'MYSQL_TABLE': 'iautos_modellist_fixed2_miss',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'koubei',
        'MONGODB_COLLECTION': 'iautos_modellist_fixed2_miss',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES': {
            'koubei_new.middlewares.ProxyMiddleware': 500,
            'koubei_new.middlewares.RotateUserAgentMiddleware': 541,
        },

    }

    def start_requests(self):
        for car_id in self.miss_list[::-1]:
        # for car_id in self.miss_list_new:
            car_url = f"https://www.iautos.cn/chexing/model.asp?id={car_id}"
            yield scrapy.Request(
                url=car_url,
                headers=self.headers,
                meta={"car_id": car_id},
                callback=self.parse_miss_car
            )

        # url = "https://www.iautos.cn/chexing/"
        # yield scrapy.Request(
        #     url=url,
        #     headers=self.headers
        # )

    def parse_miss_car(self, response):
        car_id = response.meta["car_id"]
        item = IautosFamilyItem()
        info_list = response.xpath("//div[@id='bread']/text()").getall()
        item['familyname'] = info_list[2].split('>')[-1]
        item['familyid'] = car_id
        re_data = re.findall('shwMakeModel_new\((.*?)\);', response.text)[0]
        brand_name = re.findall('"brand":"(.*?)",', re_data)[0]
        # brand_id = re.findall('"brandId":(.*?),"', re_data)[0]
        factoryname = re.findall('"maker":"(.*?)",', re_data)[0]
        item['factoryname'] = factoryname
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['brandname'] = brand_name
        # print(item)
        yield item


    def parse(self, response):
        brands = response.xpath("//div[@class='bn']")
        for brand in brands:
            brandname = brand.xpath("text()").extract_first()
            url = brand.xpath("../@href").extract_first()
            meta = {
                "brandname": brandname,
            }
            # print(url)
            yield scrapy.Request(
                url=url,
                meta=meta,
                callback=self.parse_factory,
                headers=self.headers
            )

    def parse_factory(self, response):
        meta = response.meta
        factories_list = response.xpath("//*[@class='p-r-r-2-all-models']/dl/dt/text()").getall()
        dd_list = response.xpath("//*[@class='p-r-r-2-all-models']/dl/dd")
        try:
            data = re.findall('var seriesList = (.*?)</script>', response.text)[0]
        except:
            yield scrapy.Request(
                url=response.url,
                meta=meta,
                callback=self.parse_factory,
                headers=self.headers
            )
        data = json.loads(data)[0]['s'][0]
        # print(data)
        for dd in dd_list:
            index_num = dd_list.index(dd)
            factoryname = factories_list[index_num]
            p_list = dd.xpath("./p")
            for p in p_list:
                url = p.xpath('./a[1]/@href').get()
                familyname = p.xpath('./a[1]/text()').get()
                for f in data:
                    if familyname.replace("（停产）", "") in f:
                        status = f[4]
                        familyname = familyname.replace("（停产）", "") if status else familyname
                # print(url)
                # print(familyname)
                # print(factoryname)
                familyid = url.split("=")[-1]
                meta = {
                    "factoryname": factoryname,
                    "familyname": familyname,
                    "familyid": familyid,
                }
                meta = dict(meta, **response.meta)
                yield scrapy.Request(
                    url=url,
                    meta=meta,
                    callback=self.parse_ershouche,
                    headers=self.headers
                )

    def parse_ershouche(self, response):
        item = IautosFamilyItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['brandname'] = response.meta["brandname"]
        item['factoryname'] = response.meta["factoryname"]
        item['familyname'] = response.meta["familyname"]
        item['familyid'] = response.meta["familyid"]
        ershou_brand = response.xpath("//*[@class='box3']/div[2]/a[3]/@href").extract_first()
        ershou_factory = response.xpath("//*[@class='box3']/div[2]/a[3]/@href").extract_first()
        ershou_family = response.xpath("//*[@class='box3']/div[2]/a[3]/@href").extract_first()
        if ershou_brand:
            item['ershou_brand'] = ershou_brand.split("/")[-4]
        if ershou_factory:
            item['ershou_factory'] = ershou_factory.split("/")[-3]
        if ershou_family:
            item['ershou_family'] = ershou_family.split("/")[-2]
        # print(item)
        yield item





