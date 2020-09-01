import io

import redis
import requests

__author__ = 'cagey'

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import sys
import pytesseract
from PIL import Image


def get_youxinpai_cookies():
    # 设置浏览器参数，伪装成浏览器
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")

    # 打开浏览器并访问指定地址
    driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', desired_capabilities=dcap)  # 构造网页驱动

    # 窗口调成最大，方便截图
    driver.maximize_window()
    driver.get('http://i.youxinpai.com/Login.aspx?ReturnUrl=%2fCorpAccount%2fCorpLinkManOrMessage.aspx')

    # 定位到需要截图的div，或者标签位置。
    imgelement = driver.find_element_by_xpath('//*[@id="imgCheckB"]')
    # 图片坐标。
    locations = imgelement.location
    print(locations)
    # 图片大小
    sizes = imgelement.size
    print(sizes)
    # 构造指数的位置，计算出需要截图的长宽、高度等
    rangle = (int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']), int(locations['y'] + sizes['height']+5))
    print(rangle)
    # 截取当前浏览器。path1：存储全屏图片，path2：存储二次截图的图片

    # 读取截屏图片
    full_image = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(full_image))
    # 根据上面的参数截取验证码图片
    code_image = image.crop(rangle)
    x, y = code_image.size
    code_image = code_image.resize((x*2, y*2))
    # code_image.show()
    # code_image.save('./test.png')
    # i = Image.open('./test.png')
    # 识别验证码图片
    checkCode = pytesseract.image_to_string(code_image)
    if len(checkCode) == 0:
        get_youxinpai_cookies()
        return False
    else:
        print("识别结果:" + checkCode)

    driver.find_element_by_xpath('//*[@id="username"]').send_keys('13301679752s')
    driver.find_element_by_xpath('//*[@id="pw"]').send_keys('123456a')
    driver.find_element_by_xpath('//*[@id="txtCheckCode"]').send_keys(checkCode)

    driver.find_element_by_xpath('//*[@id="Submit1"]').click()

    # log = driver.get_log("performance")
    # print(log)

    # time.sleep(2)
    cookies = driver.get_cookies()
    if len(cookies) == 2:
        get_youxinpai_cookies()

        return False
    else:
        # print(len(cookies))
        # print(cookies)
        cookie = [item['name'] + "=" + item['value'] for item in cookies ]
        cookiestr = ';'.join(item for item in cookie)
        headers_cookie ={
                   "Cookie": cookiestr         # 通过接口请求时需要cookies等信息
        }
        redis_cli = redis.Redis('127.0.0.1', port=6379, db=1)
        redis_cli.set('youxinpai_cookies', headers_cookie["Cookie"])
        # print(headers_cookie)

        return headers_cookie


# cookie = {"Hm_lpvt_5596319193662c5eba5ac2792ccb4e1b":"1569742921",
#           "Hm_lvt_5596319193662c5eba5ac2792ccb4e1b":"1569740245,1569740275,1569740602,1569742921",
#           "SERVERID":"7ccf6505e0d6219115cb44ecb2032828|1569742921|1569742917",
#           "TranstarAuction":"loginname=pRZ8MNEMlOBK8LYNjRyJ4w==",
#           ".ASPXAUTH":"1BF92A91C2C5D1385309D7F69E8D86284D25571E1CBE1190D146BFAFCD46F1EA476D397910C850BB45799A0F72D369232D4A3B856455405ADF058C93EEC98BDEEC1E9F8C1A3E45AAFB46F5F628B1FE35F91B16777B0FDFBFEFD7A9EBC597865AF35471968E968B30F0220F9FF8E22524009F91BF",
#           "jugeFirst":"0",
#           "ASP.NET_SessionId":"44ptc2w51asjcomrdeqqfmax"}


cookies = get_youxinpai_cookies()
if cookies:
    print(cookies)
# #

