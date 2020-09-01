# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
import pathlib
import time

# from scrapy.utils.project import get_project_settings
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from pybloom_live import ScalableBloomFilter
from hashlib import md5
from scrapy.exceptions import DropItem
import pymongo


# settings = get_project_settings()


class KoubeiNewPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):

        # mysql
        self.conn = create_engine(
            f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        # mongo
        # uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
        # self.connection = pymongo.MongoClient(uri)
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION'] + "_urllog"]

        # date
        self.start_date = None
        self.end_date = None
        self.scrapy_date = f'{self.start_date}  -   {self.end_date}'

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

    def open_spider(self, spider):
        self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())

    def process_item(self, item, spider):
        if spider.name in ['yiche_koubei', "pauto_koubei_new", 'xcar_koubei_new', 'autohome_koubei_new', 'weibo',
                           'iautos_modellist', 'kbb']:
            valid = True
            i = md5(item['url'].encode("utf8")).hexdigest()
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
                # 数据存入mongo
                self.collection.insert(dict(item))
                logging.log(msg="data added to MongoDB database!", level=logging.INFO)
                self.mongocounts += 1
                # # 数据存入mysql
                # items = list()
                # items.append(item)
                # df = pd.DataFrame(items)
                # df.to_sql(name=self.settings['MONGODB_COLLECTION'], con=self.conn, if_exists="append", index=False)
                # logging.log(msg=f"insert        {self.mongocounts}        items       to      sql", level=logging.INFO)

            else:
                # self.dropcounts += 1
                raise DropItem(f"isexists data! --> {item['url']}")

        elif spider.name == 'yiche_luntan':
            self.collection.insert(item)
            logging.log(msg="data added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

    def close_spider(self, spider):
        self.connection.close()
        self.conn.dispose()
        self.fa.close()
        self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
        self.scrapy_date = f'{self.start_date}  -   {self.end_date}'
        logging.info(self.scrapy_date)
