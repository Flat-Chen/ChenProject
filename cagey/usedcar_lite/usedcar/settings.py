# -*- coding: utf-8 -*-

# Scrapy settings for usedcar project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'usedcar'

SPIDER_MODULES = ['usedcar.spiders']
NEWSPIDER_MODULE = 'usedcar.spiders'

#REDIS_SERVER = '192.168.1.248'
#REDIS_DB = 1

# DEFAULT_REQUEST_HEADERS = {
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'usedcar (+http://www.yourdomain.com)'
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
#the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY=True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'usedcar.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'usedcar.middlewares.MyCustomDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
        # 'usedcar.middlewares.RotateUserAgentMiddleware' :543,
        'usedcar.middlewares.SeleniumMiddleware': 600,
        'usedcar.middlewares.ProxyMiddleware': 700,
    }


# COOKIES_ENABLES=False

# HTTPERROR_ALLOWED_CODES=[]
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'usedcar.pipelines.SomePipeline': 300,
#}
ITEM_PIPELINES = {'usedcar.pipelines.UsedcarPipeline':300, }

# website
WEBSITE = 'anxinpai'

# mysql
# MYSQLDB_SERVER = "127.0.0.1"
# MYSQLDB_USER= "root"
# MYSQLDB_PASS= "mysql"
# MYSQLDB_PORT = 3306
# MYSQLDB_DB = "usedcar"

MYSQLDB_SERVER = "192.168.1.94"
MYSQLDB_USER= "root"
MYSQLDB_PASS= "Datauser@2017"
MYSQLDB_PORT = 3306
MYSQLDB_DB = "people_zb"

MONGODB_SERVER = "192.168.1.92"
MONGODB_PORT = 27017
MONGODB_DB = "usedcar"
MONGODB_COLLECTION = "xcar"

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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

REDIRECT_ENABLED = False

#log
LOG_LEVEL="INFO"
# DOWNLOAD_DELAY=0
#LOG_FILE ="scrapy.log"

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_TIMEOUT = 8
RETRY_TIMES = 8

PHANTOMJS_PATH = "/usr/local/phantomjs/bin/phantomjs"

REDIS_HOST = '192.168.1.92'
REDIS_DB = 4

