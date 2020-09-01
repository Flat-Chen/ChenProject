# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
import pathlib
import re
import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
from pybloom_live import ScalableBloomFilter
from hashlib import md5
from scrapy.exceptions import DropItem
import pymongo
import pymysql
from scrapy import signals


# from scrapy.utils.project import get_project_settings

# from .pushdata import push_data
# settings = get_project_settings()


class BaogangPipeline(object):

    def __init__(self, settings, idle_number, crawler):
        # mysql
        self.conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        # db = pymysql.connect(settings["MYSQL_SERVER"], settings["MYSQL_USER"], settings["MYSQL_PWD"], settings["MYSQL_DB"], charset='utf8', port=3306)
        # db = create_engine(f'mysql+pymysql://{"baogang"}:{"Baogang@2019"}@{"192.168.2.120"}:{"3306"}/{"baogang"}?charset=utf8')
        # mongo
        # uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
        # self.connection = pymongo.MongoClient(uri)
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        # self.collectionurllog = db[settings['MONGODB_COLLECTION'] + "_urllog"]
        # count
        self.mongocounts = 0
        self.dropcounts = 0

        # mongo 临时表
        self.collection_tmp = self.db[settings['MONGODB_COLLECTION'] + "_tmp"]

        # pandas
        self.df_end = pd.DataFrame()

        # redis 信号
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

        self.settings = settings
        self.CrawlCar_Num = 1000000
        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']
        # pybloom
        self.df = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)

        if os.path.exists(dirname):
            if os.path.exists(filename):
                self.fa = open(filename, "a")
            else:
                pathlib.Path(filename).touch()
                self.fa = open(filename, "a")
        else:
            os.makedirs(dirname)
            pathlib.Path(filename).touch()
            self.fa = open(filename, "a")

        with open(filename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                line = line.strip('\n')
                self.df.add(line)

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置中的时间片个数，默认为12个，1分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 12)
        # 实例化扩展对象
        ext = cls(crawler.settings, idle_number, crawler)
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def open_spider(self, spider):
        # if spider.name == 'ouyeel' or spider.name == 'ouyeel_detail' or spider.name == 'ouyeel_jj':
        if spider.name == 'ouyeel':
            collection_tmp = self.db[self.settings['MONGODB_COLLECTION'] + "_tmp"]
            collection_tmp.remove({})
        if spider.name == 'ouyeel_detail' or spider.name == 'ouyeel_jj':
            # 清空mysql临时表
            try:
                sql = "truncate table " + self.settings['MONGODB_COLLECTION'] + "_tmp"
                self.conn.connect().execute(sql)
            except:
                logging.info("表不存在")

    def process_item(self, item, spider):
        if spider.name == 'feijiu' or spider.name == 'crawl_feijiu':
            if item["isvip"] is False and item["mobile"] is None and item["comPhone"] is None:
                DropItem(item)
            # self.collection.insert(dict(item))
            # logging.log(msg="data added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
            # 数据存入mysql
            items = list()
            items.append(item)
            df = pd.DataFrame(items)
            order = ['_id', 'comType', 'comName', 'comAddress', 'vip_type', 'vip_year', 'comTrade', 'comProducts',
                     'area_auth', 'debao_auth', 'comIndex', 'kind', 'label_one', 'label_two', 'title', 'infoNum',
                     'type', 'quality', 'number', 'sale_price', 'public_time', 'market', 'linkMan', 'mobile',
                     'comPhone', 'info', 'isvip', 'list_url', 'url', 'grabtime']
            data_new = df[order]
            # print(data_new)
            data_new.to_sql(name=self.settings['MONGODB_COLLECTION'], con=self.conn, if_exists="append", index=False)
            logging.log(msg="add data in mysql", level=logging.INFO)

        elif spider.name == 'ouyeel':
            self.collection.insert(item)
            self.collection_tmp.insert(item)
            logging.log(msg="data added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

        elif spider.name in ['feijiu_url', 'minzheng', 'minzheng2', 'yiche_rank', 'yiche_bg_koubei']:
            items = list()
            items.append(item)
            df = pd.DataFrame(items)
            self.mongocounts += 1
            self.df_end = pd.concat([self.df_end, df])
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
            # self.df_end.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)

        elif spider.name in ['ouyeel_detail', 'ouyeel_jj']:
            if "线材" in item["product_name"]:
                DropItem(item)
                self.dropcounts += 1
            self.collection.insert(item)
            # self.collection_tmp.insert(item)
            logging.log(msg="data added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
            # 数据存入mysql
            items = list()
            items.append(item)
            df = pd.DataFrame(items)
            self.df_end = pd.concat([self.df_end, df])
            # df.to_sql(name=self.settings['MONGODB_COLLECTION']+'_tmp', con=self.conn, if_exists="append", index=False)
            # logging.log(msg=f"add              {self.mongocounts}             mysql", level=logging.INFO)
            logging.log(msg=f"drop              {self.dropcounts}              items", level=logging.INFO)
            # return item
        else:
            if spider.name in ["yiche_koubei_weidu", "yiche_model_paihang", 'yiche_koubei_new', 'autohome_news', 'yiche_news']:
                if spider.name in ["yiche_koubei_weidu"]:
                    i = md5(str(item['url']+item["series_score"]).encode("utf8")).hexdigest()
                else:
                    i = md5(item['url'].encode("utf8")).hexdigest()
                valid = True
                returndf = self.df.add(i)
                if not returndf:
                    valid = True
                else:
                    valid = False
                    raise DropItem(f"isexists data! --> {item['url']}")
                if valid:
                    # 刷新缓存区
                    self.fa.flush()
                    self.fa.writelines(i + '\r\n')
                    items = list()
                    items.append(item)
                    df = pd.DataFrame(items)
                    self.mongocounts += 1
                    df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                    logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

    def close_spider(self, spider):
        self.connection.close()
        self.conn.dispose()
        if spider.name in ['ouyeel_detail', 'ouyeel_jj', 'minzheng', 'feijiu_url', 'minzheng2', 'yiche_rank', 'yiche_bg_koubei', 'yiche_koubei_new']:
            self.df_end.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
            # logging.log(msg=f"add              {self.mongocounts}             mysql", level=logging.INFO)
            print("*"*100)

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数
        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]
        elif idle_list_len == self.idle_number + 1:
            # 触发n次以后,开始存取数据
            if spider.name in ['ouyeel_detail', 'ouyeel_jj']:
                self.df_end.to_sql(name=self.settings['MONGODB_COLLECTION'] + '_tmp', con=self.conn, if_exists="append", index=False)
                logging.log(msg=f"add              {self.mongocounts}             mysql", level=logging.INFO)
                self.df_end = pd.DataFrame()
                print("*" * 100)
            # # 连续触发的次数达到配置次数后关闭爬虫
            # # 执行关闭爬虫操作
            # self.crawler.engine.close_spider(spider, 'closespider_pagecount')


        # 通过datax推送数据
        # status, res = push_data(self.datax_path, self.ouyeel_job_path)
        # if status:
        #     logging.info(res)
        # else:
        #     logging.info("*"*100)
        #     logging.info(res)
        #     logging.info("运行失败!")
        #     logging.info("*" * 100)



