# -*- coding: utf-8 -*-

# Scrapy settings for baogang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baogang'

SPIDER_MODULES = ['baogang.spiders']
NEWSPIDER_MODULE = 'baogang.spiders'

""" splash 配置 """
SPLASH_URL = 'http://192.168.1.241:8050'
# SPLASH_URL = 'http://127.0.0.1:8050'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# 是否调试cookies
# SPLASH_COOKIES_DEBUG = True
# 是否记录400错误
SPLASH_LOG_400 = True

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'

""" mongodb 配置 """
# MONGODB_SERVER = '127.0.0.1'
# MONGODB_SERVER = '180.167.80.118'
MONGODB_SERVER = '192.168.1.92'
# 端口号，默认是27017
# MONGODB_PORT = 1206
MONGODB_PORT = 27017
# 设置数据库名称
MONGODB_DB = 'baogang'
MONGODB_USER = 'admin'
MONGODB_PWD = 'ABCabc123'
# 存放本次数据的表名称
MONGODB_COLLECTION = 'feijiu'
CRAWL_NUM = 2000000

""" mysql 配置"""
MYSQL_DB = 'baogang'
MYSQL_TABLE = 'feijiu_url'
MYSQL_PORT = '3306'
MYSQL_SERVER = '192.168.2.120'
MYSQL_USER = 'baogang'
MYSQL_PWD = 'Baogang@2019'


"""dataX配置"""
DATAX_PATH = "/Users/cagey/datax/bin/datax.py"
OUYEEL_JOB_PATH = "/Users/cagey/datax/job/mongodb2mysql3.json"
FEIJIU_JOB_PATH = ""
# JOB_PATH = "/Users/cagey/datax/job/job.json"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baogang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

HTTPERROR_ALLOWED_CODES = [403, 401]

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
COOKIES_ENABLED = False
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    # 'baogang.middlewares.BaogangSpiderMiddleware': 543,
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    # 'baogang.middlewares.MyproxiesSpiderMiddleware': 543,
    # 'baogang.middlewares.RotateUserAgentMiddleware': 1,
    # 'baogang.middlewares.ProxyMiddleware': 300,
    # 'baogang.middlewares.MoGuProxyMiddleware': 300,
    # 'baogang.middlewares.NewProxyMiddleware': 300,
    # 'baogang.middlewares.SeleniumMiddleware': 300,
}


# 出现错误吗,重新请求
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
# 是否开启重试
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 3


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'baogang.pipelines.BaogangPipeline': 300,
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

USER_AGENTS = [
    'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
    'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
    'Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)',
    'Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/NON_NETWORK Language/zh_CN Process/tools',
]

# Ensure use this Scheduler
# SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
#
# # Ensure all spiders share same duplicates filter through redis
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

#方式一：没有密码
# REDIS_HOST = '192.168.1.249'
# REDIS_PORT = 6379

# Redis URL
# REDIS_URL = 'redis://:foobared@localhost:6379'
REDIS_URL = 'redis://192.168.1.249:6379'
# REDIS_URL = 'redis://192.168.1.241:6379'
# REDIS_URL = 'redis://192.168.1.92:6379'
FEED_EXPORT_ENCODING = 'utf-8'

# 使用布隆过滤器
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# # 增加调度配置
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# # Number of Hash Functions to use, defaults to 6
# BLOOMFILTER_HASH_NUMBER = 6
#
# # Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
# BLOOMFILTER_BIT = 30

# 配置调度器持久化, 爬虫结束, 要不要清空Redis中请求队列和去重指纹的set。如果True, 就表示要持久化存储, 否则清空数据
SCHEDULER_PERSIST = False
#redis配置(下面有两种方式)
#方式一：没有密码
# REDIS_HOST = '192.168.1.241'
# REDIS_PORT = 6379

IDLE_NUMBER = 12

MYEXT_ENABLED = True


