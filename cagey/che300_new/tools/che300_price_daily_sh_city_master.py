__author__ = 'cagey'

import pymongo
import pymysql
import time
import redis
from datetime import datetime, timedelta, date
from dateutil import rrule
from random import shuffle
import pandas as pd
from redis import Redis
from pandas.core.frame import DataFrame
import hashlib

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

def getYesterday():
    today = date.today()
    oneday = timedelta(days=1)
    yesterday = today-oneday
    return str(yesterday)

city_dic = {'3': '3'}

redis_url = 'redis://192.168.2.149:6379/15'
pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()

r.delete('che300_price_daily_all_city:dupefilter')
r.delete('che300_price_daily_all_city:start_urls')

connection = pymongo.MongoClient('192.168.2.149', 27017)
db = connection["che300"]
collection = db["che300_split"]
model_data = collection.find({}, {"brandname": 1, "brandid": 1, "familyid": 1, "salesdescid": 1, "min_reg_year": 1, "max_reg_year": 1, "part": 1, "_id": 0})

car_msg_list = list(model_data)
# print(car_msg_list)
car_msg_df = DataFrame(car_msg_list)
# car_msg_df = car_msg_df.drop_duplicates('salesdescid')
# print(car_msg_df["salesdescid"].count())


partnerId = ['douyin', 'wechat_01', 'escsh', 'yanchebang', 'cheniu', 'jhhz', 'ynhcj', 'chexiaopang']
# miss_partnerId = ["yanchebang"]
# 变量
# start_url = "http://www.che300.com/partner/result.php?prov={}&city={}&brand={}&series={}&model={}&registerDate={}&mileAge={}&intention=0&unit=1&sld=sh&partnerId=wechat_01"
start_url = "https://www.che300.com/partner/result.php?prov={}&city={}&brand={}&series={}&model={}&registerDate={}&mileAge={}&intention=0&partnerId={}&unit=1&sn={}&sld=sh"

month_now = datetime.now().month
year_now = datetime.now().year
day_now = datetime.now().day + 1
# week_now = datetime.now().weekday()+2
now_date = str(year_now) + "-" + str(month_now)
start_date = datetime.strptime(now_date, '%Y-%m')

# 获取要跑那块数据
data_f = '2020-05-02'
data_0 = '2020-06-04'
date1 = time.strptime(data_0, '%Y-%m-%d')
now_d = time.strftime('%Y-%m-%d', time.localtime())
date2 = time.strptime(now_d, '%Y-%m-%d')
start_d = datetime(date1[0], date1[1], date1[2])
end_d = datetime(date2[0], date2[1], date2[2])
part_num = (end_d - start_d).days % 28
# part_num = 28 if part_num == 0 else part_num

print(part_num+1)
# part_num = 20
# miss_num_list = []
# part_num = 7

# # 挑选当天的数据id
car_msg_df_new = car_msg_df[car_msg_df["part"] == part_num+1]
car_msg_df_new = car_msg_df_new.drop_duplicates('salesdescid')
print(car_msg_df_new["salesdescid"].count())
print(car_msg_df_new["salesdescid"])
#
#

# 更改表名字
connection2 = pymongo.MongoClient('192.168.2.149', 27017)
local_time = time.strftime('%Y-%m-%d', time.localtime())
print(local_time)
db2 = connection2['che300']
collection2 = db2['che300_price_daily_all_city']

count = collection2.count()
if count:
    print(count)
    name = 'che300_price_daily_all_city_' + str(part_num) + '_' + str(getYesterday())
    collection2.rename(name)

connection3 = pymongo.MongoClient('192.168.1.92', 27017)
db3 = connection3["che300"]
collection3 = db3["che300_price_daily_all_city_url"]
try:
    collection3.rename("che300_price_daily_all_city_url" + "_" + str(part_num) + '_' + str(getYesterday()))
except:
    pass


# def get_md5_value(src):
#     myMd5 = hashlib.md5()
#     myMd5.update(src.encode('utf-8'))
#     myMd5_Digest = myMd5.hexdigest()
#     return myMd5_Digest

# url_list = []
count = 0
other_url_list = []
data_list = []
for index, rows in car_msg_df_new.iterrows():
    max_reg_year = int(rows["max_reg_year"])
    max_reg_year_new = year_now if max_reg_year + 5 > year_now else max_reg_year + 5
    for year in range(int(rows["min_reg_year"]), max_reg_year_new + 1):
        month_list = [i for i in range(1, month_now + 2)] if year == year_now else [i for i in range(1, 13)]
        for month in month_list:
            registerDate = str(year) + "-" + str(month)
            end_date = datetime.strptime(registerDate, '%Y-%m')
            car_age = rrule.rrule(rrule.MONTHLY, dtstart=end_date, until=start_date).count()
            mile = 0.1 if car_age == 0 else round((2 / 12 * car_age), 2)
            meta = {
                "brand": rows["brandid"],
                "series": rows["familyid"],
                "model": rows["salesdescid"],
                "registerDate": registerDate,
                "city": '3',
                "prov": '3',
                "mile": mile
            }
            # shuffle(partnerId)
            # s = f"brand={meta['brand']}&city=3&mileAge={mile}&model={meta['model']}&prov=3&registerDate={registerDate}&series={meta['series']}njB6TTeQvTnGN4To"
            # md = get_md5_value(s)
            # url = start_url.format(meta["prov"], meta["city"], rows["brandid"], rows["familyid"], rows["salesdescid"], registerDate, meta["mile"], partnerId[0], md)
            # url_list.append(url)
            # print(url)

            other_city_url = f'https://dingjia.che300.com/app/EvalResult/allProvPrices?callback=jQuery18309705734921018707_1534391096144&brand={rows["brandid"]}&series={rows["familyid"]}&model={rows["salesdescid"]}&regDate={registerDate}&mile={meta["mile"]}'
            other_url_list.append(other_city_url)

            data = {"url": other_city_url}
            data_list.append(data)
            # print(other_city_url)
shuffle(other_url_list)
r.lpush('che300_price_daily_all_city:start_urls', *other_url_list)
print(len(data_list))
collection3.insert(data_list)

