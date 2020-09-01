__author__ = 'cagey'

import bson
import pandas as pd
import pymongo
import redis
from datetime import datetime

from pandas.core.frame import DataFrame
from random import shuffle

settings = {
    "MYSQL_USER": "dataUser94",
    "MYSQL_PWD": "94dataUser@2020",
    "MYSQL_SERVER": "192.168.1.94",
    "MYSQL_PORT": "3306",
    "MYSQL_DB": "jzg",
    "MYSQL_TABLE": "content_senti",
    "MONGODB_SERVER": "192.168.1.94",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "che300",
    "MONGODB_COLLECTION": "che300_price_daily_sh_city",
    "MONGODB_USER": "admin",
    "MONGODB_PWD": "ABCabc123"
}
pd.set_option('display.max_columns', None)

# redis_url = 'redis://192.168.1.241:6379/15'
pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()

lens = r.llen("che300_price_daily:start_urls")
print(f"正在抓取的数据量:{lens}")
if lens < 0:
    print("队列中还有数据...")
else:
    uri1 = f'mongodb://192.168.2.149:{settings["MONGODB_PORT"]}/'
    # connection = pymongo.MongoClient(uri1, unicode_decode_error_handler='ignore')
    connection = pymongo.MongoClient(uri1)

    db = connection['che300']
    collection = db['che300_price_daily']
    # collection = collection.with_options(codec_options=bson.CodecOptions(unicode_decode_error_handler="ignore"))

    uri2 = f'mongodb://192.168.1.92:{settings["MONGODB_PORT"]}/'
    connection2 = pymongo.MongoClient(uri2)
    db2 = connection2[settings['MONGODB_DB']]
    collection2 = db2['che300_41city_url']
    model_data = collection.find({}, {"url": 1, "_id": 0})

    car_msg_df = DataFrame(list(model_data))
    car_msg_df = car_msg_df.drop_duplicates('url')
    have_num = car_msg_df["url"].count()
    print(f"现有数据量:{have_num}")

    model_data2 = collection2.find({}, {"url": 1, "_id": 0})
    car_msg_df2 = DataFrame(list(model_data2)).drop_duplicates('url')
    all_num = car_msg_df2["url"].count()
    print(f"总共数据量:{all_num}")

    df_a_filter = car_msg_df2[~ car_msg_df2['url'].isin(car_msg_df['url'])]
    miss_num = df_a_filter["url"].count()
    print(f"缺少数据量:{miss_num}")

    miss_sid_list = [1373449 , 1373450 , 1373451 , 1373455 , 1400877 , 1400879 , 1400880 , 1400976 , 1401128 , 1401129 , 1401130 , 1401131 , 1401134 , 1401137 , 1401138 , 1401141 , 1373456 , 1373457 , 1401132 , 1401133 , 1401139 , 1401140]
    print(len(miss_sid_list))
    # na_sid_list = ["1358532", "1367052", "1369333", "1369334", "1401035"]
    #
    # miss_url_list = df_a_filter.values
    # shuffle(miss_url_list)
    # url_list = []
    # if miss_num > 0:
    #     for url in miss_url_list:
    #         url = url[0]
    #         # for na_sid in na_sid_list:
    #         #     if na_sid not in url:
    #         url_list.append(url)
    #         # for sid in miss_sid_list:
    #         #     if str(sid) in url:
    #         #         url_list.append(url)
    #         #         print(url)
    #
    #     r.rpush('che300_price_daily:start_urls', *url_list)
        # print(len(list(set(url_list))))
        # r.lpush('che300_price_daily:start_urls', *url_list)


    # collection2.insert_many(df_a_filter.to_dict('records'))
