# -*- coding:utf-8 -*-

# mongo
import os
from multiprocessing.pool import Pool
import pymongo
import time

con1 = pymongo.MongoClient('192.168.1.92', 27017)
db1 = con1['usedcar']

con2 = pymongo.MongoClient('114.67.64.181', 27017)
db2 = con2['usedcar']

websites = ["taoche", "youxin", "ttpai", "che168", "youxinpai",
            "guazi", "renrenche", "haoche51", "hx2car", "che168",
            "renrenche", "iautos", "souhu", "haoche99", "che273",
            "che101", "chewang", "xcar", "ganji", "zg2sc",
            "ygche", "che58", "youche", "cn2che", "chemao",
            "aokangda", "auto51", 'chezhibao']

def worker(website):
    t_start = time.time()
    print("开始执行,进程号为%d" % os.getpid())

    col1 = db1[website]
    col2 = db2[website]
    for i in col1.find():
        temp = dict()
        temp['url'] = i['url']
        temp['grabtime'] = i['grabtime']
        temp['website'] = i['website']
        temp['status'] = i['status']
        temp['pagetime'] = i['pagetime']
        col2.insert(temp)

    t_stop = time.time()
    print("执行完毕，耗时%0.2f" % (t_stop-t_start))


if __name__=="__main__":

    po = Pool(10)

    for website in websites:
        po.apply_async(worker, (website, ))


    print("----start----")
    start = time.time()

    po.close()
    po.join()

    print("-----end-----")
    stop = time.time()
    print('总用时：　%0.2f' %(stop - start))