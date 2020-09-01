# -*- coding: UTF-8 -*-
import redis
import scrapy
from scrapy_redis.spiders import RedisSpider
from usedcar_new.items import GuaziItem
from scrapy_redis.utils import bytes_to_str
import time
import logging
import re
# from random import shuffle
import json

pool = redis.ConnectionPool(host='192.168.1.92', port=6379, db=14)
con = redis.Redis(connection_pool=pool)
c = con.client()
# c.lpush('youxin:start_urls', *city_list)
# p = bytes.decode(p)

website = 'youxin'


class CarSpider(RedisSpider):
    name = website
    redis_key = "youxin:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'youxin_online',
        'WEBSITE': 'youxin',
        'CrawlCar_Num': 1000000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'REDIS_URL': 'redis://192.168.1.92:6379/14',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'COOKIES_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'usedcar_new.middlewares.ProxyMiddleware': 700,
            # 'usedcar_new.middlewares.MoGuProxyMiddleware': 700,
            # 'usedcar_new.middlewares.SeleniumIPMiddleware': 701,
            # 'usedcar_new.middlewares.MyproxiesSpiderMiddleware': 701,
        },
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.UsedcarNewPipeline': 300,
            # 'usedcar_new.pipelines.GanjiPipeline': 300,
        },
    }

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.counts = 0
        self.fail_url = []
        self.c = con.client()
        self.city_code = {'1001': '郑州',
 '1002': '洛阳',
 '1003': '周口',
 '1004': '信阳',
 '1005': '新乡',
 '1006': '商丘',
 '1007': '三门峡',
 '1008': '濮阳',
 '1009': '南阳',
 '101': '合肥',
 '1010': '漯河',
 '1011': '焦作',
 '1013': '开封',
 '1014': '安阳',
 '1015': '德州',
 '1016': '鹤壁',
 '1018': '平顶山',
 '102': '安庆',
 '1021': '驻马店',
 '1023': '许昌',
 '103': '蚌埠',
 '106': '阜阳',
 '107': '淮北',
 '108': '淮南',
 '109': '六安',
 '110': '马鞍山',
 '1101': '哈尔滨',
 '1102': '大庆',
 '1103': '齐齐哈尔',
 '1106': '佳木斯',
 '1107': '鸡西',
 '1108': '牡丹江',
 '1109': '七台河',
 '1112': '伊春',
 '1113': '黑河',
 '1116': '绥化',
 '1118': '双鸭山',
 '113': '铜陵',
 '114': '芜湖',
 '115': '宣城',
 '116': '滁州',
 '117': '亳州',
 '118': '黄山',
 '120': '宿州',
 '1201': '武汉',
 '1202': '十堰',
 '1203': '襄阳',
 '1204': '随州',
 '1205': '仙桃',
 '1206': '天门市',
 '1207': '宜昌',
 '1208': '黄石',
 '1209': '荆门',
 '1210': '荆州',
 '1214': '黄冈',
 '1216': '鄂州',
 '1217': '咸宁',
 '1218': '孝感',
 '1219': '潜江',
 '1301': '长沙',
 '1302': '郴州',
 '1303': '常德',
 '1304': '衡阳',
 '1305': '怀化',
 '1306': '娄底',
 '1307': '株洲',
 '1308': '岳阳',
 '1309': '湘潭',
 '1310': '邵阳',
 '1313': '益阳',
 '1315': '张家界市',
 '1401': '长春',
 '1402': '吉林',
 '1403': '通化',
 '1405': '辽源',
 '1406': '白山',
 '1412': '白城',
 '1415': '松原',
 '1501': '南京',
 '1502': '苏州',
 '1503': '无锡',
 '1505': '常州',
 '1507': '淮安',
 '1510': '连云港',
 '1511': '南通',
 '1512': '盐城',
 '1513': '扬州',
 '1515': '镇江',
 '1517': '泰州',
 '1518': '徐州',
 '1520': '宿迁',
 '1601': '南昌',
 '1602': '上饶',
 '1603': '萍乡',
 '1604': '新余',
 '1605': '宜春',
 '1606': '九江',
 '1607': '赣州',
 '1609': '吉安',
 '1612': '景德镇',
 '1613': '抚州',
 '1616': '四平',
 '1701': '沈阳',
 '1702': '丹东',
 '1703': '抚顺',
 '1704': '阜新',
 '1705': '葫芦岛',
 '1707': '朝阳',
 '1708': '大连',
 '1709': '本溪',
 '1710': '鞍山',
 '1711': '锦州',
 '1713': '辽阳',
 '1714': '营口',
 '1716': '盘锦',
 '1717': '铁岭',
 '1801': '呼和浩特',
 '1802': '包头',
 '1803': '赤峰',
 '1804': '通辽',
 '1805': '乌海',
 '1808': '鄂尔多斯',
 '1812': '呼伦贝尔',
 '1817': '锡林郭勒盟',
 '1819': '乌兰察布',
 '1820': '阿拉善盟',
 '1901': '银川',
 '1902': '吴忠',
 '1903': '固原',
 '1904': '石嘴山',
 '2001': '西宁',
 '2004': '海东',
 '201': '北京',
 '2101': '济南',
 '2102': '青岛',
 '2103': '烟台',
 '2104': '威海',
 '2105': '潍坊',
 '2106': '泰安',
 '2107': '枣庄',
 '2109': '淄博',
 '2110': '东营',
 '2112': '菏泽',
 '2113': '滨州',
 '2114': '聊城',
 '2117': '临沂',
 '2118': '济宁',
 '2120': '日照',
 '2132': '莱芜',
 '2201': '太原',
 '2202': '大同',
 '2203': '晋城',
 '2204': '晋中',
 '2205': '临汾',
 '2206': '长治',
 '2207': '运城',
 '2210': '忻州',
 '2218': '阳泉',
 '2219': '朔州',
 '2220': '吕梁',
 '222400': '延边朝鲜族自治州',
 '2301': '西安',
 '2302': '咸阳',
 '2303': '渭南',
 '2304': '榆林',
 '2305': '宝鸡',
 '2306': '安康',
 '2307': '汉中',
 '2308': '延安',
 '2310': '铜川',
 '2311': '商洛',
 '2401': '上海',
 '2501': '成都',
 '2502': '绵阳',
 '2503': '遂宁',
 '2504': '攀枝花市',
 '2506': '宜宾',
 '2508': '自贡',
 '2510': '广元',
 '2511': '德阳',
 '2512': '乐山',
 '2513': '南充',
 '2514': '眉山',
 '2517': '泸州',
 '2519': '内江',
 '2522': '达州',
 '2523': '广安',
 '2601': '天津',
 '2704': '山南市',
 '2801': '乌鲁木齐',
 '2806': '哈密',
 '2807': '吐鲁番',
 '2810': '石河子市',
 '2901': '昆明',
 '2902': '玉溪',
 '2903': '曲靖',
 '2907': '保山市',
 '2918': '昭通',
 '2924': '丽江',
 '3001': '杭州',
 '3002': '宁波',
 '3003': '温州',
 '3005': '嘉兴',
 '3006': '金华',
 '3009': '丽水',
 '301': '福州',
 '3011': '湖州',
 '3012': '衢州',
 '3015': '台州',
 '3016': '绍兴',
 '302': '厦门',
 '3020': '舟山',
 '303': '龙岩',
 '305': '漳州',
 '306': '莆田',
 '307': '泉州',
 '3101': '重庆',
 '3110': '巴彦淖尔',
 '3111': '中卫',
 '314': '南平',
 '315': '宁德',
 '318': '三明',
 '401': '兰州',
 '402': '定西',
 '405': '平凉',
 '409': '酒泉',
 '410': '张掖',
 '411': '庆阳',
 '412': '武威',
 '415': '天水',
 '416': '白银',
 '417': '陇南',
 '422800': '恩施土家族苗族自治州',
 '451400': '崇左',
 '501': '广州',
 '502': '深圳',
 '503': '珠海',
 '504': '东莞',
 '505': '中山',
 '507': '汕头',
 '510': '潮州',
 '511': '韶关',
 '513': '湛江',
 '513400': '凉山彝族自治州',
 '514': '肇庆',
 '515': '茂名',
 '516': '梅州',
 '518': '佛山',
 '520': '惠州',
 '521': '江门',
 '522': '揭阳',
 '522300': '黔西南布依族苗族自治州',
 '522600': '黔东南苗族侗族自治州',
 '522700': '黔南布依族苗族自治州',
 '524': '清远',
 '532': '阳江',
 '532300': '楚雄彝族自治州',
 '532500': '红河哈尼族彝族自治州',
 '532600': '文山壮族苗族自治州',
 '532800': '西双版纳傣族自治州',
 '532900': '大理白族自治州',
 '533100': '德宏傣族景颇族自治州',
 '535': '河源',
 '550': '汕尾',
 '601': '南宁',
 '602': '柳州',
 '603': '桂林',
 '604': '北海',
 '605': '百色',
 '606': '贺州',
 '607': '河池',
 '608': '贵港',
 '610': '玉林',
 '612': '钦州',
 '613': '梧州',
 '618': '防城港',
 '622900': '临夏回族自治州',
 '632300': '黄南藏族自治州',
 '632500': '海南藏族自治州',
 '632700': '玉树藏族自治州',
 '632800': '海西蒙古族藏族自治州',
 '652300': '昌吉回族自治州',
 '652800': '巴音郭楞蒙古自治州',
 '652900': '阿克苏地区',
 '653100': '喀什地区',
 '654000': '伊犁哈萨克自治州',
 '701': '贵阳',
 '702': '遵义',
 '706': '毕节',
 '708': '六盘水',
 '710': '铜仁',
 '801': '海口',
 '803': '三亚',
 '901': '石家庄',
 '902': '唐山',
 '903': '邢台',
 '905': '秦皇岛',
 '906': '廊坊',
 '907': '邯郸',
 '908': '衡水',
 '909': '沧州',
 '910': '保定',
 '911': '张家口',
 '912': '承德'}
        # self.r = redis.Redis(host='192.168.1.92', port=6379, db=10)
        # self.cookie = self.r.get('youxin_cookie').decode('utf8')
        # self.r.close()
        # print(self.cookie)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            # 'Cookie': f'{self.cookie}'
        }

    # def parse(self, response):
    #     # item = GuaziItem()
    #     item = dict()
    #     if 'arg1' in response.text or '人机' in response.text:
    #         print("*" * 100)
    #         print(response.url)
    #         self.c.lpush('youxin:start_urls', response.url)
    #         # self.fail_url.append(response.url)
    #     else:
    #         status = response.xpath('//div[contains(@class,"d-photo")]/em')
    #         status = "sold" if status else "sale"
    #         item["city_id"] = response.url.split('=')[1]
    #         item["city_name"] = self.city_code[item["city_id"]]
    #         ck = response.xpath("//span[contains(text(),'仓')]").get()
    #         if ck:
    #             item["store"] = re.findall("由(.*?)运往", ck)[0]
    #
    #         if response.xpath('//span[@class="cd_m_info_jg"]/b/text()'):
    #             price = response.xpath('//span[@class="cd_m_info_jg"]/b/text()').get().replace("￥","").replace("万","")
    #         else:
    #             price = "zero"
    #         item["price"] = price
    #         item["car_id"] = re.findall("che(.*?)\.html", response.url)[0]
    #         item['url'] = response.url
    #         item["sid"] = re.findall("com/(.*?)/che", response.url)[0]
    #         item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    #         item["statusplus"] = response.url + "-" + str(price) + "-" + str(status)
    #         pagetitle = response.xpath("//head/title/text()").get()
    #         if pagetitle:
    #             item["brand"] = pagetitle.split(" ")[0]
    #             item["series"] = pagetitle.split(" ")[1]
    #             item["pagetitle"] = pagetitle
    #             yield item
    #         next_url = self.c.lpop('youxin:start_urls')
    #         if next_url:
    #             next_url = bytes.decode(next_url)
    #             yield scrapy.Request(
    #                     url=next_url,
    #                     callback=self.parse,
    #                     headers=self.headers,
    #                 )
    #         # else:
    #         #     self.fail_url.append(response.url)
    #         # for fail_url in self.fail_url:
    #         #     yield scrapy.Request(
    #         #         url=fail_url,
    #         #         callback=self.parse,
    #         #         headers=self.headers,
    #         #         meta={
    #         #             'dont_redirect': True,
    #         #             'handle_httpstatus_list': [302]
    #         #         }
    #         #     )

    def parse(self, response):
        if 'arg1' in response.text:
            print("*" * 100)
            print(response.url)
            self.c.lpush('youxin:start_urls', response.url)
            # self.fail_url.append(response.url)
        else:
            datasave1 = "zero"
            # key and status (sold or sale, price,time)
            status = response.xpath('//div[contains(@class,"d-photo")]/em')
            status = "sold" if status else "sale"
            if response.xpath('//span[@class="cd_m_info_jg"]/b/text()'):
                price = response.xpath('//span[@class="cd_m_info_jg"]/b/text()').extract_first()
            else:
                price = "zero"
            datetime = response.xpath('//li[@class="br"]/em/text()')
            datetime = datetime.extract_first() if datetime else "zero"

            # item loader
            item = GuaziItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['pagetime'] = datetime
            item['datasave'] = str([datasave1, re.sub(r'\s+', ' ', response.xpath('//html').extract_first())])
            item["statusplus"] = response.url + "-" + str(price) + "-" + str(status)
            item["status"] = status
            img_url = response.xpath("//img[@class='cd_m_info_mainimg']/@data-src").get()
            # print(img_url)
            # print("*"*100)
            pagetitle = response.xpath("//head/title/text()").get()
            if pagetitle:
                item["brand"] = pagetitle.split(" ")[0]
                item["series"] = pagetitle.split(" ")[1]
                item["pagetitle"] = pagetitle
                yield item
                # print(item)

