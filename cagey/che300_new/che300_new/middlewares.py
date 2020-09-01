# -*- coding: utf-8 -*-
import requests
import base64
import logging
import json
import random
import redis
import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
from twisted.internet.error import TimeoutError

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver import FirefoxProfile
import traceback

logger = logging.getLogger(__name__)

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
c = con.client()


class Che300NewProxyMiddleware(object):
    def __init__(self):
        self.count = 0
        self.proxy = "http://" + getProxy()

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            self.proxy = "http://" + getProxy()
            request.meta['proxy'] = self.proxy
            print(f'Get a new ip {self.proxy}!')
            return request

    def process_request(self, request, spider):
        if spider.name in ['che300_futureprice', 'che300_price_daily', 'jzg_40city', 'che300_price_daily_sh_city',
                           'che300_price_daily_all_city']:
            # if self.count < 2:
            #     request.meta['proxy'] = self.proxy
            #     self.count += 1
            # else:
            #     self.proxy = "http://" + getProxy()
            #     self.count = 0
            proxy = getProxy()
            request.meta['proxy'] = "http://" + proxy
            # print(request.headers)
            print(f'proxy success : {self.proxy}!')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        print(response.status)
        if response.status in [403]:
            if spider.name in ['che300_price_daily']:
                # c.rpush('che300_price_daily:start_urls', request.url)
                print("push url in redis")
                print("-" * 100)
                print(response.status)
            # request.meta['proxy'] = "http://" + getProxy()
            # print('proxy success !')
            # return request
        elif response.status in [500]:
            print(response.url)
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response


def getProxy():
    s = requests.session()
    s.keep_alive = False
    url_list = ['http://192.168.2.120:5000']
    # random.shuffle(url_list)
    url = url_list[0]
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class Che300NewUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers.setdefault('User-Agent', ua)


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    ]


class MyproxiesSpiderMiddleware(RetryMiddleware):

    def __init__(self, name):
        super(MyproxiesSpiderMiddleware, self).__init__(name)



    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            print(response.headers)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        if '不合法' in response.body.decode("utf-8"):
            print(response.body.decode("utf-8"))
            reason = "不合法"
            return self._retry(request, reason, spider) or response
        if '未授权' in response.body.decode("utf-8"):
            print(response.body.decode("utf-8"))
            reason = "未授权"
            return self._retry(request, reason, spider) or response
        if '失败' in response.body.decode("utf-8"):
            print(response.body.decode("utf-8"))
            reason = "失败"
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            # ua = random.choice(user_agent_list)
            # request.headers.setdefault('User-Agent', ua)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            # 重新获取代理,添加代理
            proxy_ip = "http://" + getProxy()
            retryreq.meta['proxy'] = proxy_ip
            # retryreq.meta['headers'] = proxy_ip
            print(proxy_ip)
            print("-" * 100)

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            # if spider.name in ['che300_big_car_evaluate_sh_city']:
            #     c.lpush('che300_big_car_evaluate_sh_city:start_urls', request.url)
            # if spider.name in ['che300_big_car_evaluate_all_city']:
            #     c.lpush('che300_big_car_evaluate_all_city:start_urls', request.url)
            # if spider.name in ['che300_big_car_evaluate']:
            #     c.lpush('che300_big_car_evaluate:start_urls', request.url)
            # if response_status_message
            if spider.name in ['che300_big_car_evaluate_sh_city']:
                c.rpush('che300_price_daily:start_urls', request.url)
            if spider.name in ['che300_futureprice']:
                c.rpush('che300_futureprice:start_urls', request.url)
            if spider.name in ['che300_price_daily']:
                c.rpush('che300_price_daily:start_urls', request.url)
            if spider.name in ['che300_price_daily_sh_city']:
                c.rpush('che300_price_daily_sh_city:start_urls', request.url)
            if spider.name in ['che300_price_daily_all_city']:
                c.rpush('che300_price_daily_all_city:start_urls', request.url)
                print("push url in redis")
                print("-" * 100)
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})


class MoGuProxyMiddleware(object):
    def __init__(self):
        # self.proxyServer = "http://secondtransfer.moguproxy.com:9001"
        self.proxyServer = "http://transfer.mogumiao.com:9001"
        # 代理隧道验证信息,根据个人不同
        proxyUser = "pZU6DCgWGNVr6r4c"
        proxyPass = "Z0hT7xM3S6R1R2ov"
        appkey = "cFpVNkRDZ1dHTlZyNnI0YzpaMGhUN3hNM1M2UjFSMm92"
        self.proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode(
            "utf8")  # Python3
        # self.proxyAuth = "Basic" + appkey

    def process_request(self, request, spider):
        # if spider.name in ['youxin']:
        request.meta["proxy"] = self.proxyServer
        # request.headers["Proxy-Authorization"] = self.proxyAuth
        request.headers["Authorization"] = self.proxyAuth


