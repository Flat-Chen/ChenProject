# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# class Che360Spider(CrawlSpider):
from kache.items import che360Item


class Che360Spider(scrapy.Spider):
    name = 'che360'
    # allowed_domains = ['tao.360che.com']
    start_urls = ['https://tao.360che.com/1.html']

    def __init__(self):
        super(Che360Spider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.city_list = ['https://tao.360che.com/ali/', 'https://tao.360che.com/aba/', 'https://tao.360che.com/anshanshi/', 'https://tao.360che.com/anqingshi/', 'https://tao.360che.com/anyangshi/', 'https://tao.360che.com/anshunshi/', 'https://tao.360che.com/ankangshi/', 'https://tao.360che.com/akesu/', 'https://tao.360che.com/aletai/', 'https://tao.360che.com/alashanmeng/', 'https://tao.360che.com/alaershi/', 'https://tao.360che.com/baoting/', 'https://tao.360che.com/baisha/', 'https://tao.360che.com/bijie/', 'https://tao.360che.com/baodingshi/', 'https://tao.360che.com/baiyinshi/', 'https://tao.360che.com/baojishi/', 'https://tao.360che.com/baoshanshi/', 'https://tao.360che.com/bazhongshi/', 'https://tao.360che.com/baiseshi/', 'https://tao.360che.com/beijingshi/', 'https://tao.360che.com/binzhoushi/', 'https://tao.360che.com/bozhoushi/', 'https://tao.360che.com/bangbushi/', 'https://tao.360che.com/baichengshi/', 'https://tao.360che.com/baishanshi/', 'https://tao.360che.com/benxishi/', 'https://tao.360che.com/baotoushi/', 'https://tao.360che.com/beihaishi/', 'https://tao.360che.com/boertala/', 'https://tao.360che.com/bayinguoleng/', 'https://tao.360che.com/bayannaoershi/', 'https://tao.360che.com/changjiang/', 'https://tao.360che.com/changji/', 'https://tao.360che.com/changdu/', 'https://tao.360che.com/chuxiong/', 'https://tao.360che.com/chenzhoushi/', 'https://tao.360che.com/chengmaixian/', 'https://tao.360che.com/chengdushi/', 'https://tao.360che.com/chongqingshi/', 'https://tao.360che.com/chongzuoshi/', 'https://tao.360che.com/chaozhoushi/', 'https://tao.360che.com/chengdeshi/', 'https://tao.360che.com/cangzhoushi/', 'https://tao.360che.com/changshashi/', 'https://tao.360che.com/chizhoushi/', 'https://tao.360che.com/chaohushi/', 'https://tao.360che.com/chuzhoushi/', 'https://tao.360che.com/changzhoushi/', 'https://tao.360che.com/changchunshi/', 'https://tao.360che.com/chaoyangshi/', 'https://tao.360che.com/chifengshi/', 'https://tao.360che.com/changzhishi/', 'https://tao.360che.com/changdeshi/', 'https://tao.360che.com/dehong/', 'https://tao.360che.com/diqing/', 'https://tao.360che.com/dali/', 'https://tao.360che.com/datongshi/', 'https://tao.360che.com/dazhoushi/', 'https://tao.360che.com/dongfangshi/', 'https://tao.360che.com/danzhoushi/', 'https://tao.360che.com/dingxishi/', 'https://tao.360che.com/deyangshi/', 'https://tao.360che.com/dalianshi/', 'https://tao.360che.com/dongshi/', 'https://tao.360che.com/dezhoushi/', 'https://tao.360che.com/dongyingshi/', 'https://tao.360che.com/daqingshi/', 'https://tao.360che.com/dandongshi/', 'https://tao.360che.com/dinganxian/', 'https://tao.360che.com/daxinganling/', 'https://tao.360che.com/enshi/', 'https://tao.360che.com/ezhoushi/', 'https://tao.360che.com/eerduosishi/', 'https://tao.360che.com/fushunshi/', 'https://tao.360che.com/fuxinshi/', 'https://tao.360che.com/fuyangshi/', 'https://tao.360che.com/fuzhoushi/', 'https://tao.360che.com/fz/', 'https://tao.360che.com/foshanshi/', 'https://tao.360che.com/fangchenggangshi/', 'https://tao.360che.com/gannan/', 'https://tao.360che.com/ganzi/', 'https://tao.360che.com/guoluo/', 'https://tao.360che.com/ganzhoushi/', 'https://tao.360che.com/guangzhoushi/', 'https://tao.360che.com/guilinshi/', 'https://tao.360che.com/guigangshi/', 'https://tao.360che.com/guangyuanshi/', 'https://tao.360che.com/guanganshi/', 'https://tao.360che.com/guiyangshi/', 'https://tao.360che.com/guyuanshi/', 'https://tao.360che.com/hetian/', 'https://tao.360che.com/hami/', 'https://tao.360che.com/haixi/', 'https://tao.360che.com/hainan/', 'https://tao.360che.com/huangnan/', 'https://tao.360che.com/haibei/', 'https://tao.360che.com/haidong/', 'https://tao.360che.com/honghe/', 'https://tao.360che.com/heyuanshi/', 'https://tao.360che.com/huaihuashi/', 'https://tao.360che.com/huizhoushi/', 'https://tao.360che.com/hanzhongshi/', 'https://tao.360che.com/hezhoushi/', 'https://tao.360che.com/hechishi/', 'https://tao.360che.com/haikoushi/', 'https://tao.360che.com/huanggangshi/', 'https://tao.360che.com/hengyangshi/', 'https://tao.360che.com/handanshi/', 'https://tao.360che.com/hengshuishi/', 'https://tao.360che.com/huzhoushi/', 'https://tao.360che.com/hegangshi/', 'https://tao.360che.com/heiheshi/', 'https://tao.360che.com/huaianshi/', 'https://tao.360che.com/hebishi/', 'https://tao.360che.com/hangzhoushi/', 'https://tao.360che.com/hefeishi/', 'https://tao.360che.com/huainanshi/', 'https://tao.360che.com/huaibeishi/', 'https://tao.360che.com/huangshanshi/', 'https://tao.360che.com/hezeshi/', 'https://tao.360che.com/huangshishi/', 'https://tao.360che.com/haerbinshi/', 'https://tao.360che.com/huludaoshi/', 'https://tao.360che.com/hulunbeiershi/', 'https://tao.360che.com/huhehaoteshi/', 'https://tao.360che.com/jinchengshi/', 'https://tao.360che.com/jiningshi/', 'https://tao.360che.com/jiyuanshi/', 'https://tao.360che.com/jiuquanshi/', 'https://tao.360che.com/jinchangshi/', 'https://tao.360che.com/jieyangshi/', 'https://tao.360che.com/jiangmenshi/', 'https://tao.360che.com/jingzhoushi/', 'https://tao.360che.com/jingmenshi/', 'https://tao.360che.com/jiaozuoshi/', 'https://tao.360che.com/jinanshi/', 'https://tao.360che.com/jinzhongshi/', 'https://tao.360che.com/jianshi/', 'https://tao.360che.com/jiujiangshi/', 'https://tao.360che.com/jinhuashi/', 'https://tao.360che.com/jiaxingshi/', 'https://tao.360che.com/jixishi/', 'https://tao.360che.com/jilinshi/', 'https://tao.360che.com/jinzhoushi/', 'https://tao.360che.com/jiyuanshi/', 'https://tao.360che.com/jingdezhenshi/', 'https://tao.360che.com/jiamusishi/', 'https://tao.360che.com/jiayuguanshi/', 'https://tao.360che.com/kashi/', 'https://tao.360che.com/kaifengshi/', 'https://tao.360che.com/kunmingshi/', 'https://tao.360che.com/kezilesu/', 'https://tao.360che.com/kelamayishi/', 'https://tao.360che.com/lingshui/', 'https://tao.360che.com/ledong/', 'https://tao.360che.com/linxia/', 'https://tao.360che.com/linzhi/', 'https://tao.360che.com/liangshan/', 'https://tao.360che.com/laibinshi/', 'https://tao.360che.com/lingaoxian/', 'https://tao.360che.com/longnanshi/', 'https://tao.360che.com/lanzhoushi/', 'https://tao.360che.com/lasashi/', 'https://tao.360che.com/lincangshi/', 'https://tao.360che.com/lijiangshi/', 'https://tao.360che.com/leshanshi/', 'https://tao.360che.com/luzhoushi/', 'https://tao.360che.com/langfangshi/', 'https://tao.360che.com/linfenshi/', 'https://tao.360che.com/loudishi/', 'https://tao.360che.com/luoheshi/', 'https://tao.360che.com/luoyangshi/', 'https://tao.360che.com/liaochengshi/', 'https://tao.360che.com/linyishi/', 'https://tao.360che.com/laiwushi/', 'https://tao.360che.com/longyanshi/', 'https://tao.360che.com/liuanshi/', 'https://tao.360che.com/lishuishi/', 'https://tao.360che.com/liaoyuanshi/', 'https://tao.360che.com/liaoyangshi/', 'https://tao.360che.com/lvliangshi/', 'https://tao.360che.com/liuzhoushi/', 'https://tao.360che.com/liupanshuishi/', 'https://tao.360che.com/lianyungangshi/', 'https://tao.360che.com/maomingshi/', 'https://tao.360che.com/meizhoushi/', 'https://tao.360che.com/mianyangshi/', 'https://tao.360che.com/meishanshi/', 'https://tao.360che.com/mudanjiangshi/', 'https://tao.360che.com/maanshanshi/', 'https://tao.360che.com/nujiang/', 'https://tao.360che.com/naqu/', 'https://tao.360che.com/nanjingshi/', 'https://tao.360che.com/nantongshi/', 'https://tao.360che.com/ningboshi/', 'https://tao.360che.com/nanpingshi/', 'https://tao.360che.com/ningdeshi/', 'https://tao.360che.com/nanchangshi/', 'https://tao.360che.com/nanyangshi/', 'https://tao.360che.com/nanningshi/', 'https://tao.360che.com/neijiangshi/', 'https://tao.360che.com/nanchongshi/', 'https://tao.360che.com/nanshaqundao/', 'https://tao.360che.com/panjinshi/', 'https://tao.360che.com/putianshi/', 'https://tao.360che.com/pingxiangshi/', 'https://tao.360che.com/puyangshi/', 'https://tao.360che.com/pingliangshi/', 'https://tao.360che.com/pingdingshanshi/', 'https://tao.360che.com/panzhihuashi/', 'https://tao.360che.com/qiongzhong/', 'https://tao.360che.com/qiannan/', 'https://tao.360che.com/quzhoushi/', 'https://tao.360che.com/quanzhoushi/', 'https://tao.360che.com/qingdaoshi/', 'https://tao.360che.com/qingyuanshi/', 'https://tao.360che.com/qinzhoushi/', 'https://tao.360che.com/qianxinan/', 'https://tao.360che.com/qiandongnan/', 'https://tao.360che.com/qujingshi/', 'https://tao.360che.com/qingyangshi/', 'https://tao.360che.com/qionghaishi/', 'https://tao.360che.com/qianjiangshi/', 'https://tao.360che.com/qinhuangdaoshi/', 'https://tao.360che.com/qitaiheshi/', 'https://tao.360che.com/qiqihaershi/', 'https://tao.360che.com/rizhaoshi/', 'https://tao.360che.com/rikaze/', 'https://tao.360che.com/shannan/', 'https://tao.360che.com/shuozhoushi/', 'https://tao.360che.com/simaoshi/', 'https://tao.360che.com/suiningshi/', 'https://tao.360che.com/sanyashi/', 'https://tao.360che.com/shanweishi/', 'https://tao.360che.com/shantoushi/', 'https://tao.360che.com/shenshi/', 'https://tao.360che.com/shaoguanshi/', 'https://tao.360che.com/shaoyangshi/', 'https://tao.360che.com/suizhoushi/', 'https://tao.360che.com/shiyanshi/', 'https://tao.360che.com/shangqiushi/', 'https://tao.360che.com/shangluoshi/', 'https://tao.360che.com/sanmingshi/', 'https://tao.360che.com/sz/', 'https://tao.360che.com/shaoxingshi/', 'https://tao.360che.com/suqianshi/', 'https://tao.360che.com/suzhoushi/', 'https://tao.360che.com/shanghaishi/', 'https://tao.360che.com/suihuashi/', 'https://tao.360che.com/songyuanshi/', 'https://tao.360che.com/sipingshi/', 'https://tao.360che.com/shenyangshi/', 'https://tao.360che.com/shangraoshi/', 'https://tao.360che.com/shizuishanshi/', 'https://tao.360che.com/shihezishi/', 'https://tao.360che.com/shijiazhuangshi/', 'https://tao.360che.com/sanmenxiashi/', 'https://tao.360che.com/shuangyashanshi/', 'https://tao.360che.com/shennongjialinqu/', 'https://tao.360che.com/tacheng/', 'https://tao.360che.com/tongren/', 'https://tao.360che.com/tianjinshi/', 'https://tao.360che.com/tangshanshi/', 'https://tao.360che.com/tunchangxian/', 'https://tao.360che.com/tulufan/', 'https://tao.360che.com/tianshuishi/', 'https://tao.360che.com/tongchuanshi/', 'https://tao.360che.com/taianshi/', 'https://tao.360che.com/tonglingshi/', 'https://tao.360che.com/taizhoushi/', 'https://tao.360che.com/tz/', 'https://tao.360che.com/tonghuashi/', 'https://tao.360che.com/tielingshi/', 'https://tao.360che.com/tongliaoshi/', 'https://tao.360che.com/taiyuanshi/', 'https://tao.360che.com/tianmenshi/', 'https://tao.360che.com/tiemenguanshi/', 'https://tao.360che.com/tumushukeshi/', 'https://tao.360che.com/wenshan/', 'https://tao.360che.com/wuzhoushi/', 'https://tao.360che.com/wanningshi/', 'https://tao.360che.com/wenchangshi/', 'https://tao.360che.com/wuzhongshi/', 'https://tao.360che.com/wuweishi/', 'https://tao.360che.com/weinanshi/', 'https://tao.360che.com/wuhaishi/', 'https://tao.360che.com/wuhanshi/', 'https://tao.360che.com/weihaishi/', 'https://tao.360che.com/weifangshi/', 'https://tao.360che.com/wuhushi/', 'https://tao.360che.com/wenzhoushi/', 'https://tao.360che.com/wuxishi/', 'https://tao.360che.com/wuzhishanshi/', 'https://tao.360che.com/wujiaqushi/', 'https://tao.360che.com/wulanchabushi/', 'https://tao.360che.com/wulumuqishi/', 'https://tao.360che.com/xiangyang/', 'https://tao.360che.com/xiangxi/', 'https://tao.360che.com/xinzhoushi/', 'https://tao.360che.com/xiningshi/', 'https://tao.360che.com/xianyangshi/', 'https://tao.360che.com/xianshi/', 'https://tao.360che.com/xiangtanshi/', 'https://tao.360che.com/xianningshi/', 'https://tao.360che.com/xiaoganshi/', 'https://tao.360che.com/xingtaishi/', 'https://tao.360che.com/xinyangshi/', 'https://tao.360che.com/xuchangshi/', 'https://tao.360che.com/xinxiangshi/', 'https://tao.360che.com/xinyushi/', 'https://tao.360che.com/xiamenshi/', 'https://tao.360che.com/xuanchengshi/', 'https://tao.360che.com/xuzhoushi/', 'https://tao.360che.com/xinganmeng/', 'https://tao.360che.com/xiantaoshi/', 'https://tao.360che.com/xishuangbanna/', 'https://tao.360che.com/xishaqundao/', 'https://tao.360che.com/xilinguolemeng/', 'https://tao.360che.com/yili/', 'https://tao.360che.com/yanbian/', 'https://tao.360che.com/yushu/', 'https://tao.360che.com/yangjiangshi/', 'https://tao.360che.com/yinchuanshi/', 'https://tao.360che.com/yulinshi/', 'https://tao.360che.com/yananshi/', 'https://tao.360che.com/yuxishi/', 'https://tao.360che.com/yaanshi/', 'https://tao.360che.com/yibinshi/', 'https://tao.360che.com/yl/', 'https://tao.360che.com/yunfushi/', 'https://tao.360che.com/yangquanshi/', 'https://tao.360che.com/yongzhoushi/', 'https://tao.360che.com/yunchengshi/', 'https://tao.360che.com/yueyangshi/', 'https://tao.360che.com/yichangshi/', 'https://tao.360che.com/yantaishi/', 'https://tao.360che.com/yichunshi/', 'https://tao.360che.com/yingtanshi/', 'https://tao.360che.com/yangzhoushi/', 'https://tao.360che.com/yanchengshi/', 'https://tao.360che.com/yc/', 'https://tao.360che.com/yingkoushi/', 'https://tao.360che.com/yiyangshi/', 'https://tao.360che.com/zhuhaishi/', 'https://tao.360che.com/zhangyeshi/', 'https://tao.360che.com/ziyangshi/', 'https://tao.360che.com/zigongshi/', 'https://tao.360che.com/zhongshanshi/', 'https://tao.360che.com/zhaoqingshi/', 'https://tao.360che.com/zhanjiangshi/', 'https://tao.360che.com/zhenjiangshi/', 'https://tao.360che.com/zhuzhoushi/', 'https://tao.360che.com/zhaotongshi/', 'https://tao.360che.com/zhongweishi/', 'https://tao.360che.com/zhoukoushi/', 'https://tao.360che.com/zhengzhoushi/', 'https://tao.360che.com/zaozhuangshi/', 'https://tao.360che.com/ziboshi/', 'https://tao.360che.com/zhangzhoushi/', 'https://tao.360che.com/zhoushanshi/', 'https://tao.360che.com/zunyishi/', 'https://tao.360che.com/zhangjiakoushi/', 'https://tao.360che.com/zhangjiajieshi/', 'https://tao.360che.com/zhumadianshi/', 'https://tao.360che.com/zhongshaqundao/']


    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'REDIS_URL': 'redis://192.168.1.92:6379/6',
        'MYSQL_TABLE': 'che360',
        'MYSQL_DB': 'truck',
        'CrawlCar_Num': 1000000,
        'AUTOTHROTTLE_START_DELAY': 8,
        'DOWNLOAD_DELAY': 0,
    }
    # rules = (
    #     Rule(LinkExtractor(allow=r'.+\d\.html', restrict_xpaths="//div[@class='truck-pages']"), callback='parse_item', follow=True),
    #     # Rule(LinkExtractor(allow=r'Items/', restrict_xpaths="//div[@class='page']//a[contains(text(),'...')]"), callback='parse_item', follow=True),
    # )
    def start_requests(self):
        # url = "https://tao.360che.com/1.html"
        for city_url in self.city_list:
            yield scrapy.Request(
                url=city_url,
                headers=self.headers,
                dont_filter=True,
            )

    def parse(self, response):
        car_a_list = response.xpath("//div[@class='clearfix']/a")
        for car_a in car_a_list:
            url = car_a.xpath("./@href").get()
            detail_url = "https://tao.360che.com"+url
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detial_url,
                headers=self.headers
            )
        next_url = response.xpath("//div[@class='pages last']/a/@href").get()
        if next_url:
            next_url_new = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url_new,
                callback=self.parse,
                dont_filter=False
            )

    def parse_detial_url(self, response):
        item = che360Item()
        item["brand"] = response.xpath("//div[contains(text(),'品牌')]/following-sibling::div[1]/text()").get()
        item["shortdesc"] = response.xpath("//div[contains(text(),'车辆描述')]/following-sibling::div[1]/text()").get()
        item["registeryear"] = response.xpath("//div[contains(text(),'行驶证登记日期')]/following-sibling::div[1]/text()").get()
        item["mileage"] = response.xpath("//div[contains(text(),'表显里程')]/preceding-sibling::div[1]/text()").get()
        item["carid"] = re.findall("/m(.*?)_", response.url)[0]
        item["url"] = response.url
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["pagetitle"] = response.xpath("//head/title/text()").get()
        item["series"] = response.xpath("//div[contains(text(),'车系')]/following-sibling::div[1]/text()").get()
        item["price"] = response.xpath("//i[contains(text(),'万')]/preceding-sibling::span[1]/text()").get().replace("¥", "")
        item['statusplus'] = item["url"] + "-" + str(item["price"])
        item["level"] = response.xpath("//div[contains(text(),'吨位级别')]/following-sibling::div[1]/text()").get()
        item["hoursepower"] = response.xpath("//div[contains(text(),'马力')]/following-sibling::div[1]/text()").get()
        item["pull"] = response.xpath("//div[contains(text(),'准牵引总重量')]/following-sibling::div[1]/text()").get()
        item["driveType"] = response.xpath("//div[contains(text(),'驱动形式')]/following-sibling::div[1]/text()").get()
        item["speedBox"] = response.xpath("//div[contains(text(),'变速箱')]/following-sibling::div[1]/text()").get()
        item["containerLong"] = response.xpath("//div[contains(text(),'货箱长度')]/following-sibling::div[1]/text()").get()
        item["containerType"] = response.xpath("//div[contains(text(),'货箱形式')]/following-sibling::div[1]/text()").get()
        item["let"] = response.xpath("//div[contains(text(),'排放标准')]/following-sibling::div[1]/text()").get()
        item["engine"] = response.xpath("//div[contains(text(),'发动机品牌')]/following-sibling::div[1]/text()").get()
        item["speedRatio"] = response.xpath("//div[contains(text(),'后桥速比')]/following-sibling::div[1]/text()").get()
        item["trailer"] = response.xpath("//div[contains(text(),'挂车形式')]/following-sibling::div[1]/text()").get()
        item["axes"] = response.xpath("//div[contains(text(),'轴数')]/following-sibling::div[1]/text()").get()
        item["hangType"] = response.xpath("//div[contains(text(),'悬挂形式')]/following-sibling::div[1]/text()").get()
        item["insurance1_date"] = response.xpath("//div[contains(text(),'交强险过期时间')]/following-sibling::div[1]/text()").get()
        item["company"] = ''.join(response.xpath("//div[@class='info'][1]/div[1]/text()").getall()).replace(" ","").replace("\n","")
        item["linkman"] = ''.join(response.xpath("//div[@class='info'][1]/div[2]/text()").getall()).replace(" ","").replace("\n","")
        item["store_location"] = response.xpath("//div[@class='info'][1]/div[@class='name'][2]/a/text()").get()
        # item[""] = response.xpath("").get()
        city_info = response.xpath("//div[@class='tips']/div[@class='city']/text()").get()
        if city_info:
            item["province"] = city_info.split("：")[1].split(" ")[0]
            item["city"] = city_info.split("：")[1].split(" ")[1]
            item["public_time"] = city_info.split("：")[1].split(" ")[3]
            # item[""] = response.xpath("").get()
            # item[""] = response.xpath("").get()
        item["carSourceid"] = response.xpath("//div[@class='tips']/div[@class='number']/text()").get().split(" ")[1]
        # print(item)
        yield item

