# -*- coding: utf-8 -*-
import logging
import pymongo
import pandas as pd
from usedcar import car_parse
from sqlalchemy import create_engine
from scrapy.exceptions import DropItem
from usedcar.redis_bloom import BloomFilter
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class UsedcarPipeline(object):
    def __init__(self):
        print("start_save")
        # pybloom
        self.bf = BloomFilter(key='bf_' + settings['WEBSITE'])
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(settings['MYSQLDB_USER'],
                                                                                         settings['MYSQLDB_PASS'],
                                                                                         settings['MYSQLDB_SERVER'],
                                                                                         settings['MYSQLDB_PORT'],
                                                                                         settings['MYSQLDB_DB']),
                                    encoding='utf-8')
        self.table = settings['WEBSITE']+ '_online'

        # mongo
        #self.connection = pymongo.MongoClient(
            #settings['MONGODB_SERVER'],
            #settings['MONGODB_PORT']
        #)
        #db = self.connection[settings['MONGODB_DB']]
        #self.collection = db[settings['WEBSITE']]
        #self.mongocounts = 0

        self.items = []

    def process_item(self, item, spider):

        if not item:
            raise DropItem("Missing {0}!".format(item))

        # 布隆过滤器去�?        
        returndf = self.bf.isContains(item['status'])
        logging.log(msg="redis_bloom :  {}".format(returndf), level=logging.INFO)

        if not returndf:
            # mongo
            #self.collection.insert(dict(item))
            #logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            #self.mongocounts += 1
            #logging.log(msg="scrapy " + str(self.mongocounts) + " mongodb items", level=logging.INFO)

            # mysql save
            parsed_item = car_parse.parse_text(settings['WEBSITE'], item)
            self.items.append(parsed_item)
            self.items = self.save_data(self.items, self.table, 1)

            # redis_bloom
            self.bf.insert(item['status'])

        else:
            logging.log(msg="Car duplicated!", level=logging.INFO)

        return item

    def close_spider(self, spider):
        self.save_data(self.items, self.table, 1)

    def save_data(self, items, tablename, savesize=1):
        if len(items) >= savesize:
            try:
                df = pd.DataFrame(items)
                df.to_sql(name=tablename, con=self.engine, if_exists='append', index=False)
                logging.log(msg="add to SQL",level=logging.INFO)
            except Exception as e:
                print(e)
                print(items)
            items = []
        return items