FONT_DIC = {'&#x78;': 'x', '&#xe001;': '老', '&#xe002;': '适', '&#xe005;': '者', '&#xe009;': '选', '&#xe00f;': '透', '&#xe010;': '耐', '&#xe012;': '倒', '&#xe014;': '途', '&#xe017;': '耗', '&#xe01a;': '通', '&#xe01f;': '速', '&#xe020;': '造', '&#xe03c;': '值', '&#xe03e;': '倾', '&#xe047;': '遇', '&#xe04f;': '偏', '&#xe054;': '联', '&#xe06f;': '灯', '&#xe075;': '灵', '&#xe08c;': '肌', '&#xe094;': '悔', '&#xe0a1;': '股', '&#xe0a8;': '储', '&#xe0ac;': '悬', '&#xe0b2;': '悲', '&#xe0b9;': '点', '&#xe0c5;': '情', '&#xe0c8;': '烈', '&#xe0cc;': '背', '&#xe0ce;': '胎', '&#xe0df;': '烟', '&#xe0e0;': '惠', '&#xe0e6;': '烦', '&#xe0e8;': '部', '&#xe0ef;': '惯', '&#xe0f6;': '胶', '&#xe0fd;': '能', '&#xe106;': '脆', '&#xe11f;': '感', '&#xe127;': '愧', '&#xe145;': '充', '&#xe149;': '光', '&#xe14b;': '克', '&#xe14d;': '配', '&#xe15a;': '党', '&#xe162;': '慢', '&#xe165;': '入', '&#xe167;': '照', '&#xe16b;': '八', '&#xe16d;': '六', '&#xe170;': '腰', '&#xe177;': '酷', '&#xe178;': '酸', '&#xe17e;': '腾', '&#xe17f;': '腿', '&#xe184;': '熄', '&#xe185;': '内', '&#xe19c;': '农', '&#xe1a0;': '冠', '&#xe1c6;': '准', '&#xe1cc;': '凌', '&#xe1cd;': '重', '&#xe1ce;': '野', '&#xe1cf;': '量', '&#xe1d1;': '金', '&#xe1e0;': '几', '&#xe1ef;': '凯', '&#xe206;': '分', '&#xe211;': '我', '&#xe212;': '舒', '&#xe21a;': '刚', '&#xe22c;': '爬', '&#xe236;': '制', '&#xe23a;': '刺', '&#xe240;': '所', '&#xe241;': '扁', '&#xe248;': '版', '&#xe24b;': '手', '&#xe24c;': '牌', '&#xe24d;': '前', '&#xe24e;': '扎', '&#xe253;': '打', '&#xe269;': '物', '&#xe26d;': '扭', '&#xe26f;': '良', '&#xe272;': '色', '&#xe279;': '特', '&#xe280;': '犀', '&#xe291;': '抑', '&#xe296;': '抖', '&#xe2a3;': '劣', '&#xe2a5;': '报', '&#xe2a8;': '动', '&#xe2a9;': '助', '&#xe2b2;': '劲', '&#xe2b6;': '状', '&#xe2d2;': '勒', '&#xe2e0;': '狠', '&#xe2f3;': '拳', '&#xe302;': '挂', '&#xe303;': '范', '&#xe305;': '包', '&#xe307;': '指', '&#xe311;': '挑', '&#xe316;': '化', '&#xe317;': '北', '&#xe31b;': '猛', '&#xe321;': '挡', '&#xe324;': '挤', '&#xe339;': '匹', '&#xe33a;': '区', '&#xe341;': '十', '&#xe343;': '千', '&#xe347;': '升', '&#xe34a;': '半', '&#xe355;': '单', '&#xe357;': '南', '&#xe361;': '卡', '&#xe363;': '荣', '&#xe371;': '危', '&#xe377;': '捷', '&#xe382;': '厂', '&#xe387;': '率', '&#xe392;': '排', '&#xe3a3;': '掣', '&#xe3a9;': '玩', '&#xe3b0;': '现', '&#xe3bb;': '玻', '&#xe3c2;': '参', '&#xe3cc;': '双', '&#xe3cd;': '反', '&#xe3d0;': '提', '&#xe3d1;': '发', '&#xe3d7;': '受', '&#xe3dc;': '菜', '&#xe3e1;': '握', '&#xe3e3;': '口', '&#xe403;': '吃', '&#xe40d;': '名', '&#xe410;': '吐', '&#xe413;': '搓', '&#xe428;': '吨', '&#xe42a;': '搪', '&#xe42c;': '听', '&#xe42f;': '启', '&#xe434;': '琴', '&#xe438;': '吸', '&#xe43d;': '落', '&#xe457;': '呗', '&#xe468;': '周', '&#xe473;': '味', '&#xe478;': '摸', '&#xe4a2;': '钢', '&#xe4c1;': '铁', '&#xe4cd;': '操', '&#xe4dd;': '蓝', '&#xe4ea;': '哪', '&#xe4ec;': '铬', '&#xe528;': '用', '&#xe52e;': '售', '&#xe530;': '田', '&#xe535;': '电', '&#xe539;': '改', '&#xe545;': '畅', '&#xe546;': '商', '&#xe54c;': '界', '&#xe559;': '教', '&#xe55c;': '镜', '&#xe55e;': '敞', '&#xe565;': '略', '&#xe566;': '啦', '&#xe584;': '薄', '&#xe597;': '斗', '&#xe59c;': '喜', '&#xe59d;': '疝', '&#xe5ad;': '断', '&#xe5b0;': '新', '&#xe5b7;': '喷', '&#xe5bc;': '疼', '&#xe5cf;': '族', '&#xe5d6;': '嗖', '&#xe5e0;': '无', '&#xe5e5;': '日', '&#xe5e8;': '门', '&#xe5f4;': '间', '&#xe60e;': '明', '&#xe613;': '易', '&#xe61f;': '星', '&#xe62f;': '是', '&#xe634;': '嘴', '&#xe635;': '阵', '&#xe63f;': '嘿', '&#xe64e;': '虎', '&#xe65a;': '虚', '&#xe664;': '除', '&#xe668;': '器', '&#xe66a;': '噪', '&#xe66f;': '景', '&#xe67a;': '智', '&#xe67e;': '百', '&#xe684;': '的', '&#xe694;': '隔', '&#xe697;': '暗', '&#xe6ae;': '皮', '&#xe6be;': '难', '&#xe6c5;': '雅', '&#xe6c8;': '盈', '&#xe6ca;': '益', '&#xe6d2;': '盒', '&#xe6d6;': '盖', '&#xe6d8;': '盘', '&#xe6db;': '四', '&#xe6ea;': '雪', '&#xe6f0;': '困', '&#xe6f2;': '曲', '&#xe6f4;': '围', '&#xe6f7;': '雷', '&#xe6fe;': '盾', '&#xe700;': '最', '&#xe707;': '震', '&#xe708;': '圈', '&#xe70b;': '看', '&#xe717;': '朗', '&#xe71f;': '真', '&#xe721;': '蜡', '&#xe728;': '在', '&#xe72c;': '本', '&#xe738;': '霸', '&#xe740;': '着', '&#xe750;': '坐', '&#xe751;': '坑', '&#xe752;': '青', '&#xe75e;': '非', '&#xe760;': '杠', '&#xe761;': '条', '&#xe762;': '面', '&#xe779;': '睹', '&#xe77e;': '松', '&#xe79c;': '果', '&#xe7ab;': '垫', '&#xe7df;': '域', '&#xe7e9;': '韩', '&#xe7ed;': '短', '&#xe7f3;': '石', '&#xe805;': '栅', '&#xe807;': '标', '&#xe835;': '堵', '&#xe84c;': '行', '&#xe851;': '塑', '&#xe854;': '塔', '&#xe861;': '衡', '&#xe86b;': '填', '&#xe86c;': '硬', '&#xe87f;': '顿', '&#xe884;': '预', '&#xe891;': '碑', '&#xe89e;': '增', '&#xe8a0;': '颠', '&#xe8a6;': '梦', '&#xe8b0;': '械', '&#xe8c5;': '装', '&#xe8ce;': '风', '&#xe8d9;': '飙', '&#xe8de;': '飞', '&#xe8e8;': '磨', '&#xe8ee;': '森', '&#xe907;': '备', '&#xe916;': '外', '&#xe91a;': '多', '&#xe927;': '大', '&#xe92a;': '太', '&#xe92e;': '央', '&#xe934;': '头', '&#xe93e;': '社', '&#xe947;': '奇', '&#xe95e;': '神', '&#xe962;': '奢', '&#xe965;': '奥', '&#xe970;': '饰', '&#xe973;': '女', '&#xe97a;': '祺', '&#xe97d;': '好', '&#xe97f;': '西', '&#xe98f;': '福', '&#xe996;': '首', '&#xe999;': '香', '&#xe9bb;': '离', '&#xe9c2;': '观', '&#xe9c4;': '规', '&#xe9c6;': '视', '&#xe9d1;': '科', '&#xe9d2;': '角', '&#xe9d8;': '秘', '&#xe9e6;': '触', '&#xe9fd;': '槽', '&#xea01;': '威', '&#xea21;': '模', '&#xea33;': '稳', '&#xea46;': '婆', '&#xea6c;': '马', '&#xea6d;': '驭', '&#xea70;': '驰', '&#xea71;': '驱', '&#xea76;': '驶', '&#xea7b;': '驻', '&#xea81;': '突', '&#xea84;': '窄', '&#xea8f;': '骏', '&#xead8;': '高', '&#xeb3e;': '款', '&#xeb49;': '等', '&#xeb63;': '正', '&#xeb65;': '步', '&#xeb7b;': '死', '&#xeb80;': '简', '&#xeb89;': '安', '&#xeb9a;': '定', '&#xeb9e;': '实', '&#xeba2;': '订', '&#xeba4;': '认', '&#xebb0;': '记', '&#xebb1;': '箱', '&#xebb6;': '家', '&#xebb9;': '容', '&#xebbd;': '宽', '&#xebbe;': '设', '&#xebc2;': '毂', '&#xebc4;': '评', '&#xebcc;': '富', '&#xebdb;': '毛', '&#xebed;': '语', '&#xebf8;': '寸', '&#xebfc;': '导', '&#xec03;': '调', '&#xec0f;': '小', '&#xec14;': '气', '&#xec1a;': '尚', '&#xec24;': '尤', '&#xec3e;': '尾', '&#xec49;': '汉', '&#xec4f;': '屏', '&#xec55;': '展', '&#xec61;': '象', '&#xec6a;': '豪', '&#xec7d;': '汽', '&#xec83;': '沃', '&#xec99;': '沙', '&#xec9f;': '沟', '&#xecad;': '岭', '&#xecb9;': '油', '&#xecbe;': '精', '&#xecca;': '泊', '&#xecfb;': '系', '&#xed20;': '素', '&#xed27;': '紧', '&#xed28;': '质', '&#xed35;': '贵', '&#xed39;': '费', '&#xed41;': '流', '&#xed44;': '资', '&#xed4b;': '测', '&#xed4e;': '济', '&#xed5b;': '赛', '&#xed5e;': '赞', '&#xed85;': '超', '&#xed8a;': '越', '&#xed8b;': '趋', '&#xeda1;': '涡', '&#xeda3;': '趣', '&#xeda8;': '涨', '&#xedb2;': '液', '&#xedb4;': '趴', '&#xedb5;': '涵', '&#xedc3;': '跃', '&#xedd1;': '跑', '&#xede1;': '巡', '&#xede8;': '巨', '&#xedee;': '差', '&#xedef;': '路', '&#xedf7;': '混', '&#xedfb;': '添', '&#xee00;': '一', '&#xee01;': '丁', '&#xee02;': '市', '&#xee03;': '七', '&#xee05;': '清', '&#xee07;': '万', '&#xee09;': '三', '&#xee0b;': '下', '&#xee0d;': '不', '&#xee0f;': '踏', '&#xee10;': '渐', '&#xee11;': '丑', '&#xee1c;': '东', '&#xee21;': '鸡', '&#xee29;': '温', '&#xee2a;': '个', '&#xee2d;': '中', '&#xee38;': '游', '&#xee58;': '乘', '&#xee5d;': '九', '&#xee5f;': '也', '&#xee70;': '买', '&#xee71;': '乱', '&#xee86;': '了', '&#xee8a;': '床', '&#xee8b;': '事', '&#xee8c;': '二', '&#xee8e;': '于', '&#xee90;': '源', '&#xee94;': '五', '&#xee9c;': '溜', '&#xeea2;': '红', '&#xeea6;': '度', '&#xeea7;': '座', '&#xeeab;': '身', '&#xeead;': '庭', '&#xeeae;': '亮', '&#xeeba;': '躺', '&#xeebf;': '线', '&#xeec0;': '什', '&#xeec1;': '仁', '&#xeec6;': '细', '&#xeecf;': '经', '&#xeed1;': '滑', '&#xeedf;': '统', '&#xeee1;': '满', '&#xeee3;': '代', '&#xeee4;': '滤', '&#xeee5;': '以', '&#xeef0;': '绰', '&#xeef7;': '价', '&#xeeff;': '绿', '&#xef00;': '开', '&#xef02;': '异', '&#xef04;': '弄', '&#xef0f;': '式', '&#xef17;': '弗', '&#xef24;': '伤', '&#xef38;': '缸', '&#xef39;': '弹', '&#xef3a;': '强', '&#xef4d;': '位', '&#xef4e;': '低', '&#xef50;': '齐', '&#xef51;': '网', '&#xef53;': '当', '&#xef59;': '余', '&#xef66;': '车', '&#xef6e;': '轮', '&#xef73;': '佳', '&#xef7d;': '载', '&#xef7f;': '轿', '&#xef88;': '很', '&#xef8e;': '美', '&#xef93;': '输', '&#xef9b;': '供', '&#xef9d;': '依', '&#xefa7;': '侧', '&#xefa9;': '辩', '&#xefb7;': '德', '&#xefb9;': '边', '&#xefbf;': '便', '&#xefc5;': '必', '&#xefc7;': '过', '&#xefdd;': '保', '&#xefe1;': '信', '&#xefeb;': '快', '&#xeffb;': '翻', '&#xeffc;': '翼', '&#xeffd;': '追'}
