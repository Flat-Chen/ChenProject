# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from usedcar_new.items import GanjiItem


class CarStreetSpider(scrapy.Spider):
    name = 'car_street'
    allowed_domains = ['auction.autostreets.com']
    start_urls = ['http://auction.autostreets.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQLDB_SERVER': '192.168.1.94',
        'MYSQLDB_PASS': 'Datauser@2017',
        'MYSQL_USER': 'dataUser94',
        'WEBSITE': 'car_street',
        'MYSQL_TABLE': 'car_street_online',
        'MYSQL_DB': 'usedcar_update',
        'CrawlCar_Num': 1000000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOADER_MIDDLEWARES': {
           # 'usedcar_new.middlewares.SeleniumIPMiddleware': 600,
           # 'usedcar_new.middlewares.ProxyMiddleware': 700,
           'scrapy.downloadermiddlewares.retry.RetryMiddleware': 800,
            },
        # 'ITEM_PIPELINES': {
        #     'usedcar_new.pipelines.GanjiPipeline': 300,
        #     },
    }

    def __init__(self, **kwargs):
        super(CarStreetSpider, self).__init__(**kwargs)
        self.city_list = []
        self.brand_list = []
        self.counts = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

    def start_requests(self):
        """
        """
        url = "http://auction.autostreets.com/no-haggle?pageNumber=1&s=desc&sb=selltime&cert=&ps=30"
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            dont_filter=True
            )

    def parse(self, response):
        page_num = response.xpath("//span[@class='color_505fb9']/../span[3]/text()").get()
        # print(page_num)
        for page in range(1, int(page_num)+1):
            url = f"http://auction.autostreets.com/no-haggle?pageNumber={page}&s=desc&sb=selltime&cert=&ps=30"
            yield scrapy.Request(
                url=url,
                callback=self.parse_list,
                headers=self.headers,
                dont_filter=True,
            )

    def parse_list(self, response):
        div_list = response.xpath("//*[@id='carRight']/div")
        for div in div_list:
            detail_url = div.xpath(".//a/@href").get()
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,

            )

    def parse_detail(self, response):
        item = GanjiItem()
        item["carid"] = response.url.split('/')[-1:][0]
        item["shortdesc"] = response.xpath("//div[@class='title']/h3/text()").get()
        item["price1"] = response.xpath("//div[@class='ckj1']/b/text()").get()
        item["mileage"] = response.xpath("//*[contains(text(),'表显里程')]/../p/text()").get()
        # item["change_times"] = response.xpath("//li[@class='iNew-hu']//i/text()").get()
        item["car_source"] = 'car_street'
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["parsetime"] = item["grab_time"]
        item["pagetitle"] = response.xpath("//title/text()").get()
        item["url"] = response.url
        item["brand"] = item["pagetitle"].split(' ')[0]
        try:
            item["series"] = item["pagetitle"].split(' ')[1] if '款' and 'T' and '厢' not in item["pagetitle"].split(" ")[1] else item["brand"]
        except:
            item["series"] = None
        item["registeryear"] = response.xpath("//*[contains(text(),'上牌日期')]/../p/text()").get()
        item["color"] = response.xpath("//*[contains(text(),'车辆颜色')]/../p/text()").get()
        # item["body"] = response.xpath("//*[contains(text(),'车身结构')]/../p/text()").get()
        # item["bodystyle"] = item["body"]
        # item["emission"] = "".join(response.xpath("//*[contains(text(),'排放标准')]/../p/text()").getall()).replace(" ", "").replace("\n", "")
        item["body"] = response.xpath("//*[contains(text(),'变速箱类型')]/../p/text()").get()
        item["output"] = response.xpath("//*[contains(text(),'排气量')]/../p/text()").get()
        item["usage"] = response.xpath("//*[contains(text(),'使用性质')]/../p/text()").get()
        item["insurance1_date"] = response.xpath("//*[contains(text(),'交强险到期')]/../p/text()").get()
        item["insurance2_date"] = response.xpath("//*[contains(text(),'年审有效期')]/../p/text()").get()
        item["city"] = response.xpath("//*[contains(text(),'车辆所在地')]/../p/text()").get()
        item["fueltype"] = response.xpath("//*[contains(text(),'燃油类型')]/../p/text()").get()
        item["desc"] = re.findall('html\(unescape\(\"(.*?)\"\)', response.text)[0] if len(re.findall('html\(unescape\(\"(.*?)\"\)', response.text))>0 else None
        # item["yearchecktime"] = response.xpath("//*[contains(text(),'质检时间')]/../p/text()").get().split("：")[1]
        item["post_time"] = response.xpath("//*[contains(text(),'质检时间')]/../p/text()").get().split("：")[1]
        item["carcard"] = response.xpath("//*[contains(text(),'行驶证')]/../p/text()").get()
        item["guidepricetax"] = response.xpath("//*[contains(text(),'新车价')]/b/text()").get().replace("\n", "").replace(" ", "")

        item["outer_sore"] = response.xpath("//*[contains(text(),'外观')]/../span/text()").get()
        item["inner_sore"] = response.xpath("//*[contains(text(),'内饰')]/../span/text()").get()
        item["road_score"] = response.xpath("//*[contains(text(),'发动机舱')]/../span/text()").get()
        item["safe_score"] = response.xpath("//*[contains(text(),'底盘')]/../span/text()").get()
        item["accident_score"] = response.xpath("//*[contains(text(),'骨架评级')]/../p/text()").get().replace("车况评分", "")
        item["totalgrade"] = response.xpath("//*[@class='score']/h4/text()").get()

        outer_desc_li_list = response.xpath("//h3[contains(text(),'外观损伤')]/..//span[@class='scar']/..")
        if outer_desc_li_list:
            outer_desc_list = []
            for outer_desc_li in outer_desc_li_list:
                outer_desc = dict()
                outer_desc["name"] = outer_desc_li.xpath("./p/text()").get()
                outer_desc["bug"] = outer_desc_li.xpath(".//ins/text()").get()
                outer_desc_list.append(outer_desc)
            item["outer_desc"] = json.dumps(outer_desc_list, ensure_ascii=False)

        inner_desc_li_list = response.xpath("//h3[contains(text(),'内饰损伤')]/..//span[@class='scar']/..")
        if inner_desc_li_list:
            inner_desc_list = []
            for inner_desc_li in inner_desc_li_list:
                inner_desc = dict()
                inner_desc["name"] = inner_desc_li.xpath("./p/text()").get()
                inner_desc["bug"] = inner_desc_li.xpath(".//ins/text()").get()
                inner_desc_list.append(inner_desc)
            item["inner_desc"] = json.dumps(inner_desc_list, ensure_ascii=False)

        totalcheck_desc_li_list = response.xpath("//span[contains(text(),'否')]/..")
        if totalcheck_desc_li_list:
            totalcheck_desc_list = []
            for totalcheck_desc_li in totalcheck_desc_li_list:
                totalcheck_desc = dict()
                totalcheck_desc["name"] = totalcheck_desc_li.xpath("./p/text()").get()
                totalcheck_desc["bug"] = totalcheck_desc_li.xpath("./span/text()").get()
                totalcheck_desc_list.append(totalcheck_desc)
            item["totalcheck_desc"] = json.dumps(totalcheck_desc_list, ensure_ascii=False)

        item["pagetime"] = 'zero'
        # item["guideprice"] = response.xpath("//span[@class='fc-org']/i/text()").get()
        item["statusplus"] = item["carid"]+'-'+item["price1"]
        item["status"] = item["statusplus"]
        item["datasave"] = response.xpath('//html').get()
        item["website"] = "car_street"
        # print(item)
        yield item
