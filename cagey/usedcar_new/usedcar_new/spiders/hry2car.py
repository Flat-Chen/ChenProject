# -*- coding: utf-8 -*-
import scrapy
import time
import json
import time
import datetime
import json
from usedcar_new.items import GanjiItem
import re


class Hry2carSpider(scrapy.Spider):
    name = 'hry2car'
    allowed_domains = ['jnesc.com']

    # start_urls = ['http://jnesc.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Hry2carSpider, self).__init__(**kwargs)
        self.counts = 0
        self.city_list = ['http://zibo.jnesc.com/oldcar/', 'http://jining.jnesc.com/oldcar/',
                          'http://weihai.jnesc.com/oldcar/', 'http://qingdao.jnesc.com/oldcar/',
                          'http://binzhou.jnesc.com/oldcar/', 'http://rizhao.jnesc.com/oldcar/',
                          'http://linyi.jnesc.com/oldcar/', 'http://zaozhuang.jnesc.com/oldcar/',
                          'http://yantai.jnesc.com/oldcar/', 'http://heze.jnesc.com/oldcar/',
                          'http://taian.jnesc.com/oldcar/', 'http://weifang.jnesc.com/oldcar/',
                          'http://dezhou.jnesc.com/oldcar/', 'http://liaocheng.jnesc.com/oldcar/',
                          'http://laiwu.jnesc.com/oldcar/', 'http://dongying.jnesc.com/oldcar/']

        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'WEBSITE': 'hry2car',
        'MYSQL_TABLE': 'hry2car_online',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'hry2car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.GanjiPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
           'usedcar_new.middlewares.SeleniumMiddleware': 600,
           'scrapy.downloadermiddlewares.retry.RetryMiddleware': 800,
        }

    }

    def start_requests(self):
        for url in self.city_list:
            # url = url + 's2/'
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                headers=self.headers,
                callback=self.parse_list
            )

    # def parse(self, response):
    #     data_num = response.xpath("//div[@class='bc-class']//em/text()").get()
    #     data_num = int(data_num.replace(',', '')) if data_num else None
    #     if data_num:
    #         for num in range(1, int(data_num/40)+1):
    #         # for num in range(1, 2):
    #             # next_url = f'/oldcar/q{num}/'
    #             next_url = f'/oldcar/s100q{num}/'
    #             next_url = response.urljoin(next_url)
    #             yield scrapy.Request(
    #                 url=next_url,
    #                 callback=self.parse_list,
    #                 dont_filter=True,
    #                 headers=self.headers,
    #             )
    #     else:
    #         print(response.url)
    #         print("*"*100)

    def parse_list(self, response):
        url_list = response.xpath("//div[@class='reco-car-bottom']//a/@href").getall()
        print(url_list)
        if url_list:
            for url in url_list:
                url = response.urljoin(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_detail,
                )
        next_url = response.xpath("//span[contains(text(),'下一页')]/../@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_list,
                dont_filter=True,
                headers=self.headers
            )


    def parse_detail(self, response):
        item = GanjiItem()
        # status = response.meta["status"]
        item["carid"] = response.xpath('//*[@id="history_cbi_no"]/@value').get()
        item["shortdesc"] = response.xpath("//div[@class='sp-car-wenzi']/h2/text()").get()
        item["price1"] = response.xpath("//*[@class='car2-mon']/text()").get()
        item["mileage"] = response.xpath("//*[contains(text(),'表显里程')]/span/text()").get()
        registerdate = response.xpath("//div[@class='sp-car-xinxi']/ul/li[1]/span/text()").get()
        item["registerdate"] = registerdate.replace(' ', '').replace('\n', '').replace('\r', '') if registerdate else None
        geartype = response.xpath("//div[@class='sp-car-xinxi']/ul/li[3]/span/text()").get()
        item["geartype"] = geartype.replace(' ', '').replace('\n', '').replace('\r', '') if geartype else None
        item["output"] = response.xpath("//div[@class='sp-car-xinxi']/ul/li[4]/span/text()").get().replace(' ', '').replace('\n', '').replace('\r', '') if response.xpath("//div[@class='sp-car-xinxi']/ul/li[4]/span/text()").get() else None
        item["car_source"] = 'hry2car'
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["parsetime"] = item["grab_time"]
        item["pagetitle"] = response.xpath("//title/text()").get()
        item["url"] = response.url
        # item["change_times"] = response.xpath("//li[@class='iNew-hu']//i/text()").get()
        item["brand"] = response.xpath("//div[@class='qa-weizhi']/p/a[3]/text()").get()
        item["series"] = response.xpath("//div[@class='qa-weizhi']/p/a[4]/text()").get().split('二手')[1]
        item["city"] = response.xpath("//div[@class='qa-weizhi']/p/a[4]/text()").get().split('二手')[0]
        # item["registeryear"] = response.xpath("//dd[contains(text(),'首次上牌')]/preceding-sibling::dt/text()").get()
        guidepricetax = response.xpath("//*[@class='car-jiage-div']/p[1]/text()").get()
        item["guideprice"] = re.findall("新车指导价：(.*?)万", guidepricetax)[0]
        # publish_date = response.xpath("//div[contains(text(),'天前发布')]/text()").get().replace("天前发布", "")
        # if publish_date:
        #     item["post_time"] = (datetime.datetime.now() - datetime.timedelta(days=int(publish_date))).strftime(
        #         "%Y-%m-%d")
        sold_date = response.xpath("//*[@class='selldate']/text()").get()
        if sold_date:
            item["sold_date"] = sold_date.split('：')[1]
        item["yearchecktime"] = response.xpath("//ul[@class='z-info']/li[11]/div/text()").get()
        item["insurance2_date"] = response.xpath("//ul[@class='z-info']/li[10]/div/text()").get()
        item["change_times"] = response.xpath("//ul[@class='z-info']/li[7]/div/text()").get()
        item["desc"] = response.xpath("//p[@class='sp-car-explain']/text()").get()

        item["bodystyle"] = response.xpath("//span[contains(text(),'车身结构')]/following-sibling::span/text()").get()
        item["fueltype"] = response.xpath("//span[contains(text(),'燃料形式')]/following-sibling::span/text()").get()
        item["gear"] = response.xpath("//span[contains(text(),'变速箱')]/following-sibling::span/text()").get()
        item["maxps"] = response.xpath("//span[contains(text(),'最高车速')]/following-sibling::span/text()").get()
        item["level"] = response.xpath("//span[contains(text(),'级别')]/following-sibling::span/text()").get()
        # item["factoryname"] = response.xpath("//th[contains(text(),'生产厂商')]/following-sibling::td[1]/text()").get()
        # item["emission"] = response.xpath("//th[contains(text(),'排放标准')]/following-sibling::td[1]/text()").get()
        # item["output"] = response.xpath("//th[contains(text(),'排气量')]/following-sibling::td[1]/text()").get()

        # item["modelname"] = response.xpath("//span[contains(text(),'车型名称')]/following-sibling::span[1]/text()").get()
        # item["guideprice"] = response.xpath("//span[contains(text(),'厂商指导价')]/following-sibling::span[1]/text()").get()
        # item["factoryname"] = response.xpath("//th[contains(text(),'生产厂商')]/following-sibling::td[1]/text()").get()

        item["pagetime"] = 'zero'
        item["statusplus"] = item["carid"] + '-' + item["price1"]
        status = response.xpath("//div[@class='carDismounted']/text()").get()
        if status:
            item["status"] = 'sold'
        else:
            item["status"] = 'sale'
        yield item
        # print(item)
