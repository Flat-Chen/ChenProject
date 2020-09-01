# __author__ = 'cagey'
#
# from threading import Thread
# # from multiprocessing import Process, Queue
# import time
# import re
# import redis
# import pymongo
# from lxml import etree
# import requests
# import aiohttp
# import asyncio
# import sys
# sys.setrecursionlimit(100000000) # 设置最大递归调用次数
#
# pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
# con = redis.Redis(connection_pool=pool)
# c = con.client()
#
# connection = pymongo.MongoClient('192.168.2.149', 27017)
# db = connection["che300"]
# collection = db["che300_price_daily"]
#
#
# class Che300Spider(Thread):
#     def __init__(self, url):
#         super(Che300Spider, self).__init__()
#         self.c = c
#         self.url = url
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
#         }
#
#     def run(self):
#         self.parse_page()
#
#     def structure_http(self, result):
#         # 'https://m.che300.com/partner/result.php?prov=3&city=3&brand=50&series=569&model=23438&registerDate=2015-1&mileAge=0.1&intention=0&partnerId=wechat_01&unit=1&sld=sh'
#         meta = dict()
#         brand = re.search(r'brand=(.*?)&', result).group(1)
#         series = re.search(r'series=(.*?)&', result).group(1)
#         model = re.search(r'&model=(.*?)&', result).group(1)
#         mile = re.search(r'&mileAge=(.*?)&', result).group(1)
#         city = re.search(r'&city=(.*?)&', result).group(1)
#         prov = re.search(r'prov=(.*?)&', result).group(1)
#         registerDate = re.search(r'registerDate=(.*?)&', result).group(1)
#         meta['brand'] = brand
#         meta['series'] = series
#         meta['model'] = model
#         meta['registerDate'] = registerDate
#         meta['mile'] = mile
#         meta['city'] = city
#         meta['prov'] = prov
#         return meta
#
#     def send_request(self, url):
#         proxies = {
#             "http": "http://" + self.getProxy(),
#             "https": "http://" + self.getProxy()
#         }
#         # print(proxies)
#         try:
#             html = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=5)
#         except Exception as e:
#             print(e)
#             self.c.rpush('che300_price_daily:start_urls', url)
#             return False, False
#         print(html.status_code)
#         if html.status_code == 200:
#             return html.content, url
#         elif html.status_code == 500:
#             print(url)
#             return False, False
#         else:
#             # self.c.lpush('che300_price_daily:start_urls', url)
#             self.c.rpush('che300_price_daily:start_urls', url)
#             return False, False
#
#     def parse_page(self):
#         res, url = self.send_request(self.url)
#         if res:
#             meta = self.structure_http(url)
#             response = etree.HTML(res)
#             item = dict()
#             item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
#             item["url"] = url
#             item["price1"] = response.xpath("//li[@class='dealer_low_buy_price']/text()")[0]
#             item["price2"] = response.xpath("//div[@class='dealer_buy_price']/text()")[0]
#             item["price3"] = response.xpath("//li[@class='individual_low_sold_price']/text()")[0]
#             item["price4"] = response.xpath("//div[@class='individual_price']/text()")[0]
#             item["price5"] = response.xpath("//li[@class='dealer_low_sold_price']/text()")[0]
#             item["price6"] = response.xpath("//div[@class='dealer_price']/text()")[0]
#             item["price7"] = response.xpath("//li[@class='dealer_high_sold_price']/text()")[0]
#             item["brand"] = meta["brand"]
#             item["series"] = meta["series"]
#             item["salesdescid"] = meta["model"]
#             item["regDate"] = meta["registerDate"]
#             item["cityid"] = meta["city"]
#             item["prov"] = meta["prov"]
#             item["mile"] = meta["mile"]
#             print(item)
#             self.save_data(item)
#         else:
#             print("*"*100)
#
#     def save_data(self, item):
#         data_list = list()
#         data_list.append(item)
#         collection.insert(data_list)
#         print("insert data in mongo ....")
#
#
#     def getProxy(self):
#         s = requests.session()
#         s.keep_alive = False
#         url_list = ['http://192.168.2.120:5000']
#         url = url_list[0]
#         # headers = {
#         #     'Connection': 'close',
#         # }
#         proxy = s.get(url, auth=('admin', 'zd123456')).text[0:-6]
#         return proxy
#
#
# def get_url_list():
#     num = c.llen('che300_price_daily:start_urls')
#     if num:
#         url_list = [c.lpop('che300_price_daily:start_urls') for _ in range(0, 4)]
#         try:
#             start_url_list = [bytes.decode(url) for url in url_list]
#         except Exception as e:
#             print(e)
#             return False
#         return start_url_list
#     else:
#         return False
#
# def main():
#     url_list = get_url_list()
#     if url_list:
#         # 保存进程
#         Process_list = []
#         # 创建并启动进程
#         while len(url_list) > 0:
#             url = url_list.pop()
#             if url:
#                 p = Che300Spider(url)
#                 p.start()
#                 Process_list.append(p)
#                 # 让主进程等待子进程执行完成
#                 for i in Process_list:
#                     i.join()
#                     # time.sleep(1)
#         else:
#             main()
#
#     else:
#         while True:
#             print("队列为空....")
#             time.sleep(180)
#             main()
#
# if __name__ == "__main__":
#     main()
#
#
#

