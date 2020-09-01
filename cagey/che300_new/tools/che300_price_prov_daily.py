# #-*- coding: UTF-8 -*-
# from __future__ import division
#
# import scrapy
# from ..items import che300_price
# import time
# from hashlib import md5
# from SpiderInit import spider_original_Init
# from SpiderInit import spider_new_Init
# from SpiderInit import spider_update_Init
# from SpiderInit import dfcheck
# from SpiderInit import dffile
# from Car_spider_update import update
# import csv
# import datetime
# import json
#
# website ='che300_price_prov_daily_update_test'
# spidername_new = 'che300_price_prov_daily_new'
# spidername_update = 'che300_price_prov_daily_update_old'
# from scrapy.conf import settings
# update_code = settings["UPDATE_CODE"]
# #main
# class CarSpider(scrapy.Spider):
#     name = website
#     allowed_domains = ["che300.com"]
#     def __init__(self,part=0, parts=1,*args,**kwargs):
#         # args
#         super(CarSpider, self).__init__(*args, **kwargs)
#         # setting
#         self.tag = 'original'
#         self.counts = 0
#         self.carnum = 20000000
#         self.dbname = 'usedcar_evaluation'
#         # spider setting
#         spider_original_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         self.df = 'none'
#         self.fa = 'none'
#         self.part=int(part)
#         self.parts=int(parts)
#
#     #pro_city select
#     #brandselect
#     def start_requests(self):
#         #this month
#         #modellist
#         # C:\Users\Admin\Desktop
#         with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
#         # with open( 'C:\Users\Admin\Desktop/modellist.csv', 'rb') as csvfile:
#
#             reader = csv.DictReader(csvfile)
#             modellist = [row for row in reader]
#         step=len(modellist)/self.parts+1
#         starti = self.part * step
#         if self.part==self.parts-1:
#             step = len(modellist) - starti
#         #urllist
#         for model in modellist:
#             for year in range(int(model['min_reg_year']),int(model['max_reg_year'])+1):
#                 if year ==2020:
#                     month = str(time.strftime('%m', time.localtime()))
#                     shangpai_year = (time.strftime('%Y', time.localtime()))
#                     shangpai_time = int(shangpai_year) * 12 + int(month)
#                     index = int(month) % 3
#                     for i in range(12)[index:int(month):3]:
#                         car_time = int(year) * 12 + i + 1
#                         mile = (shangpai_time - car_time) * 1 / 6
#                         date =str(year)+'-'+str(i+1)
#                         url = 'https://dingjia.che300.com/app/EvalResult/allProvPrices?callback=jQuery18309705734921018707_1534391096144' + \
#                                "&brand=" + str(model['brandid']) + "&series=" + str(model['familyid']) + \
#                                "&model=" + str(model['salesdescid']) + "&regDate=" + date + "&mile=" + str(mile)
#                         meta = dict()
#                         meta['salesdescid'] = model['salesdescid']
#                         meta['regDate'] = date
#                         meta['mile'] = str(mile)
#                         print(meta)
#                         yield scrapy.Request(url=url, meta={"datainfo": meta}, callback=self.parse_allprov)
#                 else:
#                     month = str(time.strftime('%m', time.localtime()))
#                     shangpai_year = (time.strftime('%Y', time.localtime()))
#                     shangpai_time = int(shangpai_year) * 12 + int(month)
#                     index = int(month) % 3
#                     print(month,shangpai_year,shangpai_time,index)
#                     for i in range(12)[index::3]:
#                         car_time = int(year) * 12 + i + 1
#                         mile = (shangpai_time - car_time) * 1 / 6
#                         date =str(year)+'-'+str(i+1)
#                         url = 'https://dingjia.che300.com/app/EvalResult/allProvPrices?callback=jQuery18309705734921018707_1534391096144' + \
#                                "&brand=" + str(model['brandid']) + "&series=" + str(model['familyid']) + \
#                                "&model=" + str(model['salesdescid']) + "&regDate=" + date + "&mile=" + str(mile)
#                         meta = dict()
#                         meta['salesdescid'] = model['salesdescid']
#                         meta['regDate'] = date
#                         meta['mile'] = str(mile)
#                         print(meta)
#                         # headers = {
#                         #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                         #     'Accept-Language': 'en',
#                         #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
#                         # }
#                         # print meta
#                         yield scrapy.Request(url=url, meta={"datainfo": meta}, callback=self.parse_allprov)
#
#     def parse_allprov(self, response):
#         item = che300_price()
#         item = dict(item, **response.meta['datainfo'])
#         dffile(self.fa, response.url, self.tag)
#         item['url'] = response.url
#         item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#         if response.xpath('//p/text()'):
#             item['datasave'] = response.xpath('//p/text()').extract_first()
#             item['status'] = md5(item['datasave'].encode('utf-8')+item['url'] + "-" + update_code).hexdigest()
#             yield item
#
# # new
# class CarSpider_new(CarSpider):
#
#     # basesetting
#     name = spidername_new
#
#     def __init__(self,part=0, parts=1,*args,**kwargs):
#         # args
#         super(CarSpider_new, self).__init__(**kwargs)
#         # tag
#         self.tag = 'new'
#         # spider setting
#         self.df = spider_new_Init(
#             spidername=spidername_new,
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
#         self.fa = open(filename, "a")
#         self.part = int(part)
#         self.parts = int(parts)
#
# #update
# class CarSpider_update(CarSpider,update):
#
#     #basesetting
#     name = spidername_update
#
#     def __init__(self, part=0, parts=1, *args, **kwargs):
#         # load
#         super(CarSpider_update, self).__init__(**kwargs)
#         #settings
#         self.urllist = spider_update_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum
#         )
#         self.carnum = len(self.urllist)
#         self.tag='update'
#         self.part = int(part)
#         self.parts = int(parts)
#         #do
#         super(update, self).start_requests()
