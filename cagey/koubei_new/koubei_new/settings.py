# -*- coding: utf-8 -*-

# Scrapy settings for koubei_new project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'koubei_new'

SPIDER_MODULES = ['koubei_new.spiders']
NEWSPIDER_MODULE = 'koubei_new.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'koubei_new (+http://www.yourdomain.com)'

HTTPERROR_ALLOWED_CODES = [418, 403]
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

RETRY_ENABLED = True
RETRY_TIMES = 5
CRAWL_NUM = 2000000

"""koubei mongo"""
MONGODB_SERVER = "192.168.1.92"
MONGODB_PORT = 27017
MONGODB_DB = "koubei"
MONGODB_COLLECTION = "yiche_koubei"
CrawlCar_Num = 2000000

# """luntan mongo"""
# MONGODB_SERVER = "192.168.1.94"
# MONGODB_PORT = 27017
# MONGODB_DB = "luntan"
# MONGODB_COLLECTION_YCKB = "yiche_luntan"
# CrawlCar_Num = 2000000

# REDIS_SERVER ="192.168.1.248"
# REDIS_PORT =6379

""" mysql 配置"""
MYSQL_DB = 'koubei'
MYSQL_TABLE = 'yiche_koubei_new'
MYSQL_PORT = '3306'
MYSQL_SERVER = '192.168.1.94'
MYSQL_USER = "dataUser94"
MYSQL_PWD = "94dataUser@2020"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'koubei_new.middlewares.KoubeiNewSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'koubei_new.proxy.ProxyMiddleware': 500,
    'koubei_new.proxy.SeleniumMiddleware': 400,
    'koubei_new.proxy.LechebangMiddleware': 600,
    'koubei_new.proxy.GangMiddleware': 700,
    # 'koubei_new.middlewares.KoubeiNewDownloaderMiddleware': 543,
    'koubei_new.middlewares.RotateUserAgentMiddleware': 541,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'koubei_new.pipelines.KoubeiNewPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FONT_DIC = {'&#x78;': 'x', '&#xe001;': '老', '&#xe002;': '适', '&#xe005;': '者', '&#xe009;': '选', '&#xe00f;': '透', '&#xe010;': '耐', '&#xe012;': '倒', '&#xe014;': '途', '&#xe017;': '耗', '&#xe01a;': '通', '&#xe01f;': '速', '&#xe020;': '造', '&#xe03c;': '值', '&#xe03e;': '倾', '&#xe047;': '遇', '&#xe04f;': '偏', '&#xe054;': '联', '&#xe06f;': '灯', '&#xe075;': '灵', '&#xe08c;': '肌', '&#xe094;': '悔', '&#xe0a1;': '股', '&#xe0a8;': '储', '&#xe0ac;': '悬', '&#xe0b2;': '悲', '&#xe0b9;': '点', '&#xe0c5;': '情', '&#xe0c8;': '烈', '&#xe0cc;': '背', '&#xe0ce;': '胎', '&#xe0df;': '烟', '&#xe0e0;': '惠', '&#xe0e6;': '烦', '&#xe0e8;': '部', '&#xe0ef;': '惯', '&#xe0f6;': '胶', '&#xe0fd;': '能', '&#xe106;': '脆', '&#xe11f;': '感', '&#xe127;': '愧', '&#xe145;': '充', '&#xe149;': '光', '&#xe14b;': '克', '&#xe14d;': '配', '&#xe15a;': '党', '&#xe162;': '慢', '&#xe165;': '入', '&#xe167;': '照', '&#xe16b;': '八', '&#xe16d;': '六', '&#xe170;': '腰', '&#xe177;': '酷', '&#xe178;': '酸', '&#xe17e;': '腾', '&#xe17f;': '腿', '&#xe184;': '熄', '&#xe185;': '内', '&#xe19c;': '农', '&#xe1a0;': '冠', '&#xe1c6;': '准', '&#xe1cc;': '凌', '&#xe1cd;': '重', '&#xe1ce;': '野', '&#xe1cf;': '量', '&#xe1d1;': '金', '&#xe1e0;': '几', '&#xe1ef;': '凯', '&#xe206;': '分', '&#xe211;': '我', '&#xe212;': '舒', '&#xe21a;': '刚', '&#xe22c;': '爬', '&#xe236;': '制', '&#xe23a;': '刺', '&#xe240;': '所', '&#xe241;': '扁', '&#xe248;': '版', '&#xe24b;': '手', '&#xe24c;': '牌', '&#xe24d;': '前', '&#xe24e;': '扎', '&#xe253;': '打', '&#xe269;': '物', '&#xe26d;': '扭', '&#xe26f;': '良', '&#xe272;': '色', '&#xe279;': '特', '&#xe280;': '犀', '&#xe291;': '抑', '&#xe296;': '抖', '&#xe2a3;': '劣', '&#xe2a5;': '报', '&#xe2a8;': '动', '&#xe2a9;': '助', '&#xe2b2;': '劲', '&#xe2b6;': '状', '&#xe2d2;': '勒', '&#xe2e0;': '狠', '&#xe2f3;': '拳', '&#xe302;': '挂', '&#xe303;': '范', '&#xe305;': '包', '&#xe307;': '指', '&#xe311;': '挑', '&#xe316;': '化', '&#xe317;': '北', '&#xe31b;': '猛', '&#xe321;': '挡', '&#xe324;': '挤', '&#xe339;': '匹', '&#xe33a;': '区', '&#xe341;': '十', '&#xe343;': '千', '&#xe347;': '升', '&#xe34a;': '半', '&#xe355;': '单', '&#xe357;': '南', '&#xe361;': '卡', '&#xe363;': '荣', '&#xe371;': '危', '&#xe377;': '捷', '&#xe382;': '厂', '&#xe387;': '率', '&#xe392;': '排', '&#xe3a3;': '掣', '&#xe3a9;': '玩', '&#xe3b0;': '现', '&#xe3bb;': '玻', '&#xe3c2;': '参', '&#xe3cc;': '双', '&#xe3cd;': '反', '&#xe3d0;': '提', '&#xe3d1;': '发', '&#xe3d7;': '受', '&#xe3dc;': '菜', '&#xe3e1;': '握', '&#xe3e3;': '口', '&#xe403;': '吃', '&#xe40d;': '名', '&#xe410;': '吐', '&#xe413;': '搓', '&#xe428;': '吨', '&#xe42a;': '搪', '&#xe42c;': '听', '&#xe42f;': '启', '&#xe434;': '琴', '&#xe438;': '吸', '&#xe43d;': '落', '&#xe457;': '呗', '&#xe468;': '周', '&#xe473;': '味', '&#xe478;': '摸', '&#xe4a2;': '钢', '&#xe4c1;': '铁', '&#xe4cd;': '操', '&#xe4dd;': '蓝', '&#xe4ea;': '哪', '&#xe4ec;': '铬', '&#xe528;': '用', '&#xe52e;': '售', '&#xe530;': '田', '&#xe535;': '电', '&#xe539;': '改', '&#xe545;': '畅', '&#xe546;': '商', '&#xe54c;': '界', '&#xe559;': '教', '&#xe55c;': '镜', '&#xe55e;': '敞', '&#xe565;': '略', '&#xe566;': '啦', '&#xe584;': '薄', '&#xe597;': '斗', '&#xe59c;': '喜', '&#xe59d;': '疝', '&#xe5ad;': '断', '&#xe5b0;': '新', '&#xe5b7;': '喷', '&#xe5bc;': '疼', '&#xe5cf;': '族', '&#xe5d6;': '嗖', '&#xe5e0;': '无', '&#xe5e5;': '日', '&#xe5e8;': '门', '&#xe5f4;': '间', '&#xe60e;': '明', '&#xe613;': '易', '&#xe61f;': '星', '&#xe62f;': '是', '&#xe634;': '嘴', '&#xe635;': '阵', '&#xe63f;': '嘿', '&#xe64e;': '虎', '&#xe65a;': '虚', '&#xe664;': '除', '&#xe668;': '器', '&#xe66a;': '噪', '&#xe66f;': '景', '&#xe67a;': '智', '&#xe67e;': '百', '&#xe684;': '的', '&#xe694;': '隔', '&#xe697;': '暗', '&#xe6ae;': '皮', '&#xe6be;': '难', '&#xe6c5;': '雅', '&#xe6c8;': '盈', '&#xe6ca;': '益', '&#xe6d2;': '盒', '&#xe6d6;': '盖', '&#xe6d8;': '盘', '&#xe6db;': '四', '&#xe6ea;': '雪', '&#xe6f0;': '困', '&#xe6f2;': '曲', '&#xe6f4;': '围', '&#xe6f7;': '雷', '&#xe6fe;': '盾', '&#xe700;': '最', '&#xe707;': '震', '&#xe708;': '圈', '&#xe70b;': '看', '&#xe717;': '朗', '&#xe71f;': '真', '&#xe721;': '蜡', '&#xe728;': '在', '&#xe72c;': '本', '&#xe738;': '霸', '&#xe740;': '着', '&#xe750;': '坐', '&#xe751;': '坑', '&#xe752;': '青', '&#xe75e;': '非', '&#xe760;': '杠', '&#xe761;': '条', '&#xe762;': '面', '&#xe779;': '睹', '&#xe77e;': '松', '&#xe79c;': '果', '&#xe7ab;': '垫', '&#xe7df;': '域', '&#xe7e9;': '韩', '&#xe7ed;': '短', '&#xe7f3;': '石', '&#xe805;': '栅', '&#xe807;': '标', '&#xe835;': '堵', '&#xe84c;': '行', '&#xe851;': '塑', '&#xe854;': '塔', '&#xe861;': '衡', '&#xe86b;': '填', '&#xe86c;': '硬', '&#xe87f;': '顿', '&#xe884;': '预', '&#xe891;': '碑', '&#xe89e;': '增', '&#xe8a0;': '颠', '&#xe8a6;': '梦', '&#xe8b0;': '械', '&#xe8c5;': '装', '&#xe8ce;': '风', '&#xe8d9;': '飙', '&#xe8de;': '飞', '&#xe8e8;': '磨', '&#xe8ee;': '森', '&#xe907;': '备', '&#xe916;': '外', '&#xe91a;': '多', '&#xe927;': '大', '&#xe92a;': '太', '&#xe92e;': '央', '&#xe934;': '头', '&#xe93e;': '社', '&#xe947;': '奇', '&#xe95e;': '神', '&#xe962;': '奢', '&#xe965;': '奥', '&#xe970;': '饰', '&#xe973;': '女', '&#xe97a;': '祺', '&#xe97d;': '好', '&#xe97f;': '西', '&#xe98f;': '福', '&#xe996;': '首', '&#xe999;': '香', '&#xe9bb;': '离', '&#xe9c2;': '观', '&#xe9c4;': '规', '&#xe9c6;': '视', '&#xe9d1;': '科', '&#xe9d2;': '角', '&#xe9d8;': '秘', '&#xe9e6;': '触', '&#xe9fd;': '槽', '&#xea01;': '威', '&#xea21;': '模', '&#xea33;': '稳', '&#xea46;': '婆', '&#xea6c;': '马', '&#xea6d;': '驭', '&#xea70;': '驰', '&#xea71;': '驱', '&#xea76;': '驶', '&#xea7b;': '驻', '&#xea81;': '突', '&#xea84;': '窄', '&#xea8f;': '骏', '&#xead8;': '高', '&#xeb3e;': '款', '&#xeb49;': '等', '&#xeb63;': '正', '&#xeb65;': '步', '&#xeb7b;': '死', '&#xeb80;': '简', '&#xeb89;': '安', '&#xeb9a;': '定', '&#xeb9e;': '实', '&#xeba2;': '订', '&#xeba4;': '认', '&#xebb0;': '记', '&#xebb1;': '箱', '&#xebb6;': '家', '&#xebb9;': '容', '&#xebbd;': '宽', '&#xebbe;': '设', '&#xebc2;': '毂', '&#xebc4;': '评', '&#xebcc;': '富', '&#xebdb;': '毛', '&#xebed;': '语', '&#xebf8;': '寸', '&#xebfc;': '导', '&#xec03;': '调', '&#xec0f;': '小', '&#xec14;': '气', '&#xec1a;': '尚', '&#xec24;': '尤', '&#xec3e;': '尾', '&#xec49;': '汉', '&#xec4f;': '屏', '&#xec55;': '展', '&#xec61;': '象', '&#xec6a;': '豪', '&#xec7d;': '汽', '&#xec83;': '沃', '&#xec99;': '沙', '&#xec9f;': '沟', '&#xecad;': '岭', '&#xecb9;': '油', '&#xecbe;': '精', '&#xecca;': '泊', '&#xecfb;': '系', '&#xed20;': '素', '&#xed27;': '紧', '&#xed28;': '质', '&#xed35;': '贵', '&#xed39;': '费', '&#xed41;': '流', '&#xed44;': '资', '&#xed4b;': '测', '&#xed4e;': '济', '&#xed5b;': '赛', '&#xed5e;': '赞', '&#xed85;': '超', '&#xed8a;': '越', '&#xed8b;': '趋', '&#xeda1;': '涡', '&#xeda3;': '趣', '&#xeda8;': '涨', '&#xedb2;': '液', '&#xedb4;': '趴', '&#xedb5;': '涵', '&#xedc3;': '跃', '&#xedd1;': '跑', '&#xede1;': '巡', '&#xede8;': '巨', '&#xedee;': '差', '&#xedef;': '路', '&#xedf7;': '混', '&#xedfb;': '添', '&#xee00;': '一', '&#xee01;': '丁', '&#xee02;': '市', '&#xee03;': '七', '&#xee05;': '清', '&#xee07;': '万', '&#xee09;': '三', '&#xee0b;': '下', '&#xee0d;': '不', '&#xee0f;': '踏', '&#xee10;': '渐', '&#xee11;': '丑', '&#xee1c;': '东', '&#xee21;': '鸡', '&#xee29;': '温', '&#xee2a;': '个', '&#xee2d;': '中', '&#xee38;': '游', '&#xee58;': '乘', '&#xee5d;': '九', '&#xee5f;': '也', '&#xee70;': '买', '&#xee71;': '乱', '&#xee86;': '了', '&#xee8a;': '床', '&#xee8b;': '事', '&#xee8c;': '二', '&#xee8e;': '于', '&#xee90;': '源', '&#xee94;': '五', '&#xee9c;': '溜', '&#xeea2;': '红', '&#xeea6;': '度', '&#xeea7;': '座', '&#xeeab;': '身', '&#xeead;': '庭', '&#xeeae;': '亮', '&#xeeba;': '躺', '&#xeebf;': '线', '&#xeec0;': '什', '&#xeec1;': '仁', '&#xeec6;': '细', '&#xeecf;': '经', '&#xeed1;': '滑', '&#xeedf;': '统', '&#xeee1;': '满', '&#xeee3;': '代', '&#xeee4;': '滤', '&#xeee5;': '以', '&#xeef0;': '绰', '&#xeef7;': '价', '&#xeeff;': '绿', '&#xef00;': '开', '&#xef02;': '异', '&#xef04;': '弄', '&#xef0f;': '式', '&#xef17;': '弗', '&#xef24;': '伤', '&#xef38;': '缸', '&#xef39;': '弹', '&#xef3a;': '强', '&#xef4d;': '位', '&#xef4e;': '低', '&#xef50;': '齐', '&#xef51;': '网', '&#xef53;': '当', '&#xef59;': '余', '&#xef66;': '车', '&#xef6e;': '轮', '&#xef73;': '佳', '&#xef7d;': '载', '&#xef7f;': '轿', '&#xef88;': '很', '&#xef8e;': '美', '&#xef93;': '输', '&#xef9b;': '供', '&#xef9d;': '依', '&#xefa7;': '侧', '&#xefa9;': '辩', '&#xefb7;': '德', '&#xefb9;': '边', '&#xefbf;': '便', '&#xefc5;': '必', '&#xefc7;': '过', '&#xefdd;': '保', '&#xefe1;': '信', '&#xefeb;': '快', '&#xeffb;': '翻', '&#xeffc;': '翼', '&#xeffd;': '追'}


USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

CITY = {'北京': 'bj', '上海': 'sh', '成都': 'cd', '重庆': 'cq', '广州': 'gz', '安顺': 'anshun', '鞍山': 'anshan', '安阳': 'anyang', '安庆': 'anqing', '安康': 'ankang', '巴中': 'bazhong', '毕节': 'bijie', '保定': 'baoding', '滨州': 'binzhoozhou', '包头': 'baotou', '宝鸡': 'baoji', '朝阳市': 'chaoyang', '常州': 'changzhou', '承德': 'chengde', '沧州': 'cangzhou', '长春': 'cc', '滁州': 'chuzhou', '赤峰': 'chifeng', '长治': 'changzhi', '长沙': 'cs', '常德': 'changde', '东莞': 'dg', '德阳': 'deyang', '达州': 'dazhou', '大连': 'dl', '丹东': 'dandong', '大庆': 'daqing', '东营': 'dongying', '德州': 'dezhou', '大同': 'datong', '大理': 'dali', '鄂尔多斯': 'eerduosi', '鄂州': 'ezhou', '恩施':'enshi', '抚顺': 'fushun', '福州': 'fz', '阜阳': 'fuyang', '抚州': 'jxfuzhou', '广元': 'guangyuan', '广安': 'guangan', '贵阳': 'gy', '桂林': 'gl', '赣州': 'ganzhou', '惠州': 'huizhou', '河源': 'heyuan', '杭州': 'hz', '湖州': 'huzhou', '淮安': 'huaian','邯郸': 'handan', '衡水': 'hengshui', '哈尔滨': 'hrb', '菏泽': 'heze', '合肥': 'hf', '淮南': 'huainan', '淮北': 'huaibei', '海口': 'hn', '呼和浩特': 'nmg', '汉中': 'hanzhong', '黄石': 'huangshi', '黄冈': 'huanggang', '衡阳': 'hengyangiangmen', '揭阳': 'jieyang', '嘉兴': 'jiaxing', '金华': 'jinhua', '锦州': 'jinzhou', '焦作': 'jiaozuo', '吉林': 'jilin', '佳木斯': 'jiamusi', '济南': 'jn', '济宁': 'jining', '晋城': 'jincheng', '晋中': 'jinzhong', '荆州': 'jingzhou', '九江': 'jiujiang', '吉安': 'jian', '开封': 'kaifeng', '昆明': 'km', '泸州': 'luzhou', '乐山': 'leshan', '丽水': 'lishui', '六盘水': 'liupanshui', '辽阳': 'liaoyang', '连云港': 'lianyungang', '龙岩': 'longyan', '廊坊':'langfang', '漯河': 'luohe', '临沂': 'linyi', '聊城': 'liaocheng', '六安': 'luan', '柳州': 'liuzhou', '临汾': 'linfen', '兰州': 'lz', '娄底': 'loudi', '茂名': 'maoming', '梅州': 'meizhou', '绵阳': 'mianyang', '眉山': 'meishan', '牡丹江':'mudanjiang' , '南充': 'nanchong', '内江': 'neijiang', '宁波': 'nb', '南京': 'nj', '南通': 'nantong', '南平': 'nanping', '宁德': 'ningde', '南阳': 'nanyang', '南宁': 'nn', '南昌': 'nc', '攀枝花': 'panzhihua', '盘锦': 'panjin', '莆田': 'an', '濮阳': 'puyang', '萍乡': 'pingxiang', '清远': 'qingyuan', '衢州': 'quzhou', '泉州': 'quanzhou', '秦皇岛': 'qinhuangdao', '齐齐哈尔': 'qiqihaer', '青岛': 'qd', '钦州': 'qinzhou', '潜江': 'qianjiang', '曲靖': 'qujing', '日照':  'shantou', '汕尾': 'shanwei', '遂宁': 'suining', '绍兴': 'shaoxing', '沈阳': 'sy', '苏州': 'su', '宿迁': 'suqian', '三明': 'sanming', '石家庄': 'sjz', '三门峡': 'sanmenxia', '商丘': 'shangqiu', '四平': 'siping', '松原': 'songyuan' 'ahsuzhou', '榆林': 'sxyulin', '十堰': 'shiyan', '随州': 'suizhou', '邵阳': 'shaoyang', '上饶': 'shangrao', '天津': 'tj', '台州': 'zjtaizhou', '铁岭': 'tieling', '泰州': 'jstaizhou', '唐山': 'tangshan', '泰安': 'taian', '铜陵':'tongling', '温州': 'wenzhou', '无锡': 'wx', '威海': 'wei', '潍坊': 'weifang', '芜湖': 'wuhu', '梧州': 'wuzhou', '渭南': 'weinan', '武汉': 'wh', '乌鲁木齐': 'xj', '徐州': 'xuzhou', '厦门': 'xm', '邢台': 'xingtai', '新乡': 'xinxiang', '许昌': 'xuchang', '西安': 'xa', '西宁': 'xn', '襄阳': 'xiangyang', '孝感': 'xiaogan', '咸宁': 'xianning', '湘潭': 'xiangtan', '新余': 'xinyu', '阳江': 'yangjiang', '云浮': 'yunfu', '宜宾': 'yibin', '雅安': 'yaan', '营口': 'yingkou', '烟台': 'yantai', '玉林': 'yulin', '阳泉': 'yangquan', '运城': 'yuncheng', '银川': 'yc', '延安': 'yanan', '宜昌': 'yichang', '岳阳': 'yueyang', '永州': 'yongzhou', '益阳': 'yiyang', '宜春': 'jxyichun', '玉溪': 'yuxi', '': 'zhongshan', '湛江': 'zhanjiang', '肇庆': 'zhaoqing', '自贡': 'zigong', '资阳': 'ziyang', '遵义': 'zunyi', '镇江': 'zhenjiang', '漳州': 'zhangzhou', '郑州': 'zz', '周口': 'zhoukou', '驻马店': 'zhumadian', '淄博': 'zibo', '枣庄': 'zaozhuang', '昭通': 'zhaotong'}
