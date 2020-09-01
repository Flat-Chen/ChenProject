__author__ = 'cagey'

import pymongo
import pymysql
import redis
from datetime import datetime
from dateutil import rrule
from pandas.core.frame import DataFrame

pool = redis.ConnectionPool(host='192.168.1.249', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()


connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["che300"]
collection = db["che300_split"]
# collection1 = db["che300_split_new"]
# collection2 = db["che300_price_daily_40_city"]
# model_data = collection.find({},)
# model_data = collection.find({"grabtime": {'$regex': '2020-04-08'}})
# car_msg_list = list(model_data)
# print(len(car_msg_list))
# for car in car_msg_list:
#    collection.insert(dict(car))
#    print(car["url"])
# collection.insert(car_msg_list)

# db1 = connection["che300"]
# collection1 = db1["che300_price_daily_40_city_have_url"]
# model_data = collection.find({}, {"url": 1, "_id": 0})
# car_msg_df = DataFrame(list(model_data))
# # print(car_msg_df)
# car_msg_df_new = car_msg_df[car_msg_df["min_reg_year"].notnull()]
# print(car_msg_df_new)
# collection1.insert_many(car_msg_df_new.to_dict('records'))
# url_list = car_msg_df['url'].values
# url = 'https://m.che300.com/partner/result.php?prov=8&city=8&brand=634&series=36416&model=1360065&registerDate=2019-4&mileAge=2&intention=0&partnerId=wechat_01&unit=1&sld=sh'

# for url in url_list:
#     print(url)
#     r.lpush('che300_price_daily_40_city:start_urls', url)
#
# registerDate = '2016-12'
# now_date = '2020-04'
# a = datetime.strptime(registerDate, '%Y-%m')
# b = datetime.strptime(now_date, '%Y-%m')
# months = rrule.rrule(rrule.MONTHLY, dtstart=a, until=b).count()
# print(months)