#
# redis_cli = redis.Redis('127.0.0.1', port=6379, db=1)
# re_cookie = redis_cli.get('youxinpai_cookies').decode('utf-8')
# c = {i.split("=")[0]: i.split("=")[1] for i in re_cookie.split(";")}
# # #
# print(c)
# cookies = {'Cookie': 'Hm_lpvt_5596319193662c5eba5ac2792ccb4e1b=1569735010;Hm_lvt_5596319193662c5eba5ac2792ccb4e1b=1569734391,1569734755,1569734854,1569735010;SERVERID=7ccf6505e0d6219115cb44ecb2032828|1569735009|1569735006;TranstarAuction=loginname=pRZ8MNEMlOBK8LYNjRyJ4w==;.ASPXAUTH=9E6BDE09039EEAAC4FD8612D0A5F832C98AE682961049960F42CFF904F6656829922A83D84AB25C78F63FC2D62608364F28381AD7BF172921B551E93E4D29622CF1EF807A8BA55120748B121624CB2801DCE099BA0CD2B908240687C763C57825CF0B7B7EA0B2642511C03032A3B15ECE365A583;jugeFirst=0;ASP.NET_SessionId=w0z5dzbcp4wzxzbrjfkejopo'}
# headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
# headers = {'Cookie': 'Hm_lpvt_5596319193662c5eba5ac2792ccb4e1b=1569736722;Hm_lvt_5596319193662c5eba5ac2792ccb4e1b=1569734755,1569734854,1569735828,1569736722;SERVERID=7ccf6505e0d6219115cb44ecb2032828|1569736721|1569736717;TranstarAuction=loginname=pRZ8MNEMlOBK8LYNjRyJ4w==;.ASPXAUTH=420A856AAADB8CEA60EB6F6DCE147F4ADD64C589090B88E012F07421219D085B7438C0C12166C2ED6BE205506D3181F0A1266EAFAFEE5F8918A7E41BDCC02C8AD2ABCE063C975177DDB05BF8FDD0C7BF1B6A75002C6858AA09A0432C4D9E8C31A8BA15BD5C5482175B3F2FCA434167B44A82143B;jugeFirst=0;ASP.NET_SessionId=uxyrtewbq50ujp4g4gb0qlk1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
# headers = {'Cookie': f'{re_cookie}'}
# url = 'http://i.youxinpai.com/LoginFromPCClient.aspx?key=5LFu9AuZj+n4mmgHy5M3iIGhoASQzWKXlBklKbTf79X6+ygV/W1bN21JQ4s69XKV&Redirect=http://i.youxinpai.com/Default.aspx'
# url = "http://i.youxinpai.com/TradeManage/TradeList.aspx?masterBrand=2000000004&serial=2000002654"
# # url = "http://i.youxinpai.com/TradeManage/TradeList.aspx?masterBrand=2000000059&serial=2000002007"
# # # url = "http://i.youxinpai.com/TradeManage/TradeList.aspx?masterBrand=%202000000089&serial=li_2000001380"
# # # # url = "http://i.youxinpai.com/AjaxObjectPage/SellCarTypePageTrade.ashx?carAreaID=40"
# response = requests.get(url=url, cookies=c)
# # response = requests.get(url=url, headers=headers)
# res = response.content.decode('utf-8')
# print(res)














# driver.get_screenshot_as_file('验证码.jpg')                   # 截取当前页面的图片
# input_solution = input('请输入验证码 :')  手工打码
# driver.find_element_by_xpath('//input[@name="captcha"]').send_keys(input_solution)
# print(driver.title)

# def parse_img(img_url):
#     data = requests.get(url=img_url).content
#     image = Image.open(io.BytesIO(data))
#     x, y = image.size
#     try:
#         # (alpha band as paste mask).
#         p = Image.new('RGBA', image.size, (0, 0, 0))
#         p.paste(image, (0, 0, x, y), image)
#         # p.show()
#         # p.save('test.png')
#     except:
#         return "错误!"
#     vcode = pytesseract.image_to_string(p, lang='eng').strip()
#     return vcode
#
# code = parse_img(img_url)
# print(code)

