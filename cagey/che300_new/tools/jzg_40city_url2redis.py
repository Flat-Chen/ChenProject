__author__ = 'cagey'

import pymongo
import pymysql
import time
import redis
from datetime import datetime
import pandas as pd
from redis import Redis
from pandas.core.frame import DataFrame

settings = {
    "MYSQL_USER": "dataUser94",
    "MYSQL_PWD": "94dataUser@2020",
    "MYSQL_SERVER": "192.168.1.94",
    "MYSQL_PORT": "3306",
    "MYSQL_DB": "saicnqms",
    "MYSQL_TABLE": "content_senti",
}
def readMysqlaly(sql):
    dbconn = pymysql.connect(
        host="192.168.1.94",
        database='people_zb',
        user="dataUser94",
        password="94dataUser@2020",
        port=3306,
        charset='utf8')
    sqlcmd = sql
    df = pd.read_sql(sqlcmd, dbconn)
    return df

sql = "select areaId from jzg_40_city"
df_data = readMysqlaly(sql)
city_list = df_data["areaId"].values
print(city_list)

# brand_list = ["大众", "斯柯达", "丰田", "吉利", "荣威", "日产", "本田" "别克", "雪佛兰"]
redis_url = 'redis://192.168.1.241:6379/15'
pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()

connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["jzg"]
collection = db["jzg_split"]
model_data = collection.find({}, {"brandname": 1, "brandid": 1, "familyid": 1, "salesdescid": 1, "min_reg_year": 1,
                                  "max_reg_year": 1, "part": 1, "_id": 0})

# 获取要跑那块数据
data_f = '2020-05-02'
data_0 = '2020-05-29'
date1 = time.strptime(data_0, '%Y-%m-%d')
now_d = time.strftime('%Y-%m-%d', time.localtime())
date2 = time.strptime(now_d, '%Y-%m-%d')
start_d = datetime(date1[0], date1[1], date1[2])
end_d = datetime(date2[0], date2[1], date2[2])
part_num = (end_d - start_d).days % 28

month_now = datetime.now().month
year_now = datetime.now().year
day_now = datetime.now().day + 1
# week_now = datetime.now().weekday()+2
now_date = str(year_now) + "-" + str(month_now)
start_date = datetime.strptime(now_date, '%Y-%m')

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)

# # 挑选当天的数据id
car_msg_df_new = car_msg_df[car_msg_df["part"] == part_num + 1]
car_msg_df_new = car_msg_df_new.drop_duplicates('salesdescid')
print(car_msg_df_new["salesdescid"].count())

# 更改表名字
local_time = time.strftime('%Y-%m-%d', time.localtime())
connection2 = pymongo.MongoClient('192.168.2.149', 27017)
db2 = connection2['jzg']
collection2 = db2['jzg_40city']
count = collection2.count()
if count:
    print(count)
    name = 'jzg_40city_' + str(part_num) + '_' + str(local_time)
    collection2.rename(name)


for index, car in car_msg_df_new.iterrows():
    url_list = []
    for year in range(int(car["min_reg_year"]), int(car["max_reg_year"]) + 1):
        month = month_now - 1 if year == year_now else month_now
        for city in city_list:
            registerDate = str(year) + "-" + str(month) + "-1"
            mile = 1000 if year == year_now else (20000 * (year_now - year))
            meta = {
                # "brand": car["brandid"],
                # "series": car["familyid"],
                "model": car["salesdescid"],
                "registerDate": registerDate,
                "city": city,
                "mile": mile
            }
            sale_url = f"https://qd.jingzhengu.com/appraise-s{meta['model']}-r{meta['registerDate']}-m{meta['mile']}-c{meta['city']}-ugongzh-m2.html"
            # sale_url = f"http://m.jingzhengu.com/sale-s{meta['model']}-r{meta['registerDate']}-m{meta['mile']}-c{meta['city']}-y-j-h"
            buy_url = f"http://m.jingzhengu.com/buy-s{meta['model']}-r{meta['registerDate']}-m{meta['mile']}-c{meta['city']}-y-j-h"
            url_list.append(buy_url)
            url_list.append(sale_url)
            print(sale_url)
    r.lpush('jzg_40city:start_urls', *url_list)
    # r.lpush('jzg_40city:start_urls', buy_url)
#                 data1 = {"url": sale_url}
#                 data2 = {"url": buy_url}
#                 data_list.append(data1)
#                 data_list.append(data2)
#
# collection2.insert(data_list)
# connection = pymongo.MongoClient('192.168.1.94', 27017)
# db = connection["residual_value"]
# collection = db["jzg_modellist2"]
# model_data = collection.find({}, {"brandname": 1, "modelid": 1, "make_year": 1, "next_year": 1, "_id": 0})
# car_msg = DataFrame(list(model_data))
# print("*"*100)
# data = car_msg["modelid"].count()
# print(data)
#
# data1 = car_msg.drop_duplicates('modelid')['modelid'].count()
# print(data1)
# # print(data["brandname"].values[0])
# # print(data["familyname"].values[0])
#
# df = car_msg.drop_duplicates('modelid')
# for index, rows in df.iterrows():
#     print(rows)
# print(d)















