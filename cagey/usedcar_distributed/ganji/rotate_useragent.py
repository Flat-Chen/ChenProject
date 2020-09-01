# -*-coding:utf-8-*-

import random

import time
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from selenium import webdriver


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        if spider.name in ['ganji', 'zg2sc']:
            ua = random.choice(self.user_agent_list)
            if ua:
                print('Current UserAgent: ' + ua)
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


class SeleniumMiddleware(object):

    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):

        if spider.name in ['anxinpai']:
            if 'http://www.haicj.com/bidcar' == request.url:
                driver = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
                i = 0
                while i < 10:
                    try:
                        driver.get(request.url)
                        time.sleep(5)
                    except Exception as e:
                        print(e)
                        i += 1
                        print('Fail Request-----{}, url-----{}'.format(i, driver.current_url))
                    else:
                        # print data
                        data = driver.page_source.encode()
                        driver.close()
                        driver.quit()

                        res = HtmlResponse(
                            url=request.url,
                            body=data,
                            request=request,
                            encoding='utf-8'
                        )
                        return res

                    driver.close()
                    driver.quit()

        if spider.name in ['auto51']:
            if 'http://m.51auto.com/quanguo/pabmdcigf' in request.url:
                cookies = [
                    'cd_sourceId=s-m-free; cd_switchboard=4000521093; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523698527; 51autoVisitorId=guest%3Ae6e63a43-6725-43fc-b3ca-d85a0de81a5b; _ga=GA1.2.24089723.1523698527; _gid=GA1.2.882426253.1523698527; _51utmb=1523698527410; _51utmc=1523698527410; _51utma=1523698527410,1327104.8805673048; JSESSIONID=C7A60FCC56CC5EF782F6C120E4617FC9; afpCT=1; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523698564'
                    ,
                    'Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523695233; _ga=GA1.2.842212965.1523695233; _gid=GA1.2.1507475153.1523695233; 51autoVisitorId=guest%3Ab50df49d-bf64-4a0e-ad1b-5008c81fa081; _51utmb=1523695233493; _51utmc=1523695233493; _51utma=1523695233493,1327104.811070412; cd_sourceId=s-m-other; cd_switchboard=4000513056; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523695606; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; JSESSIONID=2D790969DB7FF270F538F8DE3416C20A; afpCT=1'
                    ,
                    'cd_sourceId=s-m-other; cd_switchboard=4000513056; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; _ga=GA1.2.1726893497.1523699094; _gid=GA1.2.1837865391.1523699094; _gat_webapp=1; _gat_webapp2=1; 51autoVisitorId=guest%3A8e047acc-adf0-462f-b3e6-8e6527361059; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523699094; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523699094; _51utmb=1523699094314; _51utmc=1523699094314; _51utma=1523699094314,1327104.5653112668; JSESSIONID=11DCAD83E3FE044B1A82B67C052E3521; afpCT=1; _gat=1'
                    ,
                    'cd_sourceId=s-m-free; cd_switchboard=4000521093; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; _ga=GA1.2.530996948.1523699184; _gid=GA1.2.993246815.1523699184; _gat_webapp=1; _gat_webapp2=1; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523699184; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523699184; 51autoVisitorId=guest%3Ace7d4627-f89c-4cd6-82aa-0e0bd03edaad; _51utmb=1523699184289; _51utmc=1523699184289; _51utma=1523699184289,1327104.6762856871; JSESSIONID=AA4504D39D0A339B23C956CCE29A8EB4; afpCT=1; _gat=1'
                    ,
                    'cd_sourceId=s-m-free; cd_switchboard=4000521093; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523699286; _ga=GA1.2.1031008866.1523699286; _gid=GA1.2.25400196.1523699286; _gat_webapp=1; _gat_webapp2=1; 51autoVisitorId=guest%3A2a1a1fd5-5108-4a7d-9a1e-7887375ab6a3; _51utmb=1523699285795; _51utmc=1523699285795; _51utma=1523699285795,1327104.4631392253; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523699289; JSESSIONID=15AEABB1442FB904B37548902AC3C5BE; afpCT=1; _gat=1'
                    ,
                    'cd_sourceId=s-m-free; cd_switchboard=4000521093; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523699352; _ga=GA1.2.701277605.1523699353; _gid=GA1.2.1308089571.1523699353; _gat_webapp=1; _gat_webapp2=1; 51autoVisitorId=guest%3A16c42f47-0cc5-4798-baa7-995ccfc061ee; _51utmb=1523699352635; _51utmc=1523699352635; _51utma=1523699352635,1327104.419791403; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523699355; JSESSIONID=0A55AC2FAA3EF946D7698897428FE4E1; afpCT=1; _gat=1'
                    ,
                    'cd_sourceId=s-m-free; cd_switchboard=4000521093; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523699415; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523699415; _ga=GA1.2.211355773.1523699415; _gid=GA1.2.256374760.1523699415; _gat_webapp=1; _gat_webapp2=1; 51autoVisitorId=guest%3A4cc33ffb-1db9-419f-9729-6a2948a00c34; _51utmb=1523699415471; _51utmc=1523699415471; _51utma=1523699415471,1327104.7042803303; JSESSIONID=72F578784E2503599AC085FEC00F8B64; afpCT=1; _gat=1'
                    ,
                    'cd_sourceId=s-m-free; cd_switchboard=4000521093; currentLocationZoneDesc=%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; Hm_lvt_56505c7baf0b98dd0420c695e4f046a9=1523699467; Hm_lpvt_56505c7baf0b98dd0420c695e4f046a9=1523699467; _ga=GA1.2.681763895.1523699467; _gid=GA1.2.1340465226.1523699467; _gat_webapp=1; _gat_webapp2=1; 51autoVisitorId=guest%3A77d66703-3000-4990-9fac-9300b6586400; _51utmb=1523699466971; _51utmc=1523699466971; _51utma=1523699466971,1327104.8180396736; JSESSIONID=CA634EB272CD125E3097E15C95D10756; afpCT=1; _gat=1'
                    ]

                request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                request.headers['Cookie'] = random.choice(cookies)

            if 'http://m.51auto.com/buycar' in request.url:
                request.meta['proxy'] = "http://" + self.getProxy()
                print('proxy success !')


import requests

class ProxyMiddleware(object):

    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):

        if spider.name in ['che58']:
            request.headers['Host'] = ['www.58.com']

        if spider.name in ['ganji']:
            request.headers['Host'] = ['www.ganji.com']
            request.headers['User-Agent'] = [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
            request.headers['Accept-Language'] = ['zh-CN,zh;q=0.8']
            request.cookies = {
                'ganji_login_act':'1523022981942',
                'citydomain':'anshan',
                'xxzl_deviceid':'yMBly%2FZ%2FOm5mc2%2FOfTG0I8yP9v55zkxnv%2F7aOxeVYjmyCIVL7oIXvAgtA0EISHGG'
            }

        if spider.name in ['hx2car', 'che58', 'ganji', 'haoche51', 'youxin', 'renrenche', 'che168', 'che273', 'chemao', 'souhu']:
            request.meta['proxy'] = "http://" + self.getProxy()
            print('proxy success !')
            request.meta['download_timeout'] = 8
