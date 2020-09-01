# -*- coding: utf-8 -*-

# Scrapy settings for ganji project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ganji'

SPIDER_MODULES = ['ganji.spiders']
NEWSPIDER_MODULE = 'ganji.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ganji (+http://www.yourdomain.com)'
#the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
#for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY=True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 6
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ganji.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ganji.middlewares.MyCustomDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # 'ganji.rotate_useragent.RotateUserAgentMiddleware': 543,
    'ganji.rotate_useragent.ProxyMiddleware': 400,
    'ganji.rotate_useragent.SeleniumMiddleware': 300,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    }
# DOWNLOADER_MIDDLEWARES = {
#     #'mySpider.middlewares.MyCustomDownloaderMiddleware': 543,
#     'ganji.middlewares.RandomUserAgent': 1,
#     'ganji.middlewares.RandomProxy': 100
# }


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
HTTPERROR_ALLOWED_CODES=[]
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'ganji.pipelines.SomePipeline': 300,
#}

ITEM_PIPELINES = {'ganji.pipelines.GanjiPipeline':300, }
MONGODB_SERVER = "192.168.1.94"
MONGODB_PORT = 27017
MONGODB_DB = "usedcar"
MONGODB_COLLECTION = "xcar"
CrawlCar_Num = 2000000

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

#Mail settings
MAIL_FROM ="hzhy_1@163.com"
MAIL_HOST="smtp.163.com"
MAIL_PORT=25
MAIL_USER="hzhy_1@163.com"
MAIL_PASS="Hzhy@7115240"

#log
LOG_LEVEL="INFO"
#LOG_LEVEL="DEBUG"
#LOG_FILE ="scrapy.log"

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_TIMEOUT = 18
RETRY_TIMES = 8

# BLM_PATH = "blm/"
# PHANTOMJS_PATH = "D:/phantomjs.exe"
# CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# FIREFOX_PATH = "D:/geckodriver.exe"

BLM_PATH = "/home/usedcar/blm/"
PHANTOMJS_PATH = "/usr/local/phantomjs/bin/phantomjs"
CHROME_PATH = "/root/chromedriver"
FIREFOX_PATH = "/home/firefox/geckodriver"


RETRY_HTTP_CODES = [403]