# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import json
import random
import time
import traceback
import re

import requests
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import HtmlResponse
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message

import logging

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver import ChromeOptions

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from scrapy import signals


logger = logging.getLogger(__name__)


from scrapy import signals


class MoGuProxyMiddleware(object):
    def __init__(self):
        self.proxyServer = "http://secondtransfer.moguproxy.com:9001"
        # 代理隧道验证信息,根据个人不同
        proxyUser = "ePHx8ip8PWr8yoNc"
        proxyPass = "boQxNI98K3UTBOnc"
        # appkey = "ZVBIeDhpcDhQV3I4eW9OYzpib1F4Tkk5OEszVVRCT25j"
        self.proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8") # Python3

    def process_request(self, request, spider):
        if spider.name in ['feijiu']:
            request.meta["proxy"] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers.setdefault('User-Agent', ua)


def getProxy():
    url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if spider.name in ['feijiu', 'ouyeel']:
            proxy = getProxy()
            request.meta['proxy'] = "http://" + proxy
            ua = random.choice(user_agent_list)
            request.headers.setdefault('User-Agent', ua)
            # print(request.headers)
            print(f'proxy success : {proxy}!')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if response.status == 403:
            request.meta['proxy'] = "http://" + getProxy()
            ua = random.choice(user_agent_list)
            request.headers.setdefault('User-Agent', ua)
            print(request.headers)
            print('proxy success !')
            return request
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

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
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        # if '访问太过于频繁,请输入验证码后再次访问!' in response.body.decode("utf-8"):
        #     reason = "访问太过于频繁,请输入验证码后再次访问!"
        #     return self._retry(request, reason, spider) or response
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
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            # 重新获取代理,添加代理
            proxy_ip = "http://" + getProxy()
            retryreq.meta['proxy'] = proxy_ip
            # print("-"*100)
            # print(request.url)
            # print(retries)
            # print(retryreq.meta['proxy'])
            # print("-"*100)

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})


def getProxy_new():
    url = 'http://192.168.1.241:8000/?count=50'
    headers = {
        'Connection': 'close',
    }
    r = requests.get(url, headers=headers)
    ip_ports_list = json.loads(r.text)
    ip_ports = random.choice(ip_ports_list)
    ip = ip_ports[0]
    port = ip_ports[1]
    proxies = {
        'http': 'http://%s:%s' % (ip, port),
        'https': 'https://%s:%s' % (ip, port)
    }
    # print(proxies)
    return proxies


class NewProxyMiddleware(object):
    def process_request(self, request, spider):
        if spider.name in ['feijiu', 'ouyeel']:
            proxy = getProxy_new()["http"]
            request.meta['proxy'] = proxy
            ua = random.choice(user_agent_list)
            request.headers.setdefault('User-Agent', ua)
            # print(request.headers)
            print(f'proxy success : {proxy}!')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if response.status == 403:
            request.meta['proxy'] = getProxy_new()["http"]
            ua = random.choice(user_agent_list)
            request.headers.setdefault('User-Agent', ua)
            print(request.headers)
            print('proxy success !')
            return request
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response


