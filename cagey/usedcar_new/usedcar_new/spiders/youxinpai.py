# -*- coding: utf-8 -*-
import scrapy
import time
import redis
import re
import json

from usedcar_new.items import GanjiItem

# redis_cli = redis.Redis('127.0.0.1', port=6379, db=1)
redis_cli = redis.Redis('192.168.1.241', port=6379, db=3)
re_cookie = redis_cli.get('youxinpai_cookies').decode('utf-8')
cookies = {i.split("=")[0]: i.split("=")[1] for i in re_cookie.split(";")}


website = 'youxinpai'


class YouxinpaiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['youxinpai.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YouxinpaiSpider, self).__init__(**kwargs)
        self.counts = 0
        self.cookie = cookies
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            , 'Cookie': '{}'.format(cookies)
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_PORT': '3306',
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_USER': 'dataUser94',
        'MYSQL_PWD': '94dataUser@2020',
        # 'MYSQL_SERVER': '127.0.0.1',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'youxinpai_online',
        'WEBSITE': 'youxinpai',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'people_zb',
        'MONGODB_COLLECTION': 'youxinpai_online',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://i.youxinpai.com/AjaxObjectPage/SellCarTypePageTrade.ashx?carAreaID=40"
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        url = "http://i.youxinpai.com/AjaxObjectPage/SellCarTypePageTrade.ashx?carAreaID=40"
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_1,
            dont_filter=True
        )

    def parse_1(self, response):
        print("-" * 100)
        for href in response.xpath('//dd/a'):
            brandid = href.xpath('@id').re('\d+')[0] if href.xpath('@id').re('\d+') else '-'
            brandname = href.xpath('text()').extract_first()
            urlbase = 'http://i.youxinpai.com/AjaxObjectPage/SellCarTypePageTrade.ashx?carProducerID=' + brandid
            metadata = {'brandid': brandid, 'brandname': brandname}
            yield scrapy.Request(url=urlbase, headers=self.headers, meta={'metadata': metadata},
                                 callback=self.parse_series)

    def parse_series(self, response):
        # print("&"*100)
        for href in response.xpath('//ul/li/a'):
            familyid = href.xpath('@id').re('\d+')[0] if href.xpath('@id').re('\d+') else '-'
            familyname = href.xpath('text()').extract_first()
            metadata = response.meta['metadata']
            brandid = metadata['brandid']
            metadata = dict({'familyid': familyid, 'familyname': familyname}, **metadata)
            urlbase = 'http://i.youxinpai.com/TradeManage/TradeList.aspx?masterBrand=' + brandid + '&serial=' + familyid
            # print(urlbase)
            yield scrapy.Request(
                url=urlbase,
                cookies=self.cookie,
                headers=self.headers,
                meta={'metadata': metadata, 'tag': 'series'},
                callback=self.parse_car,
                dont_filter=True
            )

    def parse_car(self, response):
        print("*" * 100)
        print(response.url)
        # print(response.text)
        for href in response.xpath('//tr[@class="list-li"]'):
            status = href.xpath('td[3]/input/@requesttype')
            status = "".join(status.re('\d+')) if status else "zero"

            print(status)
            self.counts += 1
            datasave1 = response.meta['metadata']

            # key and status (sold or sale, price,time)
            datetime = href.xpath('td[1]/text()')
            datetime = '20' + "-".join(datetime.re('\d+')) if datetime else "zero"

            # item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = status
            item['pagetime'] = datetime
            item['datasave'] = href.extract()

            item['shortdesc'] = href.xpath('.//td[3]/@title').extract_first()
            registerdate = href.xpath('.//td[7]/text()').extract_first()
            item['registerdate'] = '20' + '-'.join(re.findall(r'\d+', registerdate))
            item['price1'] = href.xpath('.//td[6]/text()').extract_first()
            item['mileage'] = href.xpath('.//td[8]/text()').extract_first()
            item['usage'] = href.xpath('.//td[10]/text()').extract_first()
            item['color'] = href.xpath('.//td[5]/text()').extract_first()
            item['city'] = href.xpath('.//td[2]/text()').extract_first()
            item['totalgrade'] = href.xpath('.//td[4]/text()').extract_first()
            item['gear'] = href.xpath('.//td[9]/text()').extract_first()

            # extra
            item['brand'] = datasave1['brandname']
            item['series'] = datasave1['familyname']

            yield item
            # print(item)