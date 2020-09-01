# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from pprint import pprint
from scrapy_redis.spiders import RedisSpider
from newcar_new.items import AutohomeItem_price

website = 'pcauto_price'

# class PcautoPriceSpider(scrapy.Spider):
class PcautoPriceSpider(RedisSpider):
    name = website
    redis_key = "pcauto_price:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(PcautoPriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.city_code_dic = {
     'c1': {'city_code': 'c1', 'city_name': '广州', 'prv_name': '广东'},
     'a1847': {'city_code': 'a1847', 'city_name': '渝中区', 'prv_name': '重庆'},
     'a1848': {'city_code': 'a1848', 'city_name': '大渡口区', 'prv_name': '重庆'},
     'a1849': {'city_code': 'a1849', 'city_name': '江北区', 'prv_name': '重庆'},
     'a1850': {'city_code': 'a1850', 'city_name': '沙坪坝区', 'prv_name': '重庆'},
     'a1851': {'city_code': 'a1851', 'city_name': '九龙坡区', 'prv_name': '重庆'},
     'a1931': {'city_code': 'a1931', 'city_name': '南岸区', 'prv_name': '重庆'},
     'a1932': {'city_code': 'a1932', 'city_name': '北碚区', 'prv_name': '重庆'},
     'a1933': {'city_code': 'a1933', 'city_name': '渝北区', 'prv_name': '重庆'},
     'a1934': {'city_code': 'a1934', 'city_name': '巴南区', 'prv_name': '重庆'},
     'a1935': {'city_code': 'a1935', 'city_name': '万州区', 'prv_name': '重庆'},
     'a1936': {'city_code': 'a1936', 'city_name': '涪陵区', 'prv_name': '重庆'},
     'a1937': {'city_code': 'a1937', 'city_name': '黔江区', 'prv_name': '重庆'},
     'a1938': {'city_code': 'a1938', 'city_name': '长寿区', 'prv_name': '重庆'},
     'a1939': {'city_code': 'a1939', 'city_name': '江津区', 'prv_name': '重庆'},
     'a1940': {'city_code': 'a1940', 'city_name': '合川区', 'prv_name': '重庆'},
     'a1941': {'city_code': 'a1941', 'city_name': '永川区', 'prv_name': '重庆'},
     'a1942': {'city_code': 'a1942', 'city_name': '南川区', 'prv_name': '重庆'},
     'a1943': {'city_code': 'a1943', 'city_name': '大足区', 'prv_name': '重庆'},
     'a1944': {'city_code': 'a1944', 'city_name': '潼南县', 'prv_name': '重庆'},
     'a1945': {'city_code': 'a1945', 'city_name': '铜梁县', 'prv_name': '重庆'},
     'a1946': {'city_code': 'a1946', 'city_name': '荣昌县', 'prv_name': '重庆'},
     'a1947': {'city_code': 'a1947', 'city_name': '璧山区', 'prv_name': '重庆'},
     'a1948': {'city_code': 'a1948', 'city_name': '梁平县', 'prv_name': '重庆'},
     'a1956': {'city_code': 'a1956', 'city_name': '丰都县', 'prv_name': '重庆'},
     'a1958': {'city_code': 'a1958', 'city_name': '垫江县', 'prv_name': '重庆'},
     'a1962': {'city_code': 'a1962', 'city_name': '忠县', 'prv_name': '重庆'},
     'a1963': {'city_code': 'a1963', 'city_name': '开县', 'prv_name': '重庆'},
     'a1965': {'city_code': 'a1965', 'city_name': '云阳县', 'prv_name': '重庆'},
     'a1967': {'city_code': 'a1967', 'city_name': '奉节县', 'prv_name': '重庆'},
     'a1972': {'city_code': 'a1972', 'city_name': '巫溪县', 'prv_name': '重庆'},
     'a1973': {'city_code': 'a1973', 'city_name': '石柱县', 'prv_name': '重庆'},
     'a1975': {'city_code': 'a1975', 'city_name': '秀山县', 'prv_name': '重庆'},
     'a1978': {'city_code': 'a1978', 'city_name': '酉阳县', 'prv_name': '重庆'},
     'a1981': {'city_code': 'a1981', 'city_name': '彭水县', 'prv_name': '重庆'},
     'a1989': {'city_code': 'a1989', 'city_name': '綦江区', 'prv_name': '重庆'},
     'a3157': {'city_code': 'a3157', 'city_name': '开州区', 'prv_name': '重庆'},
     'a40': {'city_code': 'a40', 'city_name': '宝山区', 'prv_name': '上海'},
     'a41': {'city_code': 'a41', 'city_name': '长宁区', 'prv_name': '上海'},
     'a42': {'city_code': 'a42', 'city_name': '崇明县', 'prv_name': '上海'},
     'a43': {'city_code': 'a43', 'city_name': '奉贤区', 'prv_name': '上海'},
     'a44': {'city_code': 'a44', 'city_name': '虹口区', 'prv_name': '上海'},
     'a45': {'city_code': 'a45', 'city_name': '黄浦区', 'prv_name': '上海'},
     'a46': {'city_code': 'a46', 'city_name': '嘉定区', 'prv_name': '上海'},
     'a47': {'city_code': 'a47', 'city_name': '金山区', 'prv_name': '上海'},
     'a48': {'city_code': 'a48', 'city_name': '静安区', 'prv_name': '上海'},
     'a49': {'city_code': 'a49', 'city_name': '卢湾区', 'prv_name': '上海'},
     'a50': {'city_code': 'a50', 'city_name': '闵行区', 'prv_name': '上海'},
     'a52': {'city_code': 'a52', 'city_name': '浦东新区', 'prv_name': '上海'},
     'a53': {'city_code': 'a53', 'city_name': '普陀区', 'prv_name': '上海'},
     'a54': {'city_code': 'a54', 'city_name': '青浦区', 'prv_name': '上海'},
     'a55': {'city_code': 'a55', 'city_name': '松江区', 'prv_name': '上海'},
     'a56': {'city_code': 'a56', 'city_name': '徐汇区', 'prv_name': '上海'},
     'a57': {'city_code': 'a57', 'city_name': '杨浦区', 'prv_name': '上海'},
     'a58': {'city_code': 'a58', 'city_name': '闸北区', 'prv_name': '上海'},

     'a11': {'city_code': 'a11', 'city_name': '昌平区', 'prv_name': '北京'},
     'a12': {'city_code': 'a12', 'city_name': '朝阳区', 'prv_name': '北京'},
     'a13': {'city_code': 'a13', 'city_name': '大兴区', 'prv_name': '北京'},
     'a14': {'city_code': 'a14', 'city_name': '东城区', 'prv_name': '北京'},
     'a15': {'city_code': 'a15', 'city_name': '丰台区', 'prv_name': '北京'},
     'a16': {'city_code': 'a16', 'city_name': '海淀区', 'prv_name': '北京'},
     'a17': {'city_code': 'a17', 'city_name': '怀柔区', 'prv_name': '北京'},
     'a18': {'city_code': 'a18', 'city_name': '石景山区', 'prv_name': '北京'},
     'a19': {'city_code': 'a19', 'city_name': '密云县', 'prv_name': '北京'},
     'a20': {'city_code': 'a20', 'city_name': '平谷区', 'prv_name': '北京'},
     'a21': {'city_code': 'a21', 'city_name': '顺义区', 'prv_name': '北京'},
     'a22': {'city_code': 'a22', 'city_name': '通州区', 'prv_name': '北京'},
     'a23': {'city_code': 'a23', 'city_name': '西城区', 'prv_name': '北京'},
     'a230': {'city_code': 'a230', 'city_name': '门头沟区', 'prv_name': '北京'},
     'a24': {'city_code': 'a24', 'city_name': '延庆县', 'prv_name': '北京'},
     'a96': {'city_code': 'a96', 'city_name': '房山区', 'prv_name': '北京'},

    'c1010': {'city_code': 'c1010', 'city_name': '阿拉善盟', 'prv_name': '内蒙古'},
    'c1011': {'city_code': 'c1011', 'city_name': '石嘴山', 'prv_name': '宁夏'},
    'c1012': {'city_code': 'c1012', 'city_name': '海东', 'prv_name': '青海'},
    'c1017': {'city_code': 'c1017', 'city_name': '玉树', 'prv_name': '青海'},
    'c1020': {'city_code': 'c1020', 'city_name': '商洛', 'prv_name': '陕西'},
    'c1025': {'city_code': 'c1025', 'city_name': '那曲地区', 'prv_name': '西藏'},
    'c1033': {'city_code': 'c1033', 'city_name': '北屯', 'prv_name': '新疆'},
    'c1048': {'city_code': 'c1048', 'city_name': '儋州', 'prv_name': '海南'},
    'c1050': {'city_code': 'c1050', 'city_name': '万宁', 'prv_name': '海南'},
    'c1051': {'city_code': 'c1051', 'city_name': '东方', 'prv_name': '海南'},
    'c1053': {'city_code': 'c1053', 'city_name': '琼海', 'prv_name': '海南'},
    'c107': {'city_code': 'c107', 'city_name': '昆明', 'prv_name': '云南'},
    'c117': {'city_code': 'c117', 'city_name': '长沙', 'prv_name': '湖南'},
    'c127': {'city_code': 'c127', 'city_name': '沈阳', 'prv_name': '辽宁'},
    'c137': {'city_code': 'c137', 'city_name': '石家庄', 'prv_name': '河北'},
    'c147': {'city_code': 'c147', 'city_name': '济南', 'prv_name': '山东'},
    'c157': {'city_code': 'c157', 'city_name': '苏州', 'prv_name': '江苏'},
    'c177': {'city_code': 'c177', 'city_name': '南京', 'prv_name': '江苏'},
    'c187': {'city_code': 'c187', 'city_name': '哈尔滨', 'prv_name': '黑龙江'},
    'c197': {'city_code': 'c197', 'city_name': '南宁', 'prv_name': '广西'},
    'c207': {'city_code': 'c207', 'city_name': '惠州', 'prv_name': '广东'},
    'c217': {'city_code': 'c217', 'city_name': '杭州', 'prv_name': '浙江'},
    'c218': {'city_code': 'c218', 'city_name': '宁波', 'prv_name': '浙江'},
    'c227': {'city_code': 'c227', 'city_name': '长春', 'prv_name': '吉林'},
    'c237': {'city_code': 'c237', 'city_name': '南昌', 'prv_name': '江西'},
    'c238': {'city_code': 'c238', 'city_name': '中山', 'prv_name': '广东'},
    'c247': {'city_code': 'c247', 'city_name': '兰州', 'prv_name': '甘肃'},
    'c248': {'city_code': 'c248', 'city_name': '大连', 'prv_name': '辽宁'},
    'c257': {'city_code': 'c257', 'city_name': '天津', 'prv_name': '天津'},
    'c258': {'city_code': 'c258', 'city_name': '乌鲁木齐', 'prv_name': '新疆'},
    'c259': {'city_code': 'c259', 'city_name': '海口', 'prv_name': '海南'},
    'c260': {'city_code': 'c260', 'city_name': '太原', 'prv_name': '山西'},
    'c267': {'city_code': 'c267', 'city_name': '郑州', 'prv_name': '河南'},
    'c268': {'city_code': 'c268', 'city_name': '洛阳', 'prv_name': '河南'},
    'c277': {'city_code': 'c277', 'city_name': '保定', 'prv_name': '河北'},
    'c287': {'city_code': 'c287', 'city_name': '贵阳', 'prv_name': '贵州'},
    'c288': {'city_code': 'c288', 'city_name': '汕头', 'prv_name': '广东'},
    'c289': {'city_code': 'c289', 'city_name': '揭阳', 'prv_name': '广东'},
    'c290': {'city_code': 'c290', 'city_name': '潮州', 'prv_name': '广东'},
    'c291': {'city_code': 'c291', 'city_name': '梅州', 'prv_name': '广东'},
    'c292': {'city_code': 'c292', 'city_name': '泉州', 'prv_name': '福建'},
    'c293': {'city_code': 'c293', 'city_name': '厦门', 'prv_name': '福建'},
    'c297': {'city_code': 'c297', 'city_name': '合肥', 'prv_name': '安徽'},
    'c298': {'city_code': 'c298', 'city_name': '珠海', 'prv_name': '广东'},
    'c299': {'city_code': 'c299', 'city_name': '绍兴', 'prv_name': '浙江'},
    'c300': {'city_code': 'c300', 'city_name': '金华', 'prv_name': '浙江'},
    'c301': {'city_code': 'c301', 'city_name': '台州', 'prv_name': '浙江'},
    'c302': {'city_code': 'c302', 'city_name': '湖州', 'prv_name': '浙江'},
    'c303': {'city_code': 'c303', 'city_name': '温州', 'prv_name': '浙江'},
    'c304': {'city_code': 'c304', 'city_name': '嘉兴', 'prv_name': '浙江'},
    'c305': {'city_code': 'c305', 'city_name': '无锡', 'prv_name': '江苏'},
    'c306': {'city_code': 'c306', 'city_name': '镇江', 'prv_name': '江苏'},
    'c307': {'city_code': 'c307', 'city_name': '徐州', 'prv_name': '江苏'},
    'c308': {'city_code': 'c308', 'city_name': '南通', 'prv_name': '江苏'},
    'c309': {'city_code': 'c309', 'city_name': '常州', 'prv_name': '江苏'},
    'c310': {'city_code': 'c310', 'city_name': '扬州', 'prv_name': '江苏'},
    'c311': {'city_code': 'c311', 'city_name': '德州', 'prv_name': '山东'},
    'c312': {'city_code': 'c312', 'city_name': '东营', 'prv_name': '山东'},
    'c313': {'city_code': 'c313', 'city_name': '济宁', 'prv_name': '山东'},
    'c314': {'city_code': 'c314', 'city_name': '泰安', 'prv_name': '山东'},
    'c315': {'city_code': 'c315', 'city_name': '威海', 'prv_name': '山东'},
    'c316': {'city_code': 'c316', 'city_name': '淄博', 'prv_name': '山东'},
    'c317': {'city_code': 'c317', 'city_name': '青岛', 'prv_name': '山东'},
    'c318': {'city_code': 'c318', 'city_name': '烟台', 'prv_name': '山东'},
    'c319': {'city_code': 'c319', 'city_name': '潍坊', 'prv_name': '山东'},
    'c320': {'city_code': 'c320', 'city_name': '临沂', 'prv_name': '山东'},
    'c321': {'city_code': 'c321', 'city_name': '营口', 'prv_name': '辽宁'},
    'c322': {'city_code': 'c322', 'city_name': '锦州', 'prv_name': '辽宁'},
    'c323': {'city_code': 'c323', 'city_name': '鞍山', 'prv_name': '辽宁'},
    'c324': {'city_code': 'c324', 'city_name': '盘锦', 'prv_name': '辽宁'},
    'c325': {'city_code': 'c325', 'city_name': '临汾', 'prv_name': '山西'},
    'c326': {'city_code': 'c326', 'city_name': '大同', 'prv_name': '山西'},
    'c327': {'city_code': 'c327', 'city_name': '宜昌', 'prv_name': '湖北'},
    'c328': {'city_code': 'c328', 'city_name': '绵阳', 'prv_name': '四川'},
    'c329': {'city_code': 'c329', 'city_name': '齐齐哈尔', 'prv_name': '黑龙江'},
    'c330': {'city_code': 'c330', 'city_name': '大庆', 'prv_name': '黑龙江'},
    'c331': {'city_code': 'c331', 'city_name': '牡丹江', 'prv_name': '黑龙江'},
    'c332': {'city_code': 'c332', 'city_name': '佳木斯', 'prv_name': '黑龙江'},
    'c333': {'city_code': 'c333', 'city_name': '绥化', 'prv_name': '黑龙江'},
    'c334': {'city_code': 'c334', 'city_name': '鹤岗', 'prv_name': '黑龙江'},
    'c335': {'city_code': 'c335', 'city_name': '吉林', 'prv_name': '吉林'},
    'c337': {'city_code': 'c337', 'city_name': '白城', 'prv_name': '吉林'},
    'c338': {'city_code': 'c338', 'city_name': '松原', 'prv_name': '吉林'},
    'c339': {'city_code': 'c339', 'city_name': '辽阳', 'prv_name': '辽宁'},
    'c340': {'city_code': 'c340', 'city_name': '葫芦岛', 'prv_name': '辽宁'},
    'c341': {'city_code': 'c341', 'city_name': '抚顺', 'prv_name': '辽宁'},
    'c342': {'city_code': 'c342', 'city_name': '丹东', 'prv_name': '辽宁'},
    'c343': {'city_code': 'c343', 'city_name': '铁岭', 'prv_name': '辽宁'},
    'c344': {'city_code': 'c344', 'city_name': '朝阳', 'prv_name': '辽宁'},
    'c345': {'city_code': 'c345', 'city_name': '阜新', 'prv_name': '辽宁'},
    'c346': {'city_code': 'c346', 'city_name': '本溪', 'prv_name': '辽宁'},
    'c347': {'city_code': 'c347', 'city_name': '唐山', 'prv_name': '河北'},
    'c348': {'city_code': 'c348', 'city_name': '邯郸', 'prv_name': '河北'},
    'c349': {'city_code': 'c349', 'city_name': '秦皇岛', 'prv_name': '河北'},
    'c35': {'city_code': 'c35', 'city_name': '佛山', 'prv_name': '广东'},
    'c350': {'city_code': 'c350', 'city_name': '邢台', 'prv_name': '河北'},
    'c351': {'city_code': 'c351', 'city_name': '沧州', 'prv_name': '河北'},
    'c352': {'city_code': 'c352', 'city_name': '张家口', 'prv_name': '河北'},
    'c353': {'city_code': 'c353', 'city_name': '廊坊', 'prv_name': '河北'},
    'c354': {'city_code': 'c354', 'city_name': '承德', 'prv_name': '河北'},
    'c355': {'city_code': 'c355', 'city_name': '衡水', 'prv_name': '河北'},
    'c356': {'city_code': 'c356', 'city_name': '聊城', 'prv_name': '山东'},
    'c357': {'city_code': 'c357', 'city_name': '日照', 'prv_name': '山东'},
    'c358': {'city_code': 'c358', 'city_name': '滨州', 'prv_name': '山东'},
    'c359': {'city_code': 'c359', 'city_name': '枣庄', 'prv_name': '山东'},
    'c360': {'city_code': 'c360', 'city_name': '莱芜', 'prv_name': '山东'},
    'c361': {'city_code': 'c361', 'city_name': '菏泽', 'prv_name': '山东'},
    'c364': {'city_code': 'c364', 'city_name': '宝鸡', 'prv_name': '陕西'},
    'c365': {'city_code': 'c365', 'city_name': '榆林', 'prv_name': '陕西'},
    'c366': {'city_code': 'c366', 'city_name': '南阳', 'prv_name': '河南'},
    'c367': {'city_code': 'c367', 'city_name': '开封', 'prv_name': '河南'},
    'c368': {'city_code': 'c368', 'city_name': '焦作', 'prv_name': '河南'},
    'c369': {'city_code': 'c369', 'city_name': '安阳', 'prv_name': '河南'},
    'c370': {'city_code': 'c370', 'city_name': '平顶山', 'prv_name': '河南'},
    'c371': {'city_code': 'c371', 'city_name': '许昌', 'prv_name': '河南'},
    'c372': {'city_code': 'c372', 'city_name': '商丘', 'prv_name': '河南'},
    'c373': {'city_code': 'c373', 'city_name': '濮阳', 'prv_name': '河南'},
    'c374': {'city_code': 'c374', 'city_name': '新乡', 'prv_name': '河南'},
    'c375': {'city_code': 'c375', 'city_name': '信阳', 'prv_name': '河南'},
    'c376': {'city_code': 'c376', 'city_name': '漯河', 'prv_name': '河南'},
    'c377': {'city_code': 'c377', 'city_name': '三门峡', 'prv_name': '河南'},
    'c378': {'city_code': 'c378', 'city_name': '驻马店', 'prv_name': '河南'},
    'c379': {'city_code': 'c379', 'city_name': '周口', 'prv_name': '河南'},
    'c380': {'city_code': 'c380', 'city_name': '鹤壁', 'prv_name': '河南'},
    'c382': {'city_code': 'c382', 'city_name': '连云港', 'prv_name': '江苏'},
    'c385': {'city_code': 'c385', 'city_name': '泰州', 'prv_name': '江苏'},
    'c389': {'city_code': 'c389', 'city_name': '淮安', 'prv_name': '江苏'},
    'c390': {'city_code': 'c390', 'city_name': '宿迁', 'prv_name': '江苏'},
    'c399': {'city_code': 'c399', 'city_name': '衢州', 'prv_name': '浙江'},
    'c4': {'city_code': 'c4', 'city_name': '深圳', 'prv_name': '广东'},
    'c402': {'city_code': 'c402', 'city_name': '丽水', 'prv_name': '浙江'},
    'c413': {'city_code': 'c413', 'city_name': '襄阳', 'prv_name': '湖北'},
    'c414': {'city_code': 'c414', 'city_name': '黄石', 'prv_name': '湖北'},
    'c415': {'city_code': 'c415', 'city_name': '荆州', 'prv_name': '湖北'},
    'c416': {'city_code': 'c416', 'city_name': '十堰', 'prv_name': '湖北'},
    'c417': {'city_code': 'c417', 'city_name': '荆门', 'prv_name': '湖北'},
    'c419': {'city_code': 'c419', 'city_name': '随州', 'prv_name': '湖北'},
    'c420': {'city_code': 'c420', 'city_name': '黄冈', 'prv_name': '湖北'},
    'c421': {'city_code': 'c421', 'city_name': '咸宁', 'prv_name': '湖北'},
    'c422': {'city_code': 'c422', 'city_name': '乐山', 'prv_name': '四川'},
    'c423': {'city_code': 'c423', 'city_name': '德阳', 'prv_name': '四川'},
    'c424': {'city_code': 'c424', 'city_name': '宜宾', 'prv_name': '四川'},
    'c425': {'city_code': 'c425', 'city_name': '泸州', 'prv_name': '四川'},
    'c426': {'city_code': 'c426', 'city_name': '南充', 'prv_name': '四川'},
    'c427': {'city_code': 'c427', 'city_name': '内江', 'prv_name': '四川'},
    'c428': {'city_code': 'c428', 'city_name': '眉山', 'prv_name': '四川'},
    'c429': {'city_code': 'c429', 'city_name': '衡阳', 'prv_name': '湖南'},
    'c430': {'city_code': 'c430', 'city_name': '株洲', 'prv_name': '湖南'},
    'c431': {'city_code': 'c431', 'city_name': '郴州', 'prv_name': '湖南'},
    'c432': {'city_code': 'c432', 'city_name': '常德', 'prv_name': '湖南'},
    'c433': {'city_code': 'c433', 'city_name': '邵阳', 'prv_name': '湖南'},
    'c434': {'city_code': 'c434', 'city_name': '湘潭', 'prv_name': '湖南'},
    'c435': {'city_code': 'c435', 'city_name': '怀化', 'prv_name': '湖南'},
    'c436': {'city_code': 'c436', 'city_name': '娄底', 'prv_name': '湖南'},
    'c438': {'city_code': 'c438', 'city_name': '益阳', 'prv_name': '湖南'},
    'c439': {'city_code': 'c439', 'city_name': '永州', 'prv_name': '湖南'},
    'c440': {'city_code': 'c440', 'city_name': '九江', 'prv_name': '江西'},
    'c441': {'city_code': 'c441', 'city_name': '赣州', 'prv_name': '江西'},
    'c442': {'city_code': 'c442', 'city_name': '萍乡', 'prv_name': '江西'},
    'c443': {'city_code': 'c443', 'city_name': '上饶', 'prv_name': '江西'},
    'c444': {'city_code': 'c444', 'city_name': '吉安', 'prv_name': '江西'},
    'c445': {'city_code': 'c445', 'city_name': '漳州', 'prv_name': '福建'},
    'c446': {'city_code': 'c446', 'city_name': '莆田', 'prv_name': '福建'},
    'c448': {'city_code': 'c448', 'city_name': '龙岩', 'prv_name': '福建'},
    'c449': {'city_code': 'c449', 'city_name': '南平', 'prv_name': '福建'},
    'c45': {'city_code': 'c45', 'city_name': '西安', 'prv_name': '陕西'},
    'c451': {'city_code': 'c451', 'city_name': '三明', 'prv_name': '福建'},
    'c452': {'city_code': 'c452', 'city_name': '玉溪', 'prv_name': '云南'},
    'c453': {'city_code': 'c453', 'city_name': '曲靖', 'prv_name': '云南'},
    'c455': {'city_code': 'c455', 'city_name': '大理', 'prv_name': '云南'},
    'c456': {'city_code': 'c456', 'city_name': '江门', 'prv_name': '广东'},
    'c457': {'city_code': 'c457', 'city_name': '湛江', 'prv_name': '广东'},
    'c458': {'city_code': 'c458', 'city_name': '肇庆', 'prv_name': '广东'},
    'c459': {'city_code': 'c459', 'city_name': '茂名', 'prv_name': '广东'},
    'c460': {'city_code': 'c460', 'city_name': '韶关', 'prv_name': '广东'},
    'c461': {'city_code': 'c461', 'city_name': '清远', 'prv_name': '广东'},
    'c462': {'city_code': 'c462', 'city_name': '阳江', 'prv_name': '广东'},
    'c463': {'city_code': 'c463', 'city_name': '河源', 'prv_name': '广东'},
    'c464': {'city_code': 'c464', 'city_name': '云浮', 'prv_name': '广东'},
    'c465': {'city_code': 'c465', 'city_name': '汕尾', 'prv_name': '广东'},
    'c467': {'city_code': 'c467', 'city_name': '三亚', 'prv_name': '海南'},
    'c468': {'city_code': 'c468', 'city_name': '天水', 'prv_name': '甘肃'},
    'c469': {'city_code': 'c469', 'city_name': '庆阳', 'prv_name': '甘肃'},
    'c472': {'city_code': 'c472', 'city_name': '阳泉', 'prv_name': '山西'},
    'c473': {'city_code': 'c473', 'city_name': '长治', 'prv_name': '山西'},
    'c474': {'city_code': 'c474', 'city_name': '晋城', 'prv_name': '山西'},
    'c475': {'city_code': 'c475', 'city_name': '朔州', 'prv_name': '山西'},
    'c476': {'city_code': 'c476', 'city_name': '忻州', 'prv_name': '山西'},
    'c477': {'city_code': 'c477', 'city_name': '晋中', 'prv_name': '山西'},
    'c478': {'city_code': 'c478', 'city_name': '吕梁', 'prv_name': '山西'},
    'c479': {'city_code': 'c479', 'city_name': '运城', 'prv_name': '山西'},
    'c480': {'city_code': 'c480', 'city_name': '呼伦贝尔', 'prv_name': '内蒙古'},
    'c481': {'city_code': 'c481', 'city_name': '呼和浩特', 'prv_name': '内蒙古'},
    'c482': {'city_code': 'c482', 'city_name': '包头', 'prv_name': '内蒙古'},
    'c483': {'city_code': 'c483', 'city_name': '鄂尔多斯', 'prv_name': '内蒙古'},
    'c488': {'city_code': 'c488', 'city_name': '淮南', 'prv_name': '安徽'},
    'c489': {'city_code': 'c489', 'city_name': '淮北', 'prv_name': '安徽'},
    'c490': {'city_code': 'c490', 'city_name': '芜湖', 'prv_name': '安徽'},
    'c491': {'city_code': 'c491', 'city_name': '蚌埠', 'prv_name': '安徽'},
    'c492': {'city_code': 'c492', 'city_name': '马鞍山', 'prv_name': '安徽'},
    'c493': {'city_code': 'c493', 'city_name': '安庆', 'prv_name': '安徽'},
    'c494': {'city_code': 'c494', 'city_name': '黄山', 'prv_name': '安徽'},
    'c495': {'city_code': 'c495', 'city_name': '滁州', 'prv_name': '安徽'},
    'c496': {'city_code': 'c496', 'city_name': '阜阳', 'prv_name': '安徽'},
    'c497': {'city_code': 'c497', 'city_name': '宿州', 'prv_name': '安徽'},
    'c498': {'city_code': 'c498', 'city_name': '宣城', 'prv_name': '安徽'},
    'c499': {'city_code': 'c499', 'city_name': '六安', 'prv_name': '安徽'},
    'c500': {'city_code': 'c500', 'city_name': '宁德', 'prv_name': '福建'},
    'c502': {'city_code': 'c502', 'city_name': '宜春', 'prv_name': '江西'},
    'c508': {'city_code': 'c508', 'city_name': '孝感', 'prv_name': '湖北'},
    'c509': {'city_code': 'c509', 'city_name': '岳阳', 'prv_name': '湖南'},
    'c510': {'city_code': 'c510', 'city_name': '柳州', 'prv_name': '广西'},
    'c511': {'city_code': 'c511', 'city_name': '桂林', 'prv_name': '广西'},
    'c512': {'city_code': 'c512', 'city_name': '玉林', 'prv_name': '广西'},
    'c513': {'city_code': 'c513', 'city_name': '遂宁', 'prv_name': '四川'},
    'c514': {'city_code': 'c514', 'city_name': '达州', 'prv_name': '四川'},
    'c515': {'city_code': 'c515', 'city_name': '雅安', 'prv_name': '四川'},
    'c516': {'city_code': 'c516', 'city_name': '遵义', 'prv_name': '贵州'},
    'c518': {'city_code': 'c518', 'city_name': '拉萨', 'prv_name': '西藏'},
    'c519': {'city_code': 'c519', 'city_name': '渭南', 'prv_name': '陕西'},
    'c521': {'city_code': 'c521', 'city_name': '延安', 'prv_name': '陕西'},
    'c522': {'city_code': 'c522', 'city_name': '汉中', 'prv_name': '陕西'},
    'c523': {'city_code': 'c523', 'city_name': '克拉玛依', 'prv_name': '新疆'},
    'c525': {'city_code': 'c525', 'city_name': '吐鲁番', 'prv_name': '新疆'},
    'c526': {'city_code': 'c526', 'city_name': '哈密', 'prv_name': '新疆'},
    'c527': {'city_code': 'c527', 'city_name': '阿克苏', 'prv_name': '新疆'},
    'c528': {'city_code': 'c528', 'city_name': '喀什', 'prv_name': '新疆'},
    'c529': {'city_code': 'c529', 'city_name': '昌吉', 'prv_name': '新疆'},
    'c530': {'city_code': 'c530', 'city_name': '伊犁', 'prv_name': '新疆'},
    'c531': {'city_code': 'c531', 'city_name': '银川', 'prv_name': '宁夏'},
    'c532': {'city_code': 'c532', 'city_name': '西宁', 'prv_name': '青海'},
    'c534': {'city_code': 'c534', 'city_name': '乌海', 'prv_name': '内蒙古'},
    'c535': {'city_code': 'c535', 'city_name': '通辽', 'prv_name': '内蒙古'},
    'c536': {'city_code': 'c536', 'city_name': '赤峰', 'prv_name': '内蒙古'},
    'c538': {'city_code': 'c538', 'city_name': '攀枝花', 'prv_name': '四川'},
    'c539': {'city_code': 'c539', 'city_name': '巴州', 'prv_name': '新疆'},
    'c541': {'city_code': 'c541', 'city_name': '嘉峪关', 'prv_name': '甘肃'},
    'c542': {'city_code': 'c542', 'city_name': '亳州', 'prv_name': '安徽'},
    'c545': {'city_code': 'c545', 'city_name': '百色', 'prv_name': '广西'},
    'c546': {'city_code': 'c546', 'city_name': '钦州', 'prv_name': '广西'},
    'c547': {'city_code': 'c547', 'city_name': '防城港', 'prv_name': '广西'},
    'c548': {'city_code': 'c548', 'city_name': '河池', 'prv_name': '广西'},
    'c549': {'city_code': 'c549', 'city_name': '梧州', 'prv_name': '广西'},
    'c55': {'city_code': 'c55', 'city_name': '福州', 'prv_name': '福建'},
    'c550': {'city_code': 'c550', 'city_name': '贵港', 'prv_name': '广西'},
    'c551': {'city_code': 'c551', 'city_name': '通化', 'prv_name': '吉林'},
    'c552': {'city_code': 'c552', 'city_name': '抚州', 'prv_name': '江西'},
    'c553': {'city_code': 'c553', 'city_name': '鹰潭', 'prv_name': '江西'},
    'c554': {'city_code': 'c554', 'city_name': '新余', 'prv_name': '江西'},
    'c555': {'city_code': 'c555', 'city_name': '巴彦淖尔', 'prv_name': '内蒙古'},
    'c559': {'city_code': 'c559', 'city_name': '广元', 'prv_name': '四川'},
    'c564': {'city_code': 'c564', 'city_name': '北海', 'prv_name': '广西'},
    'c567': {'city_code': 'c567', 'city_name': '鸡西', 'prv_name': '黑龙江'},
    'c569': {'city_code': 'c569', 'city_name': '锡林郭勒盟', 'prv_name': '内蒙古'},
    'c571': {'city_code': 'c571', 'city_name': '四平', 'prv_name': '吉林'},
    'c572': {'city_code': 'c572', 'city_name': '辽源', 'prv_name': '吉林'},
    'c573': {'city_code': 'c573', 'city_name': '白山', 'prv_name': '吉林'},
    'c576': {'city_code': 'c576', 'city_name': '景德镇', 'prv_name': '江西'},
    'c579': {'city_code': 'c579', 'city_name': '仙桃', 'prv_name': '湖北'},
    'c580': {'city_code': 'c580', 'city_name': '六盘水', 'prv_name': '贵州'},
    'c581': {'city_code': 'c581', 'city_name': '自贡', 'prv_name': '四川'},
    'c582': {'city_code': 'c582', 'city_name': '广安', 'prv_name': '四川'},
    'c583': {'city_code': 'c583', 'city_name': '巴中', 'prv_name': '四川'},
    'c584': {'city_code': 'c584', 'city_name': '贺州', 'prv_name': '广西'},
    'c585': {'city_code': 'c585', 'city_name': '酒泉', 'prv_name': '甘肃'},
    'c586': {'city_code': 'c586', 'city_name': '白银', 'prv_name': '甘肃'},
    'c587': {'city_code': 'c587', 'city_name': '舟山', 'prv_name': '浙江'},
    'c599': {'city_code': 'c599', 'city_name': '张家界', 'prv_name': '湖南'},
    'c6': {'city_code': 'c6', 'city_name': '东莞', 'prv_name': '广东'},
    'c600': {'city_code': 'c600', 'city_name': '潜江', 'prv_name': '湖北'},
    'c601': {'city_code': 'c601', 'city_name': '鄂州', 'prv_name': '湖北'},
    'c604': {'city_code': 'c604', 'city_name': '昭通', 'prv_name': '云南'},
    'c610': {'city_code': 'c610', 'city_name': '铜陵', 'prv_name': '安徽'},
    'c626': {'city_code': 'c626', 'city_name': '来宾', 'prv_name': '广西'},
    'c628': {'city_code': 'c628', 'city_name': '张掖', 'prv_name': '甘肃'},
    'c629': {'city_code': 'c629', 'city_name': '武威', 'prv_name': '甘肃'},
    'c644': {'city_code': 'c644', 'city_name': '七台河', 'prv_name': '黑龙江'},
    'c656': {'city_code': 'c656', 'city_name': '博尔塔拉', 'prv_name': '新疆'},
    'c657': {'city_code': 'c657', 'city_name': '石河子', 'prv_name': '新疆'},
    'c658': {'city_code': 'c658', 'city_name': '吴忠', 'prv_name': '宁夏'},
    'c659': {'city_code': 'c659', 'city_name': '固原', 'prv_name': '宁夏'},
    'c660': {'city_code': 'c660', 'city_name': '乌兰察布', 'prv_name': '内蒙古'},
    'c661': {'city_code': 'c661', 'city_name': '平凉', 'prv_name': '甘肃'},
    'c662': {'city_code': 'c662', 'city_name': '陇南', 'prv_name': '甘肃'},
    'c663': {'city_code': 'c663', 'city_name': '安顺', 'prv_name': '贵州'},
    'c664': {'city_code': 'c664', 'city_name': '毕节', 'prv_name': '贵州'},
    'c665': {'city_code': 'c665', 'city_name': '铜仁', 'prv_name': '贵州'},
    'c666': {'city_code': 'c666', 'city_name': '临沧', 'prv_name': '云南'},
    'c669': {'city_code': 'c669', 'city_name': '崇左', 'prv_name': '广西'},
    'c671': {'city_code': 'c671', 'city_name': '咸阳', 'prv_name': '陕西'},
    'c676': {'city_code': 'c676', 'city_name': '兴安盟', 'prv_name': '内蒙古'},
    'c677': {'city_code': 'c677', 'city_name': '和田', 'prv_name': '新疆'},
    'c702': {'city_code': 'c702', 'city_name': '丽江', 'prv_name': '云南'},
    'c712': {'city_code': 'c712', 'city_name': '中卫', 'prv_name': '宁夏'},
    'c713': {'city_code': 'c713', 'city_name': '金昌', 'prv_name': '甘肃'},
    'c725': {'city_code': 'c725', 'city_name': '天津滨海', 'prv_name': '天津'},
    'c727': {'city_code': 'c727', 'city_name': '延边', 'prv_name': '吉林'},
    'c729': {'city_code': 'c729', 'city_name': '保山', 'prv_name': '云南'},
    'c730': {'city_code': 'c730', 'city_name': '恩施', 'prv_name': '湖北'},
    'c735': {'city_code': 'c735', 'city_name': '黔南', 'prv_name': '贵州'},
    'c736': {'city_code': 'c736', 'city_name': '天门', 'prv_name': '湖北'},
    'c740': {'city_code': 'c740', 'city_name': '黔西南', 'prv_name': '贵州'},
    'c743': {'city_code': 'c743', 'city_name': '安康', 'prv_name': '陕西'},
    'c744': {'city_code': 'c744', 'city_name': '凉山', 'prv_name': '四川'},
    'c745': {'city_code': 'c745', 'city_name': '红河', 'prv_name': '云南'},
    'c749': {'city_code': 'c749', 'city_name': '池州', 'prv_name': '安徽'},
    'c752': {'city_code': 'c752', 'city_name': '铜川', 'prv_name': '陕西'},
    'c755': {'city_code': 'c755', 'city_name': '普洱', 'prv_name': '云南'},
    'c758': {'city_code': 'c758', 'city_name': '楚雄', 'prv_name': '云南'},
    'c759': {'city_code': 'c759', 'city_name': '西双版纳', 'prv_name': '云南'},
    'c76': {'city_code': 'c76', 'city_name': '武汉', 'prv_name': '湖北'},
    'c764': {'city_code': 'c764', 'city_name': '吉首', 'prv_name': '湖南'},
    'c773': {'city_code': 'c773', 'city_name': '定西', 'prv_name': '甘肃'},
    'c774': {'city_code': 'c774', 'city_name': '海西', 'prv_name': '青海'},
    'c777': {'city_code': 'c777', 'city_name': '文山', 'prv_name': '云南'},
    'c780': {'city_code': 'c780', 'city_name': '双鸭山', 'prv_name': '黑龙江'},
    'c794': {'city_code': 'c794', 'city_name': '日喀则地区', 'prv_name': '西藏'},
    'c795': {'city_code': 'c795', 'city_name': '阿勒泰', 'prv_name': '新疆'},
    'c796': {'city_code': 'c796', 'city_name': '塔城', 'prv_name': '新疆'},
    'c814': {'city_code': 'c814', 'city_name': '黔东南', 'prv_name': '贵州'},
    'c851': {'city_code': 'c851', 'city_name': '黑河', 'prv_name': '黑龙江'},
    'c860': {'city_code': 'c860', 'city_name': '迪庆', 'prv_name': '云南'},
    'c861': {'city_code': 'c861', 'city_name': '德宏', 'prv_name': '云南'},
    'c87': {'city_code': 'c87', 'city_name': '成都', 'prv_name': '四川'},
    'c874': {'city_code': 'c874', 'city_name': '资阳', 'prv_name': '四川'},
    'c895': {'city_code': 'c895', 'city_name': '盐城', 'prv_name': '江苏'},
    'c976': {'city_code': 'c976', 'city_name': '大兴安岭', 'prv_name': '黑龙江'},
    'c978': {'city_code': 'c978', 'city_name': '怒江', 'prv_name': '云南'},
    'c980': {'city_code': 'c980', 'city_name': '临夏', 'prv_name': '甘肃'},
    'c981': {'city_code': 'c981', 'city_name': '甘南', 'prv_name': '甘肃'},
    'c990': {'city_code': 'c990', 'city_name': '济源', 'prv_name': '河南'},
    'c991': {'city_code': 'c991', 'city_name': '伊春', 'prv_name': '黑龙江'}}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'newcar_price',
        'WEBSITE': 'pcauto_price',
        'MYSQL_TABLE': 'pcauto_price',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'newcar_price',
        'MONGODB_COLLECTION': 'pcauto_price',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.1.241:6379/15',
    }

    def parse(self, response):
        city_code = response.url.split('/')[-2]
        city_data = self.city_code_dic[city_code]
        li_list = response.xpath("//div[@class='listTb']/ul/li")
        for li in li_list:
            shopname = li.xpath(".//strong/text()").getall()[0]
            tel = li.xpath(".//strong/text()").getall()[1]
            dealerId = li.xpath(".//p[1]//a/@href").get().split('/')[-2]
            dealer_address = li.xpath(".//p[4]/span[2]/@title").get()
            meta = {
                "shopname": shopname,
                "tel": tel,
                "dealerId": dealerId,
                "dealer_address": dealer_address,
                "prov_Name": city_data["prv_name"],
                "city_ID": city_data["city_code"],
                "city_Name": city_data["city_name"],
            }
            url = f"https://price.pcauto.com.cn/interface/5_3/order_serial_json_chooser.jsp?dealerId={dealerId}"
            response.meta.update(**meta)
            yield scrapy.Request(
                url=url,
                callback=self.parse_dealer_brand,
                meta=response.meta,
                dont_filter=True
            )
        next_url = response.xpath("//a[@class='next']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True
            )

    def parse_dealer_brand(self, response):
        brand_list = []
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        # print(json_data)
        for d in json_data["firms"]:
            brand_id = d["bid"]
            brand_list.append(brand_id)
        brand_list_new = list(set(brand_list))
        print(brand_list_new)
        for b_id in brand_list_new:
            b_url = f"https://price.pcauto.com.cn/auto/api/hcs/serial_group_list?bid={b_id}&status=1&from=1"
            yield scrapy.Request(
                url=b_url,
                callback=self.parse_series,
                meta=response.meta,
                dont_filter=True
            )

    def parse_series(self, response):
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        # print(json_data["manufacturers"])
        for brand in json_data["manufacturers"]:
            brandname = brand["brandName"]
            brandid = brand["manuId"]
            factoryname = brand["name"]
            series_list = brand["serials"]
            for series in series_list:
                vehilename = series["sgname"]
                vehilenameid = series["sgid"]
                meta = {
                    "brandname": brandname,
                    "brandid": brandid,
                    "vehilename": vehilename,
                    "vehilenameid": vehilenameid,
                    "factoryname": factoryname,
                }
                response.meta.update(**meta)
                model_url = f"https://price.pcauto.com.cn/api/hcs/select/model_json_chooser?sgid={vehilenameid}&status=1&type=2"
                yield scrapy.Request(
                    url=model_url,
                    callback=self.parse_model,
                    meta=response.meta,
                    dont_filter=True
                )

    def parse_model(self, response):
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for model in json_data["cars"]:
            if 'price' in model:
                salesdescid = model["id"]
                salesdesc = model["title"]
                guideprice = model["price"]
                meta = {
                    "salesdescid": salesdescid,
                    "salesdesc": salesdesc,
                    "guideprice": guideprice,
                }
                response.meta.update(**meta)
                price_url = f"https://price.pcauto.com.cn/dealer/interface/price/getModelPriceByDid.jsp?mId={salesdescid}&dId={response.meta['dealerId']}"
                yield scrapy.Request(
                    url=price_url,
                    callback=self.parse_price,
                    meta=response.meta,
                    dont_filter=True
                )

    def parse_price(self, response):
        item = AutohomeItem_price()
        json_data = json.loads(response.text)
        print(json_data)
        try:
            salesprice = json_data["row"]["dealerPrice"]
        except KeyError:
            print(response.url)
            print(response.meta['brandid'])
            print(response.meta['dealerId'])
            print("*"*100)
            return
        item['salesprice'] = salesprice
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['prov_Name'] = response.meta['prov_Name']
        item['city_ID'] = response.meta['city_ID']
        item['city_Name'] = response.meta['city_Name']
        item["dealer_address"] = response.meta["dealer_address"]
        # brand
        item['brandname'] = response.meta['brandname']
        item['brandid'] = response.meta['brandid']
        # factory
        item['factoryname'] = response.meta['factoryname']
        #  店名
        item['shopname'] = response.meta['shopname']
        item['shopid'] = response.meta['dealerId']
        # 店电话
        item['tel'] = response.meta['tel']
        # car detail info
        #  车系
        item['vehilename'] = response.meta['vehilename']
        # url  车系url
        item['vehilenameid'] = response.meta['vehilenameid']
        # 车型描述
        item['salesdesc'] = response.meta["salesdesc"]
        # id
        item['salesdescid'] = response.meta["salesdescid"]
        # 指导价
        item['guideprice'] = response.meta["guideprice"]
        # 裸车价
        item['url'] = response.url
        item['status'] = item["url"] + '-' + str(item['salesprice'])
        # print(item)
        yield item



