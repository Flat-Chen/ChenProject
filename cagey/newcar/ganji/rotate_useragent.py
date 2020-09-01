# -*-coding:utf-8-*-

import logging
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from selenium import webdriver
"""避免被ban策略之一：使用useragent池。

使用注意：需在settings.py中进行相应的设置。
"""

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        if spider.name != "autohome_newcar":
            ua = random.choice(self.user_agent_list)
            if ua:
                #显示当前使用的useragent
                #print "********Current UserAgent:%s************" %ua
                #记录
                logging.log(msg='Current UserAgent: ' + ua, level=logging.DEBUG)
                request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
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

class ProxyMiddleware(object):

    def process_request(self, request, spider):
        # if request.meta.has_key('proxy'):
        #     print request.meta['proxy'] + "--proxy"
        print("process request..." + request.url)
        if spider.name in ['pcauto_weibo_f','wechat_autohome','autohome_koubei_all', 'autohome_price_c_2019','autohome_newcar','autohome_dealer','autohome_newcar_updating','autohome_newcar_updating_fix', 'new_autohome_newcar_v3']:
            # print("newcar")
            print(self.getProxy())
            request.meta['proxy'] = "http://" + self.getProxy()

    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_response(self, request, response, spider):
        print(response.status)
        # print(response.url)
        # print(response.body)
        return response
        # if spider.name in ['58_office', '58_shop']:
        #     if response.status == 302 or response.status >= 400:
        #         print("http://" + self.getProxy())
        #         request.meta['proxy'] = "http://" + self.getProxy()
        #         # request.meta['ip'] = "http://" + self.getProxy()
        #         print(request.meta['proxy'])
        #         return request
        #     else:
        #         return response
        # else:
        #     return response



from scrapy.http import HtmlResponse
class SeleniumMiddleware(object):

    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):
        if spider.name in ['yiche_price','yiche_local_city_price_new', 'new_autohome_newcar_v2']:
            try:

                # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
                # proxy = webdriver.Proxy()
                # proxy.proxy_type = ProxyType.MANUAL
                # proxy.http_proxy = self.getProxy()
                # proxy.add_to_capabilities(desired_capabilities)
                # spider.browser.start_session(desired_capabilities)
                # spider.browser.set_page_load_timeout(12)

                spider.browser.get(request.url)
            except Exception as e:
                print(e)
                return request
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")