class SeleniumMiddleware(object):
    """
    selenium 动态加载代理ip
    """

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置中的时间片个数，默认为12个，1分钟
        # idle_number = crawler.settings.getint('IDLE_NUMBER', 12)
        timeout = 30
        # 实例化扩展对象
        ext = cls(crawler, timeout)
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        # crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def __init__(self, crawler, timeout):
        self.crawler = crawler
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        # options = ChromeOptions()
        # options.add_argument('--headless')
        # 去掉提示：Chrome正收到自动测试软件的控制
        options.add_argument('disable-infobars')
        # 禁止加载照片
        profile.set_preference('permissions.default.image', 2)
        # 禁止加载css样式表
        profile.set_preference('permissions.default.stylesheet', 2)
        options.set_preference("dom.webnotifications.enabled", False)
        # 修改页面加载策略
        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        # self.browser = webdriver.Chrome(options=options)

        # self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_profile=profile, firefox_options=options)
        # self.browser_detail = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.timeout = timeout
        self.browser.set_page_load_timeout(self.timeout)  # 设置页面加载超时
        self.browser.set_script_timeout(self.timeout)  # 设置页面异步js执行超时
        # self.wait = WebDriverWait(self.browser, self.timeout, poll_frequency=0.5)

    def __del__(self):
        self.browser.close()
        # self.browser_detail.close()

    def spider_closed(self, spider):
        self.browser.quit()
        print("浏览器已关闭!")

    def process_request(self, request, spider):
        if spider.name in ['ouyeel']:
            if "/search-ng/shop/" in request.url:
                # print(request.url)
                # proxy, ip, port = self.get_Proxy()
                # self.set_proxy(self.browser, ip=ip, port=port)
                browser = self.browser
                # 显示等待
                main_win = browser.current_window_handle  # 记录当前窗口的句柄
                all_win = browser.window_handles
                try:
                    if len(all_win) == 1:
                        logging.info("-------------------弹出保护罩-------------------")
                        js = 'window.open("https://www.baidu.com");'
                        browser.execute_script(js)
                        # 还是定位在main_win上的
                        for win in all_win:
                            if main_win != win:
                                print('保护罩WIN', win, 'Main', main_win)
                                browser.switch_to.window(main_win)
                    # 此处访问你需要的URL
                    browser.get(request.url)
                    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.ID, "shopSign_submit")))
                    # WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="service_call"]')))
                    # element = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@class="service_call"]')))
                    # WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="totalCount"]')))
                    # element = WebDriverWait(browser, 20).until(EC.visibility_of(browser.find_element(by=By.ID, value='font12 lt10')))
                    # element = WebDriverWait(browser, 20).until(EC.text_to_be_present_in_element_value((By.XPATH, '//div[@class="left_title"]'), u'在线客服'))
                    # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "shopSign_submit"))).click()
                    # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "m_qualityGrade"))).click()
                    # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "m_qualityGrade"))).click()
                    # print("*"*100)
                    # browser.save_screenshot('./1.png')
                    # 反复确认是0的真的是0
                    count = 0
                    while True:
                        page = str(browser.page_source)
                        num = re.findall("totalCount\">(.*?)</b>", page)[0]
                        if num == 0:
                            time.sleep(1)
                            count += 1
                            print(num)
                        else:
                            break
                        if count == 3:
                            break
                        print(num)
                    url = browser.current_url
                    body = browser.page_source
                    # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'竞价')]/preceding-sibling::input"))).click()
                    return HtmlResponse(url=url, body=body, encoding="utf-8", flags=[])
                except:
                    # 超时
                    logging.info("-------------------Time out-------------------")
                    # 切换新的浏览器窗口
                    for win in all_win:
                        if main_win != win:
                            logging.info("-------------------切换到保护罩-------------------")
                            print('WIN', win, 'Main', main_win)
                            browser.close()
                            browser.switch_to.window(win)
                            main_win = win

                    js = 'window.open("https://www.baidu.com");'
                    browser.execute_script(js)
                    if 'time' in str(traceback.format_exc()):
                        # print('页面访问超时')
                        logging.info("-------------------页面访问超时-------------------")


    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
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


class SeleniumFirefoxMiddleware(object):
    """
    selenium Firefox 加载资源详情页
    """
    def __init__(self, timeout=30):
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # 去掉提示：Chrome正收到自动测试软件的控制
        options.add_argument('disable-infobars')
        # 禁止加载照片
        profile.set_preference('permissions.default.image', 2)
        # 禁止加载css样式表
        # profile.set_preference('permissions.default.stylesheet', 2)
        # options.set_preference("dom.webnotifications.enabled", False)
        self.browser_detail = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.timeout = timeout
        self.browser_detail.set_page_load_timeout(self.timeout)  # 设置页面加载超时
        self.browser_detail.set_script_timeout(self.timeout)  # 设置页面异步js执行超时


    def __del__(self):
        self.browser_detail.close()

    def process_request(self, request, spider):
        if spider.name in ['ouyeel_detail']:
            if "buyer-ng" in request.url:
                browser_detail = self.browser_detail
                browser_detail.get(request.url)
                url = browser_detail.current_url
                body = browser_detail.page_source
                return HtmlResponse(url=url, body=body, encoding="utf-8")


