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

# redis_url = 'redis://192.168.1.249:6379/15'
pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=14)
con = redis.Redis(connection_pool=pool)
r = con.client()

connection = pymongo.MongoClient('192.168.1.92', 27017)
db = connection["dasouche"]
collection_city = db["dasouche_city"]
collection_modellist = db["dasouche_modellist"]

model_city = collection_city.find({}, {"cityName": 1, "cityId": 1, "_id": 0})
car_city_list = list(model_city)
city_dic = {data["cityName"]: data["cityId"] for data in car_city_list}
print(city_dic)
model_data = collection_modellist.find({}, {"brandName": 1, "modelCode": 1, "year": 1, "_id": 0})
car_msg_df = DataFrame(list(model_data)).drop_duplicates('modelCode')
num = car_msg_df.drop_duplicates('modelCode')['modelCode'].count()
print(num)

for index, car in car_msg_df.iterrows():
    url_list = list()
    month_now = datetime.now().month
    year_now = datetime.now().year
    for year in range(car["year"]-1, year_now + 1):
        month = month_now - 1 if year == year_now else month_now
        for city_n, city_i in city_dic.items():
            registerDate = str(year) + "-" + str(month)
            mile = 0.1 if year == year_now else (2 * (year_now - year))
            meta = {
                "model": car["modelCode"],
                "registerDate": registerDate,
                "city_n": city_n,
                "city_i": city_i,
                "mile": mile
            }
            url = f"https://aolai.souche.com//v2/evaluateApi/getEvaluateInfo.json?modelCode={meta['model']}&regDate={meta['registerDate']}&mile={meta['mile']}&cityName={meta['city_n']}&cityCode={meta['city_i']}"
            url_list.append(url)
            print(url)
    r.lpush('dasouche_price:start_urls', *url_list)


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
