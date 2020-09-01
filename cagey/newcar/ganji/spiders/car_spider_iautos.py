# -*- coding: utf-8 -*-
import scrapy
from ganji.items import iautosItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import json
import re

website ='iautos'
class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["iautos.cn"]
    start_urls=['http://www.iautos.cn/chexing/',]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 200000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # family select
    def parse(self, response):
        for i in xrange(self.carnum):
            url = 'http://www.iautos.cn/chexing/trim.asp?id=' + str(i)
            yield scrapy.Request(url, callback=self.parse_car)

    # get car infor
    def parse_car(self, response):
        if response.xpath('//html').extract_first().find(u'没有该车型')==-1:
            # item loader
            item = iautosItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['url'] = response.url
            item['status'] = response.url
            item['datasave'] = response.xpath('//html').extract_first()
            #brandname factoryname familyname brandid familyid
            # item['brandname']=metadata['brandname']
            # item['brandid'] = metadata['brandid']
            item['factoryname'] = response.xpath('//div[@id="bread"]/text()').extract()[2].replace('>>','').strip() \
                if len(response.xpath('//div[@id="bread"]/text()').extract())>=2 else '-'
            #item['factoryid']=metadata['factoryid']
            item['familyname'] = response.xpath('//div[@id="bread"]/a[3]/text()').extract_first().strip() \
                if response.xpath('//div[@id="bread"]/a[3]/text()').extract_first() else '-'
            item['familyid'] = response.xpath('//div[@id="bread"]/a[3]/@href').re('\d+')[0] \
                if response.xpath('//div[@id="bread"]/a[3]/@href').re('\d+') else '-'
            item['salesdesc'] = response.xpath('//div[@id="bread"]/text()').extract()[3].replace('>>','').strip() \
                if len(response.xpath('//div[@id="bread"]/text()').extract())>=3 else '-'
            item['price'] = response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"指导价")]/b/text()').extract_first() \
                if response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"指导价")]/b/text()') else '-'
            item['saleprice'] = response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"市场价")]/b/text()').extract_first() \
                if response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"市场价")]/b/text()') else '-'
            item['price1_north'] = response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"华北地区")]/b/text()').extract_first() \
                if response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"华北地区")]/b/text()') else '-'
            item['price1_east'] = response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"华东地区")]/b/text()').extract_first() \
                if response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"华东地区")]/b/text()') else '-'
            item['price1_south'] = response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"华南地区")]/b/text()').extract_first() \
                if response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"华南地区")]/b/text()') else '-'
            item['price1_west'] = response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"西南地区")]/b/text()').extract_first() \
                if response.xpath(u'//div[@class="carDetailRightTop"]/ul/li[contains(text(),"西南地区")]/b/text()') else '-'
            item['comments_good'] = response.xpath(u'//div[@class="carDp"]/ul/li/strong[contains(text(),"优点")]/../text()').extract_first().replace(u'\uff1a','').strip() \
                if response.xpath(u'//div[@class="carDp"]/ul/li/strong[contains(text(),"优点")]/../text()').extract_first() else '-'
            item['comments_bad'] = response.xpath(u'//div[@class="carDp"]/ul/li/strong[contains(text(),"缺点")]/../text()').extract_first().replace(u'\uff1a','').strip() \
                if response.xpath(u'//div[@class="carDp"]/ul/li/strong[contains(text(),"缺点")]/../text()').extract_first() else '-'
            item['desc'] = response.xpath('//div[@class="kssm"]/div/p/text()').extract_first().strip() \
                if response.xpath('//div[@class="kssm"]/div/p/text()').extract_first() else '-'
            #carlist
            car = dict()
            for keyinfo in response.xpath('//div[@class="jbxx"]/div/table/tr'):
                if len(keyinfo.xpath('td'))==2:
                    name=keyinfo.xpath('td/text()').extract_first().replace('.','').strip() if keyinfo.xpath('td/text()') else '-'
                    info=keyinfo.xpath('td/text()').extract()[1].replace('.','').strip() if len(keyinfo.xpath('td/text()'))>=2 else '-'
                    car=dict(car,**{name:info})
                elif len(keyinfo.xpath('td'))==4:
                    name1 = keyinfo.xpath('td/text()').extract_first().replace('.','').strip() if keyinfo.xpath('td/text()') else '-'
                    info1 = keyinfo.xpath('td/text()').extract()[1].replace('.','').strip() if len(keyinfo.xpath('td/text()')) >= 2 else '-'
                    name2 = keyinfo.xpath('td/text()').extract()[2].replace('.','').strip() if len(keyinfo.xpath('td/text()')) >= 3 else '-'
                    info2 = keyinfo.xpath('td/text()').extract()[3].replace('.','').strip() if len(keyinfo.xpath('td/text()')) >= 4 else '-'
                    car = dict(car, **{name1: info1,name2:info2})
            if car.has_key('1'):
                car.pop('1')
            namedict={u'款式名称':'salesdesc1',u'出厂时间':'produceyear',u'车型年款':'makeyear',u'排放标准':'emission',
                      u'车体形式':'bodystyle',u'前/后轮距(mm)':'frontwheel_backwheel',u'轴距(mm)':'wheel',
                      u'整备质量(kg)':'weight',u'油箱容积(l)':'fuelvolumn',u'行李箱容积(l)':'baggage',
                      u'车门数(含后车门)':'doors',u'接近角(°)':'approach_angle',u'长/宽/高(mm)':'lengthwh',
                      u'前/后悬长度(mm)':'frontgauge_backgauge_length',u'风阻系数(cd)':'drag_coef',
                      u'最大总质量(kg)':'maxload',u'最大行李箱容积(l)':'maxbaggage',
                      u'乘员数(含驾驶员)':'passengers',u'离去角(°)':'departure_angle',
                      u'发动机重要技术':'motortechnique',u'发动机描述':'motordesc',
                      u'发动机型号':'motortype',u'升功率(kw/l)':'powerL',u'压缩比':'compress',
                      u'行程(mm)':'cylinder_travel',u'每缸气门数':'valve',u'最大功率(kw(ps)/rpm)':'maxpower',
                      u'燃料类型标号':'fueltype',u'排气量(ml)':'cylinder',u'发动机放置方向':'lwv',
                      u'进气方式':'method',u'发动机生产厂家':'motorfactoryname',u'综合油耗(L/100km)':'petrol',
                      u'缸径(mm)':'cylinder_diameter',u'缸盖材料':'cylinder_head_material',
                      u'缸体材料':'cylinder_body_material',u'最大扭矩(nm/rpm)':'maxnm',u'燃油供给方式':'fuelmethod',
                      u'气缸数':'lwvnumber',u'发动机放置位置':'motor_position',u'冷却系统':'cooling_system',
                      u'变速器形式':'gear',u'驱动方式':'driveway',u'前悬架':'fronthang',u'前制动':'frontbrake',
                      u'变速器名称':'geardesc',u'前轮胎规格':'frontwheel',u'备胎规格':'sparewheel',
                      u'前轮毂材料':'fronthubtype',u'驱动轮胎宽度(mm)':'drive_width',u'驱动轮胎负荷指数':'drive_load',
                      u'驱动轮毂直径(英寸)':'drive_wheel',u'排档方式':'transmission_way',u'转向系统':'assistanttype',
                      u'后悬架':'backhang',u'后制动':'backbrake',u'整车平台':'platform',u'后轮胎规格':'backwheel',
                      u'备胎轮毂材料':'sparehubtype',u'后轮毂材料':'backhubtype',u'驱动轮胎扁平比(%)':'drive_flat',
                      u'驱动轮胎速度级别':'drive_speed',u'最高车速(km/h)':'maxspeed',u'最大爬坡度(%)':'max_grade_angel',
                      u'保修期':'warranty',u'0-100km/h加速时间(s)':'accelerate',u'安全气囊':'airbag',u'100km/h-0制动距离(m)':'brakelength',}
            for name in namedict.keys():
                if car.has_key(name):
                    name_en=namedict[name]
                    item[name_en]=car[name]
            item['jsonsave']=car
            # carother
            carinfors = dict()
            for keyinfo in response.xpath('//div[@class="gxhpzCon"]/table/tr'):
                if len(keyinfo.xpath('td')) == 2:
                    name = keyinfo.xpath('td[1]/text()').extract_first().replace('.', '').strip() \
                        if keyinfo.xpath('td[1]/text()') else '-'
                    info = str(keyinfo.xpath('td[2]/img/@src').extract_first()) \
                        if keyinfo.xpath('td[2]/img/@src') else '-'
                    if info == '-' or info == 'http://img4.iautos.cn/new_images/new_chexing/cha-icon.gif':
                        info = 'N'
                    else:
                        info = 'Y'
                    carinfors = dict(carinfors, **{name: info})
                elif len(keyinfo.xpath('td')) == 4:
                    name1 = keyinfo.xpath('td[1]/text()').extract_first().replace('.', '').strip() \
                        if keyinfo.xpath('td[1]/text()') else '-'
                    info1 = str(keyinfo.xpath('td[2]/img/@src').extract_first()) \
                        if keyinfo.xpath('td[2]/img/@src') else '-'
                    if info1 == '-' or info1 == 'http://img4.iautos.cn/new_images/new_chexing/cha-icon.gif':
                         info1 = 'N'
                    else:
                         info1 = 'Y'
                    name2 = keyinfo.xpath('td[3]/text()').extract_first().replace('.', '').strip() \
                        if keyinfo.xpath('td[3]/text()') else '-'
                    info2 = str(keyinfo.xpath('td[4]/img/@src').extract_first()) \
                        if keyinfo.xpath('td[4]/img/@src') else '-'
                    if info2 == '-' or info2 == 'http://img4.iautos.cn/new_images/new_chexing/cha-icon.gif':
                         info2 = 'N'
                    else:
                         info2 = 'Y'
                    carinfors = dict(carinfors, **{name1: info1, name2: info2})
            item['infors'] = carinfors
            yield item