class SeleniumMiddleware(object):
    """
    selenium 动态加载代理ip
    """

    def __init__(self, timeout=30):
        self.r = redis.Redis(host='192.168.2.149', db=5)
        self.cookie = self.r.get('che300_cookie').decode('utf8')
        self.r.close()
        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        #     "Cookie": self.cookie,
        # }
        self.cookie = {
            "name": "pcim",
            "value": "8b7c7256db284e01a54442e53d1cb896d0ca6d7b"
        }
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        # 去掉提示：Chrome正收到自动测试软件的控制
        options.add_argument('disable-infobars')
        # 禁止加载照片
        # profile.set_preference('permissions.default.image', 2)
        # 禁止加载css样式表
        profile.set_preference('permissions.default.stylesheet', 2)
        options.set_preference("dom.webnotifications.enabled", False)
        # 修改页面加载策略
        # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。

        # self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options,
        #                                  executable_path='/usr/bin/firefox')

        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        # 首先加载要添加cookie的网站, 然后添加cookie字典
        self.browser.get("https://www.che300.com/pinggu?from=bd_seo&rt=1590457829285")
        self.browser.add_cookie(self.cookie)

        self.timeout = timeout
        # self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout)  # 设置页面加载超时
        self.browser.set_script_timeout(self.timeout)  # 设置页面异步js执行超时
        # self.wait = WebDriverWait(self.browser, self.timeout, poll_frequency=0.5)


    def close_spider(self, spider):
        self.browser.quit()
        self.browser.close()

    def __del__(self):
        self.browser.quit()
        self.browser.close()

    def process_request(self, request, spider):
        if spider.name in ['che300_big_car_evaluate_sh_city']:
            proxy, ip, port = self.get_Proxy()
            self.set_proxy(self.browser, ip=ip, port=port)
            # browser = self.browser
            # 显示等待
            # self.wait.until(lambda browser: browser.find_element_by_class_name('tslb_b'))
            # 隐形等待
            # browser.implicitly_wait(10)
            main_win = self.browser.current_window_handle  # 记录当前窗口的句柄
            all_win = self.browser.window_handles
            try:
                if len(all_win) == 1:
                    logging.info("-------------------弹出保护罩-------------------")
                    js = 'window.open("https://www.baidu.com");'
                    self.browser.execute_script(js)
                    # 还是定位在main_win上的
                    for win in all_win:
                        if main_win != win:
                            print('保护罩WIN', win, 'Main', main_win)
                            self.browser.switch_to.window(main_win)
                # 此处访问你需要的URL
                self.browser.get(request.url)
                url = self.browser.current_url
                body = self.browser.page_source
                return HtmlResponse(url=url, body=body, encoding="utf-8")
            except:
                # 超时
                logging.info("-------------------Time out-------------------")
                # 切换新的浏览器窗口
                for win in all_win:
                    if main_win != win:
                        logging.info("-------------------切换到保护罩-------------------")
                        print('WIN', win, 'Main', main_win)
                        self.browser.close()
                        self.browser.switch_to.window(win)
                        main_win = win

                js = 'window.open("https://www.baidu.com");'
                self.browser.execute_script(js)
                if 'time' in str(traceback.format_exc()):
                    # print('页面访问超时')
                    logging.info("-------------------页面访问超时-------------------")

    def get_Proxy(self):
        url = 'http://192.168.2.120:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        ip = proxy.split(":")[0]
        port = proxy.split(":")[1]
        return proxy, ip, port

    def set_proxy(self, driver, ip='', port=0):
        driver.get("about:config")
        script = '''
                    var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
                    prefs.setIntPref("network.proxy.type", 1);
                    prefs.setCharPref("network.proxy.http", "{ip}");
                    prefs.setIntPref("network.proxy.http_port", "{port}");
                    prefs.setCharPref("network.proxy.ssl", "{ip}");
                    prefs.setIntPref("network.proxy.ssl_port", "{port}");
                    prefs.setCharPref("network.proxy.ftp", "{ip}");
                    prefs.setIntPref("network.proxy.ftp_port", "{port}");
        　　　　　　　 prefs.setBoolPref("general.useragent.site_specific_overrides",true);
        　　　　　　　 prefs.setBoolPref("general.useragent.updates.enabled",true);
                    '''.format(ip=ip, port=port)
        driver.execute_script(script)
