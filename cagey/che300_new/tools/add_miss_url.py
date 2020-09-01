__author__ = 'cagey'

import pandas as pd
import pymongo
import redis
from datetime import datetime
from pandas.core.frame import DataFrame

settings = {
    "MYSQL_USER": "dataUser94",
    "MYSQL_PWD": "94dataUser@2020",
    "MYSQL_SERVER": "192.168.1.94",
    "MYSQL_PORT": "3306",
    "MYSQL_DB": "jzg",
    "MYSQL_TABLE": "content_senti",
    "MONGODB_SERVER": "192.168.2.149",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "che300",
    "MONGODB_COLLECTION": "che300_price_daily_all_city",
    "MONGODB_USER": "admin",
    "MONGODB_PWD": "ABCabc123"
}
pd.set_option('display.max_columns', None)

# redis_url = 'redis://192.168.1.241:6379/15'
pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()

uri1 = f'mongodb://192.168.2.149:{settings["MONGODB_PORT"]}/'
connection = pymongo.MongoClient(uri1)
db = connection['che300']
collection = db['che300_price_daily_all_city']

uri2 = f'mongodb://192.168.1.92:{settings["MONGODB_PORT"]}/'
connection2 = pymongo.MongoClient(uri2)
db2 = connection2[settings['MONGODB_DB']]
collection2 = db2['che300_price_daily_all_city_url']

model_data = collection.find({}, {"url": 1, "_id": 0})
car_msg_df = DataFrame(list(model_data)).drop_duplicates('url')
have_num = car_msg_df["url"].count()
print(have_num)

model_data2 = collection2.find({}, {"url": 1, "_id": 0})
car_msg_df2 = DataFrame(list(model_data2)).drop_duplicates('url')
all_num = car_msg_df2["url"].count()
print(all_num)

df_a_filter = car_msg_df2[~ car_msg_df2['url'].isin(car_msg_df['url'])]
miss_num = df_a_filter["url"].count()
print(miss_num)

lens = r.llen("che300_price_daily_all_city:start_urls")
print(lens)

# sale_url = f"https://qd.jingzhengu.com/appraise-s{meta['model']}-r{meta['registerDate']}-m{meta['mile']}-c{meta['city']}-ugongzh-m2.html"
# sale_url = f"http://m.jingzhengu.com/sale-s{meta['model']}-r{meta['registerDate']}-m{meta['mile']}-c{meta['city']}-y-j-h"

url_list = []
if lens == 0 and miss_num > 0:
    for url in df_a_filter.values:
        url = url[0]
        # print(url)
        url_list.append(url)
    r.lpush('che300_price_daily_all_city:start_urls', *url_list)

# df_a_filter = car_msg_df2[~ car_msg_df2['url'].isin(car_msg_df['url'])]
# miss_num = df_a_filter["url"].count()
# print(miss_num)
# collection2.insert_many(df_a_filter.to_dict('records'))
