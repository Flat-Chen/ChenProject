# -*- coding: utf-8 -*-
import scrapy
from ganji.items import PcautoItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json

website ='pcauto'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["pcauto.com.cn"]
    start_urls = [
        "http://m.pcauto.com.cn/auto/"
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # brand select
    def parse(self, response):
        for href in response.xpath('//div[@class="box"]/ul/li/a'):
            urlbase = "http://price.pcauto.com.cn/auto/api/hcs/serial_group_list?bid=" + href.xpath('@data-id').extract_first()
            brandname=href.xpath('@title').extract_first()
            brandid = str(href.xpath('@data-id').extract_first())
            metadata={'brandname':brandname,'brandid':brandid}
            yield scrapy.Request(urlbase, meta={'metadata':metadata},callback=self.family_parse)

    # family select
    def family_parse(self, response):
        metadata =response.meta['metadata']
        data=json.loads(response.xpath('//p/text()').extract_first()[11:-1])
        for factorydata in data['manufacturers']:
            factoryname=factorydata['name']
            for familydata in factorydata['serials']:
                familyid =str(familydata['sgid'])
                familyname =familydata['sgname']
                metadata_family= dict({'factoryname':factoryname,'familyid':familyid,'familyname':familyname,},**metadata)
                urlbase = "http://price.pcauto.com.cn/sg" + familyid+'/config.html'
                yield scrapy.Request(urlbase, meta={'metadata': metadata_family}, callback=self.parse_car)

    # get car infor
    def parse_car(self, response):
        # item loader
        item = PcautoItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['datasave'] = response.xpath('//html').extract_first()
        #brandname factoryname familyname brandid familyid
        metadata =response.meta['metadata']
        if metadata:
            item['brandname']=metadata['brandname']
            item['factoryname'] = metadata['factoryname']
            item['familyname'] = metadata['familyname']
            item['brandid'] = 'nb'+metadata['brandid']
            item['familyid'] = 'sg'+metadata['familyid']
        # factoryid
        item['factoryid'] = 'b'+response.xpath('//div[@class="pos-mark"]/a[4]/@href').re('\d+')[0] \
            if response.xpath('//div[@class="pos-mark"]/a[4]/@href') else '-'
        # list value
        jsonlist = json.loads(response.xpath('//script[contains(text(),"config")]/text()').re(',"body": (.*?)};')[0]) \
                if response.xpath('//script[contains(text(),"config")]/text()').re(',"body": (.*?)};') else '-'
        #item['jsonsave']=jsonlist
        namelist={ u"基本参数-车型名称":"salesdesc",u"基本参数-厂商指导价(元)":"price",u"基本参数-厂商":"factoryname",
                   u"基本参数-级别":"level",u"基本参数-上市时间":"salemonth",u"基本参数-发动机":"motor",
                   u"基本参数-进气形式":"method",u"基本参数-最大马力(PS)":"maxps",u"基本参数-最大扭矩(N·m)":"maxnm",
                   u"基本参数-变速箱":"gear",u"基本参数-车身类型":"bodystyle",u"基本参数-长×宽×高(mm)":"lengthwh",
                   u"基本参数-轴距(mm)":"wheel",u"基本参数-最高车速(km/h)":"maxspeed",
                   u"基本参数-官方0-100km/h加速(s)":"accelerate",u"基本参数-实测0-100km/h加速(s)":"actualaccelerate",
                   u"基本参数-实测100-0km/h制动(m)":"actualstop",u"基本参数-工信部综合油耗(L/100km)":"petrol",
                   u"基本参数-整车质保":"warranty",u"车身-车身类型":"type",u"车身-长度(mm)":"length",
                   u"车身-宽度(mm)":"width",u"车身-高度(mm)":"height",u"车身-轴距(mm)":"wheel",
                   u"车身-前轮距(mm)":"frontwheel",u"车身-后轮距(mm)":"backwheel",u"车身-最小离地间隙(mm)":"liftoff_distance",
                   u"车身-车重(kg)":"weight",u"车身-车门数(个)":"doors",u"车身-座位数(个)":"seats",
                   u"车身-油箱容积(L)":"fuelvolumn",u"车身-行李厢容积(L)":"baggage",u"车身-行李厢最大容积(L)":"maxbaggage",
                   u"发动机-发动机型号":"motortype",u"发动机-排量(mL)":"cylinder",u"发动机-进气形式":"method1",
                   u"发动机-最大马力(PS)":"maxps1",u"发动机-最大功率(kW)":"maxpower",u"发动机-最大功率转速(rpm)":"maxrpm",
                   u"发动机-最大扭矩(N·m)":"maxnm1",u"发动机-最大扭矩转速(rpm)":"maxtorque",u"发动机-气缸排列形式":"lwv",
                   u"发动机-气缸数(个)":"lwvnumber",u"发动机-每缸气门数(个)":"valve",u"发动机-压缩比":"compress",
                   u"发动机-配气机构":"valve_gear",u"发动机-缸径(mm)":"cylinder_diameter",u"发动机-行程(mm)":"cylinder_travel",
                   u"发动机-发动机特有技术":"motortechnique",u"发动机-燃料形式":"fuletype",u"发动机-燃油标号":"fulevolumn",
                   u"发动机-供油方式":"fulemethod",u"发动机-缸盖材料":"cylinder_head_material",
                   u"发动机-缸体材料":"cylinder_body_material",u"发动机-排放标准":"emission",u"变速箱-简称":"geardesc",
                   u"变速箱-挡位个数":"gearnumber",u"变速箱-变速箱类型":"geartype",u"底盘转向-驱动方式":"driveway",
                   u"底盘转向-前悬挂类型":"frontgauge",u"底盘转向-后悬挂类型":"backgauge",u"底盘转向-转向助力类型":"assistanttype",
                   u"底盘转向-车体结构":"body_structure",u"车轮制动-前制动器类型":"frontbrake",u"车轮制动-后制动器类型":"backbrake",
                   u"车轮制动-驻车制动类型":"parking_brake_type",u"车轮制动-前轮胎规格":"frontwheel",
                   u"车轮制动-后轮胎规格":"backwheel",u"车轮制动-备胎规格":"sparewheel",u"越野性能-接近角(°)":"approach_angle",
                   u"越野性能-离去角(°)":"departure_angle",u"越野性能-纵向通过角(°)":"ramp_angle",
                   u"越野性能-最大爬坡度(%)/爬坡角度(°)":"climbing_angle",u"越野性能-最小离地间隙(mm)":"liftoff_distance1",
                   u"越野性能-最小转弯半径(m)":"turning_radius",u"越野性能-最大涉水深度(mm)":"wading_depth"}
        if jsonlist['items'][0]['ModelExcessIds']:
            listdata=[]
            itemdata=dict()
            for i in  jsonlist['items']:
                key= i['Item']+'-'+i['Name']
                k = 0
                if namelist.has_key(key):
                    for j in i['ModelExcessIds']:
                        tmpdata=dict()
                        name =namelist[key]
                        tmpdata[name]=j['Value']
                        if len(listdata) >k:
                            listdata[k]=dict(listdata[k],**tmpdata)
                        else:
                            tmpdata['carid'] = str(j['Id'])
                            listdata.append(tmpdata)
                        k+=1
            for i in listdata:
                # count
                self.counts += 1
                logging.log(msg="download              " + str(self.counts) + "                  items",level=logging.INFO)
                i['url'] = 'http://price.pcauto.com.cn/m'+i['carid']+'/'
                i['status'] = 'http://price.pcauto.com.cn/m'+i['carid']+'/'
                itemnew = PcautoItem()
                itemnew =dict(item,**i)
                yield itemnew

        else:
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            item['url'] = response.url
            item['status'] = response.url
            yield item

        for list_next in response.xpath('//div[@class="stopDrop"]/a/@href'):
            yield scrapy.Request(url=response.urljoin(list_next.extract()), meta={'metadata': metadata}, callback=self.parse_car)