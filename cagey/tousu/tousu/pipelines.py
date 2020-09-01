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
import pymysql
from pybloom_live import ScalableBloomFilter, BloomFilter
from hashlib import md5
from scrapy.exceptions import DropItem
import pymongo


class TousuPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mysql
        self.conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        # mongo
        # uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
        # self.connection = pymongo.MongoClient(uri)
        # self.connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = self.connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]
        # self.collectionurllog = db[settings['MONGODB_COLLECTION'] + "_urllog"]

        # count
        self.mongocounts = 0
        self.counts = 0
        self.CrawlCar_Num = 1000000
        self.settings = settings
        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']
        # pybloom
        self.df = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)
        # self.df = BloomFilter(capacity=self.CrawlCar_Num, error_rate=0.01)
        # # read
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

    def process_item(self, item, spider):
        if spider.name in ['a315tousu', 'qctsw', 'tousu315che', 'a12345auto', 'all_brand_qctsw', 'all_brand_315tousu', 'czw', 'all_brand_tousu315che']:
            valid = True
            i = md5(item['status'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            # if returndf or '一汽' in item["brand"]:
            if returndf:
                valid = False
                raise DropItem("Drop data {0}!".format(item["detail_url"]))
            else:
                pass
            if valid:
                self.fa.flush()
                self.fa.writelines(i + '\n')
                self.mongocounts += 1
                logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
                # 数据存入mysql
                items = list()
                items.append(item)
                df = pd.DataFrame(items)
                df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                logging.log(msg=f"add data in mysql", level=logging.INFO)
                # return item

    def close_spider(self, spider):
        self.conn.dispose()
        self.fa.close()