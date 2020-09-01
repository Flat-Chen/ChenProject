# -*- coding: utf-8 -*-
import scrapy
from ganji.items import XcarItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import re
import logging

website ='xcar'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["xcar.com.cn"]
    start_urls = [
        "http://newcar.xcar.com.cn/price/"
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

    # family select
    def parse(self, response):
        for brandhref in response.xpath('//div[@class="container"]/table/tbody/tr'):
            brandname=brandhref.xpath('td[1]/div/a/span/text()').extract_first()
            brandid='pb'+str(brandhref.xpath('td[1]/div/a/@href').re('\d+')[0]) \
                if brandhref.xpath('td[1]/div/a/@href').re('\d+') else ''

            for factoryhref in brandhref.xpath('td[2]/div'):
                factoryname=factoryhref.xpath('p/a/text()').extract_first()
                factoryid = 'b'+str(factoryhref.xpath('p/a/@href').re('\d+')[0]) \
                    if factoryhref.xpath('p/a/@href').re('\d+') else ''

                for familyhref in factoryhref.xpath('ul/li/div/a'):
                    familyname = familyhref.xpath('@title').extract_first()
                    familyid = str(familyhref.xpath('@href').re('\d+')[0]) \
                        if familyhref.xpath('@href').re('\d+') else ''
                    href=familyhref.xpath('@href').extract_first()
                    url = response.urljoin(href)
                    metadata={"brandname":brandname,"brandid":brandid,
                              "factoryname":factoryname,"factoryid":factoryid,
                              "familyname": familyname, "familyid": familyid,}
                    yield scrapy.Request(url,meta={"metadata":metadata},callback= self.salemodel_parse)
        for i in range(1,self.carnum):
            urlbase="http://newcar.xcar.com.cn/m"+str(i)+"/config.htm"
            url = response.urljoin(href)
            yield scrapy.Request(url, meta={"metadata": "-"}, callback=self.parse_car)


    # model select
    def salemodel_parse(self, response):
        metadata=response.meta["metadata"]
        for href in response.xpath('//a[@onclick="clicklog(124707);"]/@href'):
            urlbase = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"metadata":metadata},callback=self.parse_car)
        if response.xpath('//a[@class="ps_stop_model_list"]'):
            for href in response.xpath('//a[@class="ps_stop_model_list"]/@data'):
                familyid=metadata["familyid"]
                urlbase = 'http://newcar.xcar.com.cn/auto/index.php?r=newcar/SeriseParentIndex/AjaxStopSaleModel&pserid='\
                          + familyid+'&year='+href.extract()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.salemodel_parse)

    # get car infor
    def parse_car(self, response):
        # count
        self.counts += 1
        logging.log(msg= "download              " + str(self.counts) + "                  items", level=logging.INFO)
        # item loader
        item = XcarItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()
        #carid
        item['carid'] = 'm'+ str(re.findall('\d+',response.url)[0]) if re.findall('\d+',response.url) else '-'
        carid=str(re.findall('\d+', response.url)[0]) if re.findall('\d+', response.url) else '-'
        # brandname familyname factoryname brandid familyid factoryid
        metadata =response.meta['metadata']
        if metadata=="-":
            item['brandname'] = ''
            item['brandid'] = ''
            item['familyname'] = response.xpath('//div[@class="place"]/a[3]/text()').extract_first() \
                if response.xpath('//div[@class="place"]/a[3]/text()') else '-'
            item['familyid'] = response.xpath('//div[@class="place"]/a[3]/@href').re('\d+')[0] \
                if response.xpath('//div[@class="place"]/a[3]/@href').re('\d+') else '-'
            factorynamexpath = '//td[id="bname_' + str(carid) + '"]/a/text()'
            factoryidxpath = '//td[id="bname_' + str(carid) + '"]/a/@href'
            item['factoryname'] = response.xpath(factorynamexpath).extract_first() \
                if response.xpath(factorynamexpath) else '-'
            item['factoryid'] = response.xpath(factoryidxpath).extract_first() \
                if response.xpath(factoryidxpath) else '-'
        else:
            item['brandname']=metadata['brandname']
            item['brandid'] = metadata['brandid']
            item['familyname'] = metadata['familyname']
            item['familyid'] = metadata['familyid']
            item['factoryname'] = metadata['factoryname']
            item['factoryid'] = metadata['factoryid']
        #salesdesc makeyear
        item['salesdesc'] = response.xpath('//h1/text()').extract_first() \
            if response.xpath('//h1/text()') else '-'
        item['makeyear'] = response.xpath('//span[@class="lt_f1"]/text()').re('\d+')[0] \
            if response.xpath('//span[@class="lt_f1"]/text()').re('\d+') else '-'
        # list value
        jsonlist = response.xpath('//tr')
        if jsonlist and carid!='-':
            namelist=['price','an_price','bname','type_name','disl_working_mpower','dynamic','speed_transtype',
                      'length_width_height','door_seat_frame','ear','mspeed','hatime','comfuel','ypolicy',
                      'length','width','height','wheelbase','weight','clearance','btread','ftread','frame',
                      'door','seat','oilbox','trunk','mtrunk','enginetype','disl','mdisl','working','cyarrange',
                      'cylinder','cylindernum','cr','valvegear','cylinderbore','journey','cylinderblock',
                      'cylinderhead','mhpower','mpower','mtorque','fuel','fuelno','sfueltype','envstand',
                      'stechnology','speed','transtype','tranname','drivetype','awdtype','mdifferentialtype',
                      'carstruc','hptype','fsustype_text','bsustype_text','fdifferentiallock','mdifferentiallock',
                      'rdifferentiallock','fbraketype','bbraketype','park','ftiresize','btiresize','sparetire',
                      'isdairbag','isfhairbag','isfsairbag','iskairbag','pedeairbag','isofix','istpmonitor',
                      'istpruning','isseatbeltti','iseanti','enginelock','iscclock','isrekey','baws','nightwork',
                      'isabs','isebd','iseba','isasr','isesp','hillassist','hdc','isuphillassist','isandstitch',
                      'deviatewar','iskbsus','issteesys','aba','iswindow','isarwindow','isspround','isaluhub',
                      'eletric_sdoor','electricdoor','rack','agrille','elecartrunk','isleasw','isswud','ismultisw',
                      'steelectrol','steewhmory','iswheelhot','isswshift','isassibc','isparkvideo','panorcamera',
                      'ispark','isascd','autcruise','isnokeyinto','isnokeysys','display','ishud','isleaseat',
                      'sportseat','isseatadj','isfseatadj','reseateletrol','iswaistadj','shouldersdj','thighsdj',
                      'iseseatmem','isseathot','isseatknead','chairmassage','secseatbadj','secseatfbwadj',
                      'isbseatlay','isbseatplay','thirdrowseat','isfarmrest','isbcup','isgps','isbluetooth',
                      'iscclcd','isblcd','humancomption','interservice','istv','audio_brand','aux','ismp3',
                      'isscd','ismcd','allcd','onedvd','ismdvd','is2audio','is4audio','is6audio','is8audio',
                      'isxelamp','isledlamp','isjglamp','ishfoglamp','dayrunlight','islampheiadj','isautohlamp',
                      'bendauxlig','isturnhlamp','islampclset','interatmlamp','isfewindow','isgnhand',
                      'ispreventionuv','fseat_pglass','isermirror','ishotrmirror','iseprmirror','ecm',
                      'ismemorymirror','isbssvisor','ishbsvisor','issvisordr','isinswiper','rwiper','isairc',
                      'isaairc','fseat_ac','isbsairo','istempdct','isairfilter','iscaricebox','other',]

            for name in namelist:
                if name in ['price','an_price','bname','type_name',]:
                    id = name + '_'+carid
                else:
                    id = 'm_' + name + '_' + carid
                xpathname='td[@id="'+id+'"]/text()'
                item[name]='|'.join(jsonlist.xpath(xpathname).extract()).strip() if jsonlist.xpath(xpathname) else '-'
        yield item