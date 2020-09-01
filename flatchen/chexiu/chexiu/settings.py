# -*- coding: utf-8 -*-

# Scrapy settings for chexiu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chexiu'

SPIDER_MODULES = ['chexiu.spiders']
NEWSPIDER_MODULE = 'chexiu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chexiu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

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
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'chexiu.middlewares.ChexiuSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'chexiu.middlewares.ChexiuDownloaderMiddleware': 543,
   #  'chexiu.middlewares.RotateUserAgentMiddleware': 1,
  'chexiu.middlewares.ChexiuNewProxyMiddleware': 100,
  'chexiu.middlewares.ChexiuNewUserAgentMiddleware': 101,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'chexiu.pipelines.ChexiuPipeline': 300,
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
# HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

RETRY_HTTP_CODES = [403]

SCHEDULER_PERSIST = False
REDIS_URL = 'redis://192.168.1.241:6379/15'
FEED_EXPORT_ENCODING = 'utf-8'

MONGODB_SERVER = "192.168.1.94"
MONGODB_PORT = 27017
MONGODB_DB = "chexiu"
MONGODB_COLLECTION = "chexiu"
CrawlCar_Num = 2000000




WEBSITE = ''


PCAUTO_DIC = {
  "基本参数-车型名称": "salesdesc",
  "基本参数-厂商指导价(元)": "price",
  "基本参数-厂商": "factoryname",
  "基本参数-级别": "level",
  "基本参数-上市时间": "salemonth",
  "基本参数-发动机": "motor",
  "基本参数-进气形式": "method",
  "基本参数-最大马力(PS)": "maxps",
  "基本参数-最大扭矩(N·m)": "maxnm",
  "基本参数-变速箱": "gear",
  "基本参数-车身类型": "bodystyle",
  "基本参数-长×宽×高(mm)": "lengthwh",
  "基本参数-轴距(mm)": "wheel",
  "基本参数-最高车速(km/h)": "maxspeed",
  "基本参数-官方0-100km/h加速(s)": "accelerate",
  "基本参数-实测0-100km/h加速(s)": "actualaccelerate",
  "基本参数-实 测100-0km/h制动(m)": "actualstop",
  "基本参数-实测油耗(L/100km)": "jbcs_ssyh",
  "基本参数-工信部综合油耗(L/100km)": "petrol",
  "基本参数-整车质保": "warranty",
  "车身-车身类型": "type",
  "车身-长度(mm)": "length",
  "车身-宽度(mm)": "width",
  "车身-高度(mm)": "height",
  "车身-轴距(mm)": "wheel",
  "车身-前轮距(mm)": "frontgauge",
  "车身-后轮距(mm)": "backgauge",
  "车身-最小离地间隙(mm)": "liftoff_distance",
  "车身-车重(kg)": "weight",
  "车身-车门数(个)": "doors",
  "车身-座位数(个)": "seats",
  "车身-油箱容积(L)": "fuelvolumn",
  "车身-行李厢容积(L)": "baggage",
  "车身-行李厢最大容积(L)": "maxbaggage",
  "车身-行李厢内部尺寸(mm)": "cs_xlxnbcc",
  "发动机-发动机型号": "motortype",
  "发动机-排量(mL)": "cylinder",
  "发动机-进气形式": "method1",
  "发动机-最大马力(PS)": "maxps1",
  "发动机-最大功率(kW)": "maxpower",
  "发动机-最大功率转速(rpm)": "maxrpm",
  "发动机-最大扭矩(N·m)": "maxnm1",
  "发动机-最大扭矩转速(rpm)": "maxtorque",
  "发动机-气缸排列形式": "lwv",
  "发动机-气缸数(个)": "lwvnumber",
  "发动机-每缸气门数(个)": "valve",
  "发动机-压缩比": "compress",
  "发动机-配气机构": "valve_gear",
  "发动机-缸径(mm)": "cylinder_diameter",
  "发动机-行程(mm)": "cylinder_travel",
  "发动机-发动机特有技术": "motortechnique",
  "发动机-燃料形式": "fuletype",
  "发动机-燃油标号": "fulevolumn",
  "发动机-供油方式": "fulemethod",
  "发动机-缸盖材料": "cylinder_head_material",
  "发动机-缸体材料": "cylinder_body_material",
  "发动机-排放标准": "emission",
  "变速箱-简称": "geardesc",
  "变速箱-挡位个数": "gearnumber",
  "变速箱-变速箱类型": "geartype",
  "底盘转向-驱动方式": "driveway",
  "底盘转向-前悬挂类型": "fronthang",
  "底盘转向-后悬挂类型": "backhang",
  "底盘转向-转向助力类型": "assistanttype",
  "底盘转向-车体结构": "body_structure",
  "车轮制动-前制动器类型": "frontbrake",
  "车轮制动-后制动器类型": "backbrake",
  "车轮制动-驻车制动类型": "parking_brake_type",
  "车轮制动-前轮胎规格": "frontwheel",
  "车轮制动-后轮胎规格": "backwheel",
  "车轮制动-备胎规格": "sparewheel",
  "车轮制动-备胎尺寸": "sizewheel",
  "主动安全配置-ABS防抱死": "zdaqpz_ABSfbs",
  "主动安全配置-制动力分配(EBD/CBC等)": "zdaqpz_zdlfp",
  "主动安全配置-刹车辅助(EBA/BAS/BA等)": "zdaqpz_scfz",
  "主动安全配置-牵引力控制(ASR/TCS/TRC等)": "zdaqpz_qylkz",
  "主动安全配置-车身稳定控制(ESP/DSC/ESC等)": "zdaqpz_cswdkz",
  "主动安全配置-胎压监测装置": "zdaqpz_tywdzz",
  "主动安全配置-防爆轮胎": "zdaqpz_fblt",
  "主动安全配置-安全带未系提示": "zdaqpz_aqwxts",
  "主动安全配置-并线辅助": "zdaqpz_bxfz",
  "主动安全配置-车道偏离预警系统": "zdaqpz_cdplyjxt",
  "主动安全配置-车道保持辅助系统": "zdaqpz_cdbcfzxt",
  "主动安全配置-主动刹车/主动安全系统": "zdaqpz_zdsc_zdaqxt",
  "主动安全配置-道路交通标示识别": "zdaqpz_dljtbssb",
  "主动安全配置-疲劳驾驶提示": "zdaqpz_pljsts",
  "主动安全配置-夜视系统": "zdaqpz_ysxt",
  "被动安全配置-前排正面安全气囊": "bdaqpz_qpzmaqqn",
  "被动安全配置-前/后排侧气囊": "bdaqpz_q_hpcqn",
  "被动安全配置-前/后排头部气囊(气帘)": "bdaqpz_q_hptbqn",
  "被动安全配置-前排膝部气囊": "bdaqpz_qpxbqn",
  "被动安全配置-行人碰撞防护系统": "bdaqpz_xrpzfhxt",
  "被动安全配置-ISO FIX儿童座椅接口": "bdaqpz_ztzyjk",
  "防盗配置-发动机电子防盗": "fdpz_fdjdzfd",
  "防盗配置-车内中控锁": "fdpz_cnzks",
  "防盗配置-遥控钥匙": "fdpz_ykys",
  "防盗配置-远程启动": "fdpz_ycqd",
  "防盗配置-无钥匙启动系统": "fdpz_wysqdxt",
  "防盗配置-无钥匙进入系统": "fdpz_wysjrxt",
  "驾驶辅助配置-巡航系统": "jsfzpz_xhxt",
  "驾驶辅助配置-前/后雷达": "jsfzpz_q_hld",
  "驾驶辅助配置-泊车影像系统": "jsfzpz_bcyxxt",
  "驾驶辅助配置-车侧盲区影像系统": "jsfzpz_ccmqyxxt",
  "驾驶辅助配置-倒车动态提醒系统": "jsfzpz_dcdttxxt",
  "驾驶辅助配置-驾驶模式切换": "jsfzpz_jsmsqh",
  "驾驶辅助配置-发动机启停技术": "jsfzpz_fdjqtjs",
  "驾驶辅助配置-自动泊车入位": "jsfzpz_zdbcrw",
  "驾驶辅助配置-自动驾驶辅助": "jsfzpz_zdjsfz",
  "驾驶辅助配置-上坡辅助": "jsfzpz_spfz",
  "驾驶辅助配置-自动驻车": "jsfzpz_zdzc",
  "驾驶辅助配置-陡坡缓降": "jsfzpz_dphj",
  "驾驶辅助配置-可变悬挂": "jsfzpz_kbxg",
  "驾驶辅助配置-空气悬挂": "jsfzpz_kqxg",
  "驾驶辅助配置-可变转向比": "jsfzpz_kbzxb",
  "驾驶辅助配置-整体主动转向系统": "jsfzpz_ztzdzxxt",
  "驾驶辅助配置-前桥限滑差速器/差速锁": "jsfzpz_qqxhcsq",
  "驾驶辅助配置-中央差速器锁止功能": "jsfzpz_zycsqszgn",
  "驾驶辅助配置-后桥限滑差速器/差速锁": "jsfzpz_hqxhcsq",
  "外部配置-天窗类型": "wbpz_tclx",
  "外部配置-天窗尺寸(mm)": "wbpz_tccc",
  "外部配置-运动外观套件": "wbpz_ydwgtj",
  "外部配置-铝合金轮毂": "wbpz_lhjlg",
  "外部配置-电动吸合门": "wbpz_ddxhm",
  "外部配置-电动后备厢": "wbpz_ddhbx",
  "外部配置-后备厢感应开启": "wbpz_hbxgykq",
  "外部配置-电动后备厢位置记忆": "wbpz_ddhbxwzjy",
  "外部配置-车顶行李架": "wbpz_cdxlj",
  "外部配置-主动进气格栅": "wbpz_zdjqgs",
  "内部配置-方向盘材质": "nbpz_fxpcz",
  "内部配置-方向盘调节范围": "nbpz_fxptjfw",
  "内部配置-方向盘电动调节": "nbpz_fxpddtj",
  "内部配置-多功能方向盘": "nbpz_dgnfxp",
  "内部配置-方向盘换挡": "nbpz_fxphd",
  "内部配置-方向盘加热": "nbpz_fxpjr",
  "内部配置-方向盘记忆": "nbpz_fxpjy",
  "内部配置-行车电脑显示屏功能": "nbpz_xcdnxspgn",
  "内部配置-全液晶仪表盘": "nbpz_qyjybp",
  "内部配置-液晶仪表盘尺寸": "nbpz_yjybpcc",
  "内部配置-HUD抬头数字显示": "nbpz_HUDttszxs",
  "内部配置-车载行车记录仪": "nbpz_czxcjly",
  "内部配置-手机无线充电": "nbpz_sjwxcd",
  "座椅配置-座椅材质": "zypz_zycz",
  "座椅配置-运动风格座椅": "zypz_ydfgzy",
  "座椅配置-前排座椅高低调节": "zypz_qpzygdtj",
  "座椅配置-前排座垫倾角调节": "zypz_qpzdqjtj",
  "座椅配置-前排腰部支撑调节": "zypz_qpybzctj",
  "座椅配置-前排肩部支撑调节": "zypz_qpjbzctj",
  "座椅配置-主/副驾驶座电动调节": "zypz_z_fjszddtj",
  "座椅配置-副驾驶席座椅后排电动可调": "zypz_hpddkt",
  "座椅配置-后排座椅调节": "zypz_hpzytj",
  "座椅配置-后排座椅电动调节": "zypz_hpzyddtj",
  "座椅配置-电动座椅记忆": "zypz_ddzyjy",
  "座椅配置-前/后排座椅加热": "zypz_q_hpzyjr",
  "座椅配置-前/后排座椅通风": "zypz_q_hpzytf",
  "座椅配置-前/后排座椅按摩": "zypz_q_hpzyam",
  "座椅配置-后排座椅放倒形式": "zypz_hpzyfdxs",
  "座椅配置-第三排座椅": "zypz_dspzy",
  "座椅配置-座椅布局形式": "zypz_zybjxs",
  "座椅配置-前/后座中央扶手": "zypz_q_hzzyfs",
  "座椅配置-后排杯架": "zypz_hpbj",
  "空调配置-空调调节方式": "ktpz_kttjfs",
  "空调配置-温度分区控制": "ktpz_wdfqkz",
  "空调配置-后排独立空调": "ktpz_hpdlkt",
  "空调配置-后座出风口": "ktpz_hpcfk",
  "空调配置-车内PM2.5过滤装置": "ktpz_cnPM25glzz",
  "空调配置-车载空气净化器": "ktpz_czkqjhq",
  "空调配置-车载冰箱": "ktpz_czbx",
  "灯光配置-近光灯光源": "dgpz_jygdy",
  "灯光配置-远光灯光源": "dgpz_yjgdy",
  "灯光配置-自适应远近光灯": "dgpz_zsyyjgd",
  "灯光配置-日间行车灯": "dgpz_rjxcd",
  "灯光配置-自动头灯": "dgpz_zdtd",
  "灯光配置-转向辅助灯": "dgpz_zxfzd",
  "灯光配置-随动转向大灯(AFS)": "dgpz_sdzxdd",
  "灯光配置-前雾灯": "dgpz_qud",
  "灯光配置-前大灯雨雾模式": "dgpz_qddywms",
  "灯光配置-大灯高度可调": "dgpz_ddgdkt",
  "灯光配置-大灯清洗装置": "dgpz_ddqxzz",
  "灯光配置-大灯延时关闭": "dgpz_ddysgb",
  "灯光配置-车内氛围灯": "dgpz_cnfwd",
  "玻璃/后视镜-电动车窗": "bl_hsj_ddcc",
  "玻璃/后视镜-车窗一键升/降": "bl_hsj_ccyjs_j",
  "玻璃/后视镜-车窗防夹手功能": "bl_hsj_ccfjsgn",
  "玻璃/后视镜-防紫外线/隔热玻璃": "bl_hsj_fzwx_grbol",
  "玻璃/后视镜-后视镜电动调节": "bl_hsj_hsjddtj",
  "玻璃/后视镜-外后视镜加热": "bl_hsj_whsjjr",
  "玻璃/后视镜-后视镜电动折叠": "bl_hsj_hsjddzd",
  "玻璃/后视镜-后视镜锁车自动折叠": "bl_hsj_hsjsczdzd",
  "玻璃/后视镜-后视镜倒车自动下翻": "bl_hsj_hsjdczdxf",
  "玻璃/后视镜-后视镜记忆": "bl_hsj_hsjjy",
  "玻璃/后视镜-内/外后视镜自动防眩目": "bl_hsj_n_whsjzdfxm",
  "玻璃/后视镜-后风挡遮阳帘": "bl_hsj_hfdzyl",
  "玻璃/后视镜-后排侧遮阳帘": "bl_hsj_hpczyl",
  "玻璃/后视镜-后排侧隐私玻璃": "bl_hsj_hpcysbl",
  "玻璃/后视镜-遮阳板化妆镜": "bl_hsj_zybhzj",
  "玻璃/后视镜-后雨刷": "bl_hsj_hys",
  "玻璃/后视镜-感应雨刷": "bl_hsj_gyys",
  "多媒体配置-中控台彩色大屏": "dmtpz_zktcsdp",
  "多媒体配置-中控台大屏尺寸": "dmtpz_zktdpcc",
  "多媒体配置-中控屏操作方式": "dmtpz_zkpczfs",
  "多媒体配置-GPS导航系统": "dmtpz_GPSdhxt",
  "多媒体配置-实时路况信息显示": "dmtpz_sslkxxxx",
  "多媒体配置-手机互联/映射": "dmtpz_sjhl_ys",
  "多媒体配置-车联网": "dmtpz_clw",
  "多媒体配置-道路救援呼叫": "dmtpz_dljyhj",
  "多媒体配置-语音识别控制系统": "dmtpz_yysbkzxt",
  "多媒体配置-手势控制": "dmtpz_sskz",
  "多媒体配置-蓝牙/车载电话": "dmtpz_ly_czdh",
  "多媒体配置-中控液晶屏分屏显示": "dmtpz_zkyjpfpxs",
  "多媒体配置-车载电视": "dmtpz_czds",
  "多媒体配置-后排液晶屏": "dmtpz_hpyjp",
  "多媒体配置-后排中央控制系统": "dmtpz_hpzykzxt",
  "多媒体配置-接口类型": "dmtpz_jklx",
  "多媒体配置-220V/230V电源": "dmtpz_220V_230Vdy",
  "多媒体配置-后备厢12V电源接口": "dmtpz_hbx12Vdyjk",
  "多媒体配置-CD/DVD": "dmtpz_CD_DVD",
  "多媒体配置-扬声器品牌": "dmtpz_ysqpp",
  "多媒体配置-扬声器数量": "dmtpz_ysqsl",
  "多媒体配置-主动降噪系统": "dmtpz_zdjzxt",
  "颜色配置": "color_pz",
  "内饰颜色": "color_inner"
}

