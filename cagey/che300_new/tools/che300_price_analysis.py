__author__ = 'cagey'

import pymongo
import pymysql
from datetime import datetime
from dateutil import rrule
import time
import redis
import hashlib
import pypinyin
from random import shuffle
import pandas as pd
import time
from pandas.core.frame import DataFrame


connection1 = pymongo.MongoClient('192.168.2.149', 27017)
connection2 = pymongo.MongoClient('192.168.1.92', 27017)
db1 = connection1["che300"]

collection1 = db1["che300_queue"]
collection2 = db1["che300_price_daily"]
collection3 = db1["che300_price_daily_all_city_26_2020-06-01"]

model_data1 = collection1.find({}, {"i": 1, "salesdescid": 1, "_id": 0})
model_data2 = collection2.find({}, {"salesdescid": 1, "price1": 1,  "price2": 1,  "price3": 1,  "price4": 1,  "price5": 1,  "price6": 1,  "price7": 1,  "cityid": 1,   "regDate": 1,   "mile": 1, "_id": 0})
model_data3 = collection3.find({}, {"salesdescid": 1, "prices": 1,  "regDate": 1,   "mile": 1, "_id": 0})

# car_msg_list1 = list(model_data1)[5:500]
# car_msg_df1 = DataFrame(car_msg_list1)
# car_msg_df_new1 = car_msg_df1.drop_duplicates('salesdescid').dropna(axis=0, how='any')
# sid_list = [str(sid).replace('.0', '') for sid in car_msg_df_new1["salesdescid"].values]
# print(sid_list)

car_msg_list3 = list(model_data3)
car_msg_df3 = DataFrame(car_msg_list3)
sid_list = [str(sid).replace('.0', '') for sid in car_msg_df3.drop_duplicates('salesdescid')["salesdescid"].values]
print(len(sid_list))

car_msg_list2 = list(model_data2)
car_msg_df2 = DataFrame(car_msg_list2)
car_msg_df_new2 = car_msg_df2[car_msg_df2['salesdescid'].isin(sid_list)]
sid_list2 = [str(sid).replace('.0', '') for sid in car_msg_df_new2.drop_duplicates('salesdescid')["salesdescid"].values]
print(car_msg_df_new2["salesdescid"].count())
print(len(sid_list2))

msg_df_new2 = car_msg_df2[car_msg_df2['salesdescid'].isin(sid_list2)]
msg_df_new3 = car_msg_df3[car_msg_df3['salesdescid'].isin(sid_list2)]

print(msg_df_new2[msg_df_new2["cityid"]==5])
print(msg_df_new2["cityid"])
print(msg_df_new3["salesdescid"].count())

# car_msg_new = pd.merge(msg_df_new2, msg_df_new3, how='inner', on=["regDate", "mile"],)
# car_msg_new = car_msg_new.dropna(axis=0, how='any')
# print(car_msg_new["salesdescid"].count())