# def parse(self, response):
#     prv_list = response.xpath("//div[@class='Items cityItems']/a")
#     for prv in prv_list:
#         url = prv.xpath("./@href").get()
#         if 'void' not in url:
#             prv_name = prv.xpath("./text()").get()
#             prv_url = f"http:{url}"
#             yield scrapy.Request(
#                 url=prv_url,
#                 callback=self.parse_1,
#                 dont_filter=True,
#                 meta={"prv_name": prv_name}
#             )
#
    # def start_requests(self):
    #     k = 'c77'
    #     url = f"https://price.pcauto.com.cn/shangjia/{k}/"
    #     yield scrapy.Request(
    #         url=url
    #     )
    #
    # def parse(self, response):
    #     print("*"*100)
    #     prv_name = "重庆"
    #     a_list = response.xpath("//div[@class='Items ']/a")
    #     for a in a_list:
    #         data_dic = dict()
    #         city_name = a.xpath("./text()").get()
    #         # city_url = a.xpath("./@href").get()
    #         city_url = a.xpath("./@onclick").get()
    #         if city_url:
    #             # city_code = re.findall('shangjia/(.*?)/', city_url)[0]
    #             city_code = re.findall('shangjia/(.*?)/', city_url)[0]
    #             data_dic["prv_name"] = prv_name
    #             data_dic["city_name"] = city_name
    #             data_dic["city_code"] = city_code
    #             self.city_code_dic[city_code] = data_dic
    #             print("*" * 100)
    #             pprint(self.city_code_dic)
