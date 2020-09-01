# -*- coding: utf-8 -*-

# Scrapy settings for luntan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'luntan'

SPIDER_MODULES = ['luntan.spiders']
NEWSPIDER_MODULE = 'luntan.spiders'

# HTTPERROR_ALLOWED_CODES = [418]
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODECS = [503]
CRAWL_NUM = 2000000

"""luntan mongo"""
# MONGODB_SERVER = "192.168.1.94"
MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "luntan"
MONGODB_COLLECTION = "yiche"
CrawlCar_Num = 2000000

# REDIS_SERVER ="192.168.1.248"
# REDIS_PORT =6379

""" mysql 配置"""
MYSQL_DB = 'huachen'
MYSQL_TABLE = 'tousu'
MYSQL_PORT = '3306'
MYSQL_SERVER = '192.168.1.94'
MYSQL_USER = "dataUser94"
MYSQL_PWD = "94dataUser@2020"
# MYSQL_SERVER = '127.0.0.1'
# MYSQL_USER = "dataUser94"
# MYSQL_PWD = 'yangkaiqi'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'luntan (+http://www.yourdomain.com)'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'luntan.middlewares.LuntanSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'luntan.middlewares.ProxyMiddleware': 543,
    'luntan.middlewares.RotateUserAgentMiddleware': 542,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'luntan.pipelines.LuntanPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 增加调度配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 配置调度器持久化, 爬虫结束, 要不要清空Redis中请求队列和去重指纹的set。如果True, 就表示要持久化存储, 否则清空数据
SCHEDULER_PERSIST = False
# redis配置(下面有两种方式)
# 方式一：没有密码
# REDIS_HOST = '192.168.1.241'
# REDIS_PORT = 6379
REDIS_URL = 'redis://192.168.1.241:6379/10'
FEED_EXPORT_ENCODING = 'utf-8'

RETRY_HTTP_CODES = [301, 403, 503]
HTTPERROR_ALLOWED_CODES = [301, 403]  # 上面报的是403，就把403加入。
# 方式二：有密码
# REDIS_URL = 'redis://user:pass@hostname:6379'

# MYEXT_ENABLED: 是否启用扩展，启用扩展为 True， 不启用为 False
# IDLE_NUMBER: 关闭爬虫的持续空闲次数，持续空闲次数超过IDLE_NUMBER，爬虫会被关闭。默认为 360 ，也就是30分钟，一分钟12个时间单位

# MYEXT_ENABLED = True      # 开启扩展
# IDLE_NUMBER = 360           # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
# # # 在 EXTENSIONS 配置，激活扩展
# EXTENSIONS = {
#     'luntan.extensions.RedisSpiderSmartIdleClosedExensions': 500,
# }
