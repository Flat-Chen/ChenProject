# __author__ = 'cagey'
#
import requests
# import execjs
import re
#
# # 准备去爬的 URL 链接
# # url = "https://www.xin.com/40d0nl1ky9/che35539795.html?cityid=652300"
# url = 'https://www.xin.com/orwz2gpwq4/che25001254.html?cityid=2401'
# # # url = 'https://www.xin.com/shanghai/zhonghua/'
# # url = 'https://www.xin.com/ajax/opxsign'
url = "http://m.51auto.com/quanguo/pabmdcigf?ordering=publishTime&direction=2"
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
  'Cookie': '51autoVisitorId=guest%3A86c711f4-84ce-406c-9f2f-edc7d77ceed3'
}
#
r = requests.get(url, headers=headers)
res = r.text
print(res)


# code = re.findall("arg1='(.*?)'", r.content.decode('utf-8'))[0]
# print(code)
# Cookie = execjs.compile(open("youxin.js").read()).call('getpwd', code)
# print(Cookie)
# # Cookie = '5e169bbcaae355879757affb4b0a9aedf2cc4f19'
# headers1 = {
#   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#   'cookie': f'acw_sc__v2={Cookie}',
# }
#
# url = 'https://openapix.xin.com/report/report_main?source=pc'
# # url = 'https://www.xin.com/orwz2gpwq4/che25001254.html?cityid=2401'
# # url = 'https://www.xin.com/ajax/opxsign'
# res = requests.post(url=url, headers=headers1)
#
# formData = {"sn": "015d5cd4be30c92db40dafbd822518d1", "params":{"carid":"37189368","ajax":1,"type":3}}
#
# # res = requests.post(url, formData, headers=headers1)
#
# print(res.text)
# url = 'https://www.xin.com/shanghai/biyadi/'
# res = requests.get(url)
# print(res.text)