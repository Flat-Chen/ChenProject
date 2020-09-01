# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import time
from copy import deepcopy

from usedcar_new.items import chesupaiItem


class ChesupaiSpider(scrapy.Spider):
    name = 'chesupai'
    # allowed_domains = ['chesupai.cn']
    # start_urls = ['http://chesupai.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(ChesupaiSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        # self.headers = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        self.city_list = ['https://www.chesupai.cn/list/anshun/', 'https://www.chesupai.cn/list/anshan/',
                          'https://www.chesupai.cn/list/anyang/', 'https://www.chesupai.cn/list/anqing/',
                          'https://www.chesupai.cn/list/ankang/', 'https://www.chesupai.cn/list/bj/',
                          'https://www.chesupai.cn/list/bazhong/', 'https://www.chesupai.cn/list/bijie/',
                          'https://www.chesupai.cn/list/baoding/', 'https://www.chesupai.cn/list/binzhou/',
                          'https://www.chesupai.cn/list/bengbu/', 'https://www.chesupai.cn/list/bozhou/',
                          'https://www.chesupai.cn/list/baotou/', 'https://www.chesupai.cn/list/baoji/',
                          'https://www.chesupai.cn/list/cq/', 'https://www.chesupai.cn/list/cd/',
                          'https://www.chesupai.cn/list/chaoyang/', 'https://www.chesupai.cn/list/changzhou/',
                          'https://www.chesupai.cn/list/chengde/', 'https://www.chesupai.cn/list/cangzhou/',
                          'https://www.chesupai.cn/list/cc/', 'https://www.chesupai.cn/list/chuzhou/',
                          'https://www.chesupai.cn/list/chifeng/', 'https://www.chesupai.cn/list/changzhi/',
                          'https://www.chesupai.cn/list/cs/', 'https://www.chesupai.cn/list/changde/',
                          'https://www.chesupai.cn/list/chenzhou/', 'https://www.chesupai.cn/list/chuxiong/',
                          'https://www.chesupai.cn/list/dg/', 'https://www.chesupai.cn/list/deyang/',
                          'https://www.chesupai.cn/list/dazhou/', 'https://www.chesupai.cn/list/dl/',
                          'https://www.chesupai.cn/list/dandong/', 'https://www.chesupai.cn/list/daqing/',
                          'https://www.chesupai.cn/list/dongying/', 'https://www.chesupai.cn/list/dezhou/',
                          'https://www.chesupai.cn/list/datong/', 'https://www.chesupai.cn/list/dali/',
                          'https://www.chesupai.cn/list/eerduosi/', 'https://www.chesupai.cn/list/ezhou/',
                          'https://www.chesupai.cn/list/enshi/', 'https://www.chesupai.cn/list/foshan/',
                          'https://www.chesupai.cn/list/fushun/', 'https://www.chesupai.cn/list/fz/',
                          'https://www.chesupai.cn/list/fuyang/', 'https://www.chesupai.cn/list/jxfuzhou/',
                          'https://www.chesupai.cn/list/gz/', 'https://www.chesupai.cn/list/guangyuan/',
                          'https://www.chesupai.cn/list/guangan/', 'https://www.chesupai.cn/list/gy/',
                          'https://www.chesupai.cn/list/gl/', 'https://www.chesupai.cn/list/ganzhou/',
                          'https://www.chesupai.cn/list/huizhou/', 'https://www.chesupai.cn/list/heyuan/',
                          'https://www.chesupai.cn/list/hz/', 'https://www.chesupai.cn/list/huzhou/',
                          'https://www.chesupai.cn/list/huaian/', 'https://www.chesupai.cn/list/handan/',
                          'https://www.chesupai.cn/list/hengshui/', 'https://www.chesupai.cn/list/hrb/',
                          'https://www.chesupai.cn/list/heze/', 'https://www.chesupai.cn/list/hf/',
                          'https://www.chesupai.cn/list/huainan/', 'https://www.chesupai.cn/list/huaibei/',
                          'https://www.chesupai.cn/list/hn/', 'https://www.chesupai.cn/list/nmg/',
                          'https://www.chesupai.cn/list/hanzhong/', 'https://www.chesupai.cn/list/huangshi/',
                          'https://www.chesupai.cn/list/huanggang/', 'https://www.chesupai.cn/list/hengyang/',
                          'https://www.chesupai.cn/list/huaihua/', 'https://www.chesupai.cn/list/jiangmen/',
                          'https://www.chesupai.cn/list/jieyang/', 'https://www.chesupai.cn/list/jiaxing/',
                          'https://www.chesupai.cn/list/jinhua/', 'https://www.chesupai.cn/list/jinzhou/',
                          'https://www.chesupai.cn/list/jiaozuo/', 'https://www.chesupai.cn/list/jilin/',
                          'https://www.chesupai.cn/list/jiamusi/', 'https://www.chesupai.cn/list/jn/',
                          'https://www.chesupai.cn/list/jining/', 'https://www.chesupai.cn/list/jincheng/',
                          'https://www.chesupai.cn/list/jinzhong/', 'https://www.chesupai.cn/list/jingzhou/',
                          'https://www.chesupai.cn/list/jingmen/', 'https://www.chesupai.cn/list/jingdezhen/',
                          'https://www.chesupai.cn/list/jiujiang/', 'https://www.chesupai.cn/list/jian/',
                          'https://www.chesupai.cn/list/kaifeng/', 'https://www.chesupai.cn/list/km/',
                          'https://www.chesupai.cn/list/luzhou/', 'https://www.chesupai.cn/list/leshan/',
                          'https://www.chesupai.cn/list/lishui/', 'https://www.chesupai.cn/list/liupanshui/',
                          'https://www.chesupai.cn/list/liaoyang/', 'https://www.chesupai.cn/list/lianyungang/',
                          'https://www.chesupai.cn/list/longyan/', 'https://www.chesupai.cn/list/langfang/',
                          'https://www.chesupai.cn/list/luoyang/', 'https://www.chesupai.cn/list/luohe/',
                          'https://www.chesupai.cn/list/linyi/', 'https://www.chesupai.cn/list/liaocheng/',
                          'https://www.chesupai.cn/list/luan/', 'https://www.chesupai.cn/list/liuzhou/',
                          'https://www.chesupai.cn/list/linfen/', 'https://www.chesupai.cn/list/lz/',
                          'https://www.chesupai.cn/list/loudi/', 'https://www.chesupai.cn/list/maoming/',
                          'https://www.chesupai.cn/list/meizhou/', 'https://www.chesupai.cn/list/mianyang/',
                          'https://www.chesupai.cn/list/meishan/', 'https://www.chesupai.cn/list/mudanjiang/',
                          'https://www.chesupai.cn/list/maanshan/', 'https://www.chesupai.cn/list/nanchong/',
                          'https://www.chesupai.cn/list/neijiang/', 'https://www.chesupai.cn/list/nb/',
                          'https://www.chesupai.cn/list/nj/', 'https://www.chesupai.cn/list/nantong/',
                          'https://www.chesupai.cn/list/nanping/', 'https://www.chesupai.cn/list/ningde/',
                          'https://www.chesupai.cn/list/nanyang/', 'https://www.chesupai.cn/list/nn/',
                          'https://www.chesupai.cn/list/nc/', 'https://www.chesupai.cn/list/panzhihua/',
                          'https://www.chesupai.cn/list/panjin/', 'https://www.chesupai.cn/list/putian/',
                          'https://www.chesupai.cn/list/pingdingshan/', 'https://www.chesupai.cn/list/puyang/',
                          'https://www.chesupai.cn/list/pingxiang/', 'https://www.chesupai.cn/list/qingyuan/',
                          'https://www.chesupai.cn/list/quzhou/', 'https://www.chesupai.cn/list/quanzhou/',
                          'https://www.chesupai.cn/list/qinhuangdao/', 'https://www.chesupai.cn/list/qiqihaer/',
                          'https://www.chesupai.cn/list/qd/', 'https://www.chesupai.cn/list/qinzhou/',
                          'https://www.chesupai.cn/list/qianjiang/', 'https://www.chesupai.cn/list/qujing/',
                          'https://www.chesupai.cn/list/rizhao/', 'https://www.chesupai.cn/list/sh/',
                          'https://www.chesupai.cn/list/sz/', 'https://www.chesupai.cn/list/shantou/',
                          'https://www.chesupai.cn/list/shanwei/', 'https://www.chesupai.cn/list/suining/',
                          'https://www.chesupai.cn/list/shaoxing/', 'https://www.chesupai.cn/list/sy/',
                          'https://www.chesupai.cn/list/su/', 'https://www.chesupai.cn/list/suqian/',
                          'https://www.chesupai.cn/list/sanming/', 'https://www.chesupai.cn/list/sjz/',
                          'https://www.chesupai.cn/list/sanmenxia/', 'https://www.chesupai.cn/list/shangqiu/',
                          'https://www.chesupai.cn/list/siping/', 'https://www.chesupai.cn/list/songyuan/',
                          'https://www.chesupai.cn/list/ahsuzhou/', 'https://www.chesupai.cn/list/sxyulin/',
                          'https://www.chesupai.cn/list/shiyan/', 'https://www.chesupai.cn/list/suizhou/',
                          'https://www.chesupai.cn/list/shaoyang/', 'https://www.chesupai.cn/list/shangrao/',
                          'https://www.chesupai.cn/list/tj/', 'https://www.chesupai.cn/list/zjtaizhou/',
                          'https://www.chesupai.cn/list/tieling/', 'https://www.chesupai.cn/list/jstaizhou/',
                          'https://www.chesupai.cn/list/tangshan/', 'https://www.chesupai.cn/list/taian/',
                          'https://www.chesupai.cn/list/tongling/', 'https://www.chesupai.cn/list/ty/',
                          'https://www.chesupai.cn/list/wenzhou/', 'https://www.chesupai.cn/list/wx/',
                          'https://www.chesupai.cn/list/wei/', 'https://www.chesupai.cn/list/weifang/',
                          'https://www.chesupai.cn/list/wuhu/', 'https://www.chesupai.cn/list/wuzhou/',
                          'https://www.chesupai.cn/list/weinan/', 'https://www.chesupai.cn/list/wh/',
                          'https://www.chesupai.cn/list/xj/', 'https://www.chesupai.cn/list/xuzhou/',
                          'https://www.chesupai.cn/list/xm/', 'https://www.chesupai.cn/list/xingtai/',
                          'https://www.chesupai.cn/list/xinxiang/', 'https://www.chesupai.cn/list/xuchang/',
                          'https://www.chesupai.cn/list/xinyang/', 'https://www.chesupai.cn/list/xuancheng/',
                          'https://www.chesupai.cn/list/xa/', 'https://www.chesupai.cn/list/xn/',
                          'https://www.chesupai.cn/list/xiangyang/', 'https://www.chesupai.cn/list/xiaogan/',
                          'https://www.chesupai.cn/list/xianning/', 'https://www.chesupai.cn/list/xiangtan/',
                          'https://www.chesupai.cn/list/xinyu/', 'https://www.chesupai.cn/list/yangjiang/',
                          'https://www.chesupai.cn/list/yunfu/', 'https://www.chesupai.cn/list/yibin/',
                          'https://www.chesupai.cn/list/yaan/', 'https://www.chesupai.cn/list/yingkou/',
                          'https://www.chesupai.cn/list/yancheng/', 'https://www.chesupai.cn/list/yangzhou/',
                          'https://www.chesupai.cn/list/yantai/', 'https://www.chesupai.cn/list/gxyulin/',
                          'https://www.chesupai.cn/list/yangquan/', 'https://www.chesupai.cn/list/yuncheng/',
                          'https://www.chesupai.cn/list/yc/', 'https://www.chesupai.cn/list/yanan/',
                          'https://www.chesupai.cn/list/yichang/', 'https://www.chesupai.cn/list/yueyang/',
                          'https://www.chesupai.cn/list/yongzhou/', 'https://www.chesupai.cn/list/yiyang/',
                          'https://www.chesupai.cn/list/jxyichun/', 'https://www.chesupai.cn/list/yuxi/',
                          'https://www.chesupai.cn/list/zhuhai/', 'https://www.chesupai.cn/list/zhongshan/',
                          'https://www.chesupai.cn/list/zhanjiang/', 'https://www.chesupai.cn/list/zhaoqing/',
                          'https://www.chesupai.cn/list/zigong/', 'https://www.chesupai.cn/list/ziyang/',
                          'https://www.chesupai.cn/list/zunyi/', 'https://www.chesupai.cn/list/zhenjiang/',
                          'https://www.chesupai.cn/list/zhangzhou/', 'https://www.chesupai.cn/list/zz/',
                          'https://www.chesupai.cn/list/zhoukou/', 'https://www.chesupai.cn/list/zhumadian/',
                          'https://www.chesupai.cn/list/zibo/', 'https://www.chesupai.cn/list/zaozhuang/',
                          'https://www.chesupai.cn/list/zhuzhou/', 'https://www.chesupai.cn/list/zhaotong/']

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'chesupai_online',
        'WEBSITE': 'chesupai',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'chesupai_online',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.1.92:6379/2',
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.GanjiPipeline': 300,
        },

    }

    def start_requests(self):
        # url = "http://www.chesupai.cn/index/"
        for url in self.city_list:
            yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        print(response.url)
        item = chesupaiItem()
        li_list = response.xpath("//div[@class='w hide']/ul/li")
        for li in li_list:
            brand_url = li.xpath("./p[@class='l-name']/a/@href").get()
            carid = brand_url[-7:]
            detail_url = f'http://api.chesupai.cn/customer/detail/info?id={carid}'
            item["url"] = brand_url
            yield scrapy.Request(
                 url=detail_url,
                 callback=self.parse_detail_url,
                 meta={"item": item},
                 dont_filter=True,
            )
        # 翻页
        next_url = response.xpath("//a[@class='next']/@href").get()
        if next_url is not None:
            next_url = "http://www.chesupai.cn" + next_url
            # print(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={"item": deepcopy(item)},
                dont_filter=True
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        data = json.loads(response.text)["data"]
        detailInfo = data["detailInfo"]
        evaluateInfo = data["evaluateInfo"]
        basicInfo = data["basicInfo"]
        item["shortdesc"] = detailInfo["title"]
        item["carid"] = detailInfo["id"]
        item["city"] = detailInfo["address"]
        try:
            s = re.findall('(\D\S.*?) .*', item["shortdesc"])[0]
            pattern = re.compile('[0-9A-Z]+')
            if pattern.findall(s):
                item["brand"] = re.findall('(.*?)[a-zA-Z1-9]', item["shortdesc"])[0]
                if len(item["brand"]) == 0:
                    item["brand"] = re.findall('(\D\S.*?) .*', item["shortdesc"])[0]
            else:
                item["brand"] = re.findall('(\D\S.*?) .*', item["shortdesc"])[0]
        except:
            item["brand"] = None

        item["car_source"] = "chesupai"
        item["status"] = 'sale'
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["pagetime"] = "zero"
        item["pagetitle"] = item["shortdesc"]
        series = re.findall('\s(\S.*?) .*', item["pagetitle"])[0]
        if '款' in series:
            item["series"] = re.findall('(\S.*?) .*', item["pagetitle"])[0]
        else:
            item["series"] = re.findall('\s(\S.*?) .*', item["pagetitle"])[0]
        for info in basicInfo:
            if '上牌日期' in info["key"]:
                item["registeryear"] = info['val']
                item["registerdate"] = info['val']
            elif '表显里程' in info["key"]:
                item["mileage"] = info['val']
            elif '排放标准' in info["key"]:
                item["emission"] = info['val']
            elif '过户次数' in info["key"]:
                item["change_times"] = info['val']
            elif '车辆性质' in info["key"]:
                item["usage"] = info['val']
            elif '燃料类型' in info["key"]:
                item["fueltype"] = info['val']
            elif '交强险到期' in info["key"]:
                item["insurance1_date"] = info['val']
            elif '商业险到期' in info["key"]:
                item["insurance2_date"] = info['val']
            elif '年检到期' in info["key"]:
                item["yearchecktime"] = info['val']
            elif '车身颜色' in info["key"]:
                item["color"] = info['val']
            elif '变速箱' in info["key"]:
                item["geartype"] = info['val']
            elif '驱动方式' in info["key"]:
                item["level"] = info['val']
            elif '车身结构' in info["key"]:
                item["body"] = info['val']
            elif '出厂时间' in info["key"]:
                item["makeyear"] = info['val']
        item["produceyear"] = item["makeyear"]
        item["generation"] = item["makeyear"]
        output = re.findall('\d\.\d[LT]', item["pagetitle"])
        if len(output) > 0:
            item["output"] = output[0]
        else:
            item["output"] = None
        item["totalcheck_desc"] = evaluateInfo["conclusion"]
        item["totalgrade"] = evaluateInfo["score"]
        for bug in evaluateInfo["evaluate"]:
            if '主架构' in bug["name"]:
                if bug["errorNumber"] != '0':
                    new_bug = []
                    for error in bug["errorPoint"]:
                        error_dic = {}
                        error_dic["name"] = error["name"]
                        error_dic["error"] = error["error"]
                        new_bug.append(error_dic)
                    item["accident_desc"] = json.dumps(new_bug, ensure_ascii=False)
            elif '外观' in bug["name"]:
                if bug["errorNumber"] is not "0":
                    new_bug = []
                    for error in bug["errorPoint"]:
                        error_dic = {}
                        error_dic["name"] = error["name"]
                        error_dic["error"] = error["error"]
                        new_bug.append(error_dic)
                    item["outer_desc"] = json.dumps(new_bug, ensure_ascii=False)
            elif '内饰' in bug["name"]:
                if bug["errorNumber"] is not "0":
                    new_bug = []
                    for error in bug["errorPoint"]:
                        error_dic = {}
                        error_dic["name"] = error["name"]
                        error_dic["error"] = error["error"]
                        new_bug.append(error_dic)
                    item["safe_desc"] = json.dumps(new_bug, ensure_ascii=False)
            elif '路试' in bug["name"]:
                if bug["errorNumber"] is not "0":
                    new_bug = []
                    for error in bug["errorPoint"]:
                        error_dic = {}
                        error_dic["name"] =  error["name"]
                        error_dic["error"] = error["error"]
                        new_bug.append(error_dic)
                    item["road_desc"] = json.dumps(new_bug, ensure_ascii=False)
        item["status"] = 'sale'
        carid = item["carid"]
        url = f"http://www.chesupai.cn/ajax/?act=getBidInfo&source_id={carid}"
        yield scrapy.Request(
            url=url,
            callback=self.parse_price,
            meta={"item": deepcopy(item)},
            dont_filter=True
        )

    def parse_price(self, response):
        item = response.meta["item"]
        data = json.loads(response.body)
        if "last_bid" in data:
            # 当前投标价格
            item["price1"] = data["last_bid"]["amount"]
            # 最后一次投标时间
            item["post_time"] = data["last_bid"]["timeFormat"]
            item['statusplus'] = item["url"] + "-" + str(item["price1"])
            item["carid"] = item["carid"] + 'x'
            item['parsetime'] = item['grab_time']
            yield item
            # print(item)
        else:
            pass
