__author__ = 'cagey'

import pymongo
import pymysql
import time
import redis
from datetime import datetime
from dateutil import rrule
from random import shuffle
import pandas as pd
from redis import Redis

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

# sql = "select cityid, provid from che300_need_city_200"
# df_data = readMysqlaly(sql)
# city_list = df_data["cityid"].to_list()
# prov_list = df_data["provid"].to_list()
# city_dic = dict(zip(city_list, prov_list))
# print(city_dic)
city_dic = {'3': '3'}

# brand_list = ["大众", "斯柯达", "丰田", "吉利", "荣威", "日产", "本田" "别克", "雪佛兰"]
redis_url = 'redis://192.168.2.149:6379/15'
pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()
r.lpush('che300_price_daily_200_city:start_urls', url)

connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["usedcar_evaluation"]
collection = db["che300_app_modelinfo2_20200410"]
model_data = collection.find({}, {"brand_name": 1, "sid": 1, "bid": 1, "id": 1, "min_reg_year": 1, "max_reg_year": 1, "_id": 0})

car_msg_list = list(model_data)
# shuffle(car_msg_list)

connection2 = pymongo.MongoClient('192.168.1.92', 27017)
db2 = connection2["che300"]
collection2 = db2["che300_sh_url"]
data_list = []


start_url = "https://m.che300.com/partner/result.php?prov={}&city={}&brand={}&series={}&model={}&registerDate={}&mileAge={}&intention=0&partnerId=wechat_01&unit=1&sld=sh"
month_now = datetime.now().month
year_now = datetime.now().year
now_date = str(year_now) + "-" + str(month_now)
start_date = datetime.strptime(now_date, '%Y-%m')

for car in car_msg_list:
    for year in range(int(car["min_reg_year"]), int(car["max_reg_year"]) + 1):
        month_list = [1, 5] if year == year_now else [1, 12]
        # for city, prov in city_dic.items():
        for month in month_list:
            registerDate = str(year) + "-" + str(month)
            end_date = datetime.strptime(registerDate, '%Y-%m')
            car_age = rrule.rrule(rrule.MONTHLY, dtstart=end_date, until=start_date).count()
            mile = 0.1 if car_age == 0 else int(round(float((2/12 * car_age)), 0))
            meta = {
                "brand": car["bid"],
                "series": car["sid"],
                "model": car["id"],
                "registerDate": registerDate,
                "city": '3',
                "prov": '3',
                "mile": mile
            }
            url = start_url.format(meta["prov"], meta["city"], car["bid"], car["sid"], car["id"], registerDate,meta["mile"])
            # r.lpush('che300_price_daily:start_urls', url)
            # r.lpush('che300_price_daily_200_city:start_urls', url)
            # data = {"url": url}
            # data_list.append(data)
            # print(url)
# collection2.insert(data_list)
