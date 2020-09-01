# -*- coding: utf-8 -*-

# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas
import pymongo
from datetime import datetime
from pybloom_live import ScalableBloomFilter
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy.exceptions import DropItem
import logging
from hashlib import md5
from scrapy.mail import MailSender
import scrapy
from sqlalchemy import create_engine
from ganji import car_parse


class GanjiPipeline(object):
    def __init__(self):
        # mail
        self.mailer = MailSender.from_settings(settings)

        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )

        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionwrong = db[settings['MONGODB_COLLECTION'] + "_wrongurllog"]

        # pybloom
        # num = (int(settings['CrawlCar_Num']) + self.collection.count()) * 1.1
        num = (int(200000) + self.collection.count()) * 1.1
        self.df = ScalableBloomFilter(initial_capacity=num, error_rate=0.01)

        # read
        print('original num :   ', self.collection.count())
        for i in self.collection.find():
            if "status" in i.keys():
                item = i["status"]
                item = md5(item.encode('utf8')).hexdigest()
                # print(item)
                self.df.add(item)
        # count
        self.start_time = datetime.now()
        self.counts = 0
        self.dupcounts = 0
        self.mongocounts = 0
        self.sqlcounts = 0
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(settings['MYSQLDB_USER'],
                                                                                         settings['MYSQLDB_PASS'],
                                                                                         settings['MYSQLDB_SERVER'],
                                                                                         settings['MYSQLDB_PORT'],
                                                                                         settings['MYSQLDB_DB']),
                                    encoding='utf-8')
        self.table = settings['MONGODB_COLLECTION'] + '_online'
        self.items = []
        self.caritemlist = car_parse.Parse_conf(settings['MONGODB_COLLECTION'])

    def process_item(self, item, spider):

        self.counts += 1

        valid = True
        i = md5(item['status'].encode('utf8')).hexdigest()
        print(i)

        # 布隆过滤器去重
        returndf = self.df.add(i)
        print(returndf)

        # 判断是否是错误的response
        if item['url'].find('error') == -1:
            iserror = False
        else:
            iserror = True
        print(iserror)

        if returndf or iserror:
            valid = False
        else:
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))

        print(valid)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        if valid:
            # 存入mongodb
            temp = dict()
            temp['url'] = item['url']
            temp['grabtime'] = item['grabtime']
            temp['website'] = item['website']
            temp['status'] = item['status']
            temp['pagetime'] = item['pagetime']
            self.collection.insert(temp)
            self.mongocounts += 1

            # mysql save
            if settings['MONGODB_COLLECTION'] in ["taoche", "youxin", "ttpai", "che168", "youxinpai", "guazi",
                                                  "renrenche", "haoche51", "hx2car", "che168", "renrenche", "iautos",
                                                  "souhu", "haoche99", "che273", "che101", "chewang", "xcar", "ganji",
                                                  "zg2sc", "ygche", "che58", "youche", "cn2che"]:
                # 解析信息页面
                domtext = scrapy.selector.Selector(text=item["datasave"][1])
                parsed_item = car_parse.ILikeParse(self.caritemlist, item, domtext)
                self.items.append(parsed_item)
                self.items = self.savedata(self.items, self.table, self.engine, 1)

            elif settings['MONGODB_COLLECTION'] in ["chemao", "aokangda", "auto51", 'chezhibao', 'anxinpai']:
                # 解析列表节点数据
                domtext = scrapy.selector.Selector(text=item["datasave"][0])
                parsed_item = car_parse.ILikeParse(self.caritemlist, item, domtext)
                self.items.append(parsed_item)
                self.items = self.savedata(self.items, self.table, self.engine, 1)

        elif iserror:
            logging.log(msg="Car Error!", level=logging.INFO)
            # log save
            urlog = {'url': item['url'], 'grabtime': item['grabtime']}
            self.collectionwrong.insert(urlog)

        else:
            self.dupcounts += 1
            logging.log(msg="Car duplicated!", level=logging.INFO)

        return item

    def close_spider(self, spider):
        self.connection.close()

        self.savefinal(self.items, self.table, self.engine)

        # 爬取情况记录
        end_time = datetime.now()
        info = dict()
        info['start_time'] = str(self.start_time)
        info['end_time'] = str(end_time)
        info['cost_time'] = (end_time - self.start_time).seconds
        info['cost_hour'] = round((end_time - self.start_time).seconds / 3600, 2)
        info['website'] = settings['MONGODB_COLLECTION']
        info['total_count'] = self.collection.count()
        info['unit_count'] = self.counts
        info['mongodb_count'] = self.mongocounts
        info['mysql_count'] = self.sqlcounts
        info['duplicate_count'] = self.dupcounts

        try:
            df = pandas.DataFrame([info])
            df.to_sql(name='spider_info', con=self.engine, if_exists='append', index=False)
        except Exception as e:
            print(e)
            print("add to spider_info fail")

        self.mailer.send(to=["1573480512@qq.com"], subject=settings['MONGODB_COLLECTION'],
                         body="Scrapy Finished! \n"
                              + 'start_time:  ' + str(self.start_time) + '\n'
                              + 'end_time:  ' + str(end_time) + '\n'
                              + 'cost_time:  ' + str((end_time - self.start_time).seconds) + '\n'
                              + 'cost_hour:  ' + str(round((end_time - self.start_time).seconds / 3600, 2)) + '\n'
                              + 'website:  ' + settings['MONGODB_COLLECTION'] + '\n'
                              + 'total_count:  ' + str(self.collection.count()) + '\n'
                              + 'unit_count:  ' + str(self.counts) + '\n'
                              + 'mongodb_count:  ' + str(self.mongocounts) + '\n'
                              + 'mysql_count:  ' + str(self.sqlcounts) + '\n'
                              + 'duplicate_count:  ' + str(self.dupcounts) + '\n'
                         )

        if (self.mongocounts != 0 and self.sqlcounts != 0):
            # 异常数据超过一半
            if (self.sqlcounts / self.mongocounts < 0.5):
                self.mailer.send(to=["1573480512@qq.com"], subject=settings['MONGODB_COLLECTION'],
                                 body="Website update!" + settings['MONGODB_COLLECTION'])

    def savedata(self, items, tablename, engine, savesize=1):
        error = True
        count = 0
        print(len(items))

        if len(items) == savesize:
            while error and count == 0:
                print("XXXX")
                try:
                    # pandas解析数据
                    df = pandas.DataFrame(items)
                    df.to_sql(name=tablename, con=engine, if_exists='append', index=False)

                    self.sqlcounts += 1
                    logging.log(msg="add to SQL", level=logging.INFO)
                    error = False
                except Exception as e:
                    print(e)
                    print("MARK")
                    if str(e).find("pymysql.err.InternalError") >= 0:
                        try:
                            self.engine = create_engine(
                                'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(settings['MYSQLDB_USER'],
                                                                                     settings['MYSQLDB_PASS'],
                                                                                     settings['MYSQLDB_SERVER'],
                                                                                     settings['MYSQLDB_PORT'],
                                                                                     settings['MYSQLDB_DB']),
                                encoding='utf-8')
                        except Exception as e:
                            print(e)
                            items = []

                    error = True
                    count = 1
            items = []
        return items

    def savefinal(self, items, tablename, engine):
        """截留下来的异常items保存"""

        if len(items) != 0:
            df = pandas.DataFrame(items)
            self.sqlcounts += len(items)
            df.to_sql(name=tablename, con=engine, if_exists='append', index=False)
