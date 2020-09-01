__author__ = 'cagey'

import pymongo
import pymysql
# from datetime import datetime, date
from datetime import datetime
from dateutil import rrule
import time
import redis
import hashlib
import pypinyin
from random import shuffle
import pandas as pd
import time
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

sql = "select che300_cityid, che300_provid, cityname from che300_need_city_light"
df_data = readMysqlaly(sql)
city_list = df_data["che300_cityid"].values
cityname_list = df_data["cityname"].values
prov_list = df_data["che300_provid"].values
city_dic = dict(zip(city_list, prov_list))
cityname_dic = dict(zip(city_list, cityname_list))
# print(city_dic)
# print(cityname_dic)

redis_url = 'redis://192.168.2.149:6379/15'
pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
r = con.client()

r.delete('che300_price_daily:dupefilter')
# r.delete('che300_price_daily:start_urls')
queue_num = r.llen('che300_price_daily:start_urls')
print(r.llen('che300_price_daily:start_urls'))
h = time.strftime('%Y-%m-%d %X', time.localtime()).split(' ')[-1].split(':')[0]
print(h)
#  当队列为空时, push url 进入队列中
if queue_num > 0:
    pass
else:
    connection = pymongo.MongoClient('192.168.1.94', 27017)
    connection2 = pymongo.MongoClient('192.168.2.149', 27017)
    connection4 = pymongo.MongoClient('192.168.1.92', 27017)
    db4 = connection4["che300"]
    collection4 = db4["che300_41city_url"]

    db3 = connection2["che300"]
    collection3 = db3["che300_num"]

    # 当前是几点, 下午18点,清空 队列,停止爬取
    h = time.strftime('%Y-%m-%d %X', time.localtime()).split(' ')[-1].split(':')[0]
    print(h)
    if str(h) in ["18"]:
        print(h)
        # 清空队列
        r.delete('che300_price_daily:dupefilter')
        r.delete('che300_price_daily:start_urls')
        # 重置抓取区块
        collection3.remove()
        data_list = []
        data = {"start_num": 0, "end_num": 100}
        data_list.append(data)
        collection3.insert(data_list)
        # 更改表名字
        local_time = time.strftime('%Y-%m-%d', time.localtime())
        # db = connection2['che300']
        # collection = db['che300_price_daily']
        # count = collection.count()
        # if count:
        #     print(count)
        #     name = 'che300_price_daily' + '_' + str(local_time)
        #     collection.rename(name)

        connection4 = pymongo.MongoClient('192.168.1.92', 27017)
        db4 = connection4["che300"]
        collection4 = db4["che300_41city_url"]
        try:
            collection4.rename("che300_41city_url" + '_' + str(local_time))
        except:
            pass
    else:
        num_data = collection3.find({}, {"start_num": 1, "end_num": 1, "_id": 0})
        num_data_list = list(num_data)[0]
        start_num = num_data_list["start_num"]
        end_num = num_data_list["end_num"]
        print(start_num)
        print(end_num)
        if start_num == 0 or start_num == "0":
            local_time = time.strftime('%Y-%m-%d', time.localtime())
            db = connection2['che300']
            collection = db['che300_price_daily']
            count = collection.count()
            if count:
                print(count)
                name = 'che300_price_daily' + '_' + str(local_time)
                collection.rename(name)
        collection3.remove()
        data_list = []
        # data = {"start_num": 0, "end_num": 100}
        data = {"start_num": end_num, "end_num": end_num + 100}
        data_list.append(data)
        collection3.insert(data_list)

        collection1 = db3["che300_split"]

        model_data1 = collection1.find({}, {"brandname": 1, "brandid": 1, "familyid": 1, "salesdescid": 1, "min_reg_year": 1,
                                          "max_reg_year": 1, "part": 1, "_id": 0})

        car_msg_list1 = list(model_data1)
        car_msg_df = DataFrame(car_msg_list1)
        car_msg_df_new = car_msg_df.drop_duplicates('salesdescid').dropna(axis=0, how='any')
        print(car_msg_df_new["salesdescid"].count())

        db2 = connection2["che300"]
        collection2 = db2["che300_queue"]
        model_data2 = collection2.find({}, {"salesdescid": 1,  "_id": 0})

        # start_num = 0
        # end_num = 500
        car_msg_list2 = list(model_data2)
        sid_list = list()
        for i in car_msg_list2[start_num:end_num]:
            sid_list.append(str(i["salesdescid"]).replace('.0', ''))
        # print(sid_list)

        partnerId = ['douyin', 'escsh', 'yanchebang', 'jhhz', 'ynhcj', 'chexiaopang']

        month_now = datetime.now().month
        day_now = datetime.now().day + 1
        year_now = datetime.now().year
        now_date = str(year_now) + "-" + str(month_now)
        start_date = datetime.strptime(now_date, '%Y-%m')
        today = datetime.today()

        def get_md5_value(src):
            myMd5 = hashlib.md5()
            myMd5.update(src.encode('utf-8'))
            myMd5_Digest = myMd5.hexdigest()
            return myMd5_Digest

        start_url = "https://www.che300.com/partner/result.php?prov={}&city={}&brand={}&series={}&model={}&registerDate={}&mileAge={}&intention=0&partnerId={}&unit=1&sn={}&sld={}"

        # sid_list = [1373449 , 1373450 , 1373451 , 1373452 , 1373455 , 1400873 , 1400874 , 1400875 , 1400876 , 1400877 , 1400878 , 1400879 , 1400880 , 1400976 , 1401127 , 1401128 , 1401129 , 1401130 , 1401131 , 1401134 , 1401137 , 1401138 , 1401141 , 1373453 , 1373454 , 1373456 , 1373457 , 1401132 , 1401133 , 1401139 , 1401140]
        na_sid_list = ["1358532", "1367052", "1369333", "1369334", "1401035", "1210617"]

        count = 0
        url_list = list()
        for index, rows in car_msg_df_new.iterrows():
            car = rows
            # print("*"*100)
            # if int(car["salesdescid"]) in sid_list:
            if car["salesdescid"] in sid_list and car["salesdescid"] not in na_sid_list:
                # url_list = list()
                data_list = list()
                max_reg_year = int(car["max_reg_year"])
                max_reg_year_new = year_now if max_reg_year + 2 > year_now else max_reg_year + 2
                for year in range(int(car["min_reg_year"]), max_reg_year_new + 1):
                    month_list = [1, 12] if month_now == 12 else [1, month_now + 1] if year == year_now else [1, 12]
                    for month in month_list:
                        registerDate = str(year) + "-" + str(month)
                        end_date = datetime.strptime(registerDate, '%Y-%m')
                        car_age = rrule.rrule(rrule.MONTHLY, dtstart=end_date, until=start_date).count()
                        mile = "0.1" if car_age == 0 else str(round((2 / 12 * car_age), 2))
                        mile = mile.replace('.0', '')
                        for city, prov in city_dic.items():
                            meta = {
                                "brand": car["brandid"],
                                "series": car["familyid"],
                                "model": car["salesdescid"],
                                "registerDate": registerDate,
                                "city": city,
                                "prov": prov,
                                "mile": mile
                            }
                            shuffle(partnerId)
                            s = f"brand={meta['brand']}&city={meta['city']}&mileAge={mile}&model={meta['model']}&prov={meta['prov']}&registerDate={registerDate}&series={meta['series']}njB6TTeQvTnGN4To"
                            md = get_md5_value(s)

                            cityname = cityname_dic[city]
                            a = pypinyin.pinyin(cityname, style=pypinyin.FIRST_LETTER)
                            c_pinyin = ''.join([str(a[i][0]) for i in range(len(a))])
                            # print(c_pinyin)

                            url = start_url.format(meta["prov"], meta["city"], rows["brandid"], rows["familyid"], rows["salesdescid"], registerDate, mile, partnerId[0], md, c_pinyin)
                            url_list.append(url)
                            data = {"url": url}
                            data_list.append(data)
                            # print(url)
                            count += 1

                print(count)
                collection4.insert(data_list)
        shuffle(url_list)
        r.rpush('che300_price_daily:start_urls', *list(set(url_list)))
                # print(len(data_list))



        # r.rename('che300_price_daily_40_city:start_urls', 'che300_price_daily_old:start_urls',)
        # r.rename('che300_price_daily:start_urls', 'che300_price_daily_40_city:start_urls',)

        # month_len = (int(car["max_reg_year"])-int(car["min_reg_year"]))*12+int(month_now)
        # registerDate_list = [getTheMonth(today, i) for i in range(0, month_len, 3)]
        # mile_list = [round(i*(2/12), 2) for i in range(0, month_len, 3)]
        # data_dic = dict(zip(registerDate_list, mile_list))
        # for year, mile in data_dic.items():

        # def getTheMonth(date, n):
        #     month = date.month
        #     year = date.year
        #     for i in range(n):
        #         if month == 1:
        #             year -= 1
        #             month = 12
        #         else:
        #             month -= 1
        #     return datetime.date(year, month, 1).strftime('%Y-%m')


        # if year == year_now:
        #     if month_now == 1:
        #         month_list = [1, 2]
        #     elif month_now == 12:
        #         month_list = [1, 12]
        #     else:
        #         month_list = [1, month_now + 1]
        #         # month_list.append(int(1 + month_now + 1)/2)
        # else:
        #     month_list = [1, 12]
        # print("*" * 100)
        # if month_now in month_list:
        #     month_list = month_list[:month_list.index(month_now) + 1]
        # else:
        #     for m in month_list:
        #         if month_now < m and m in month_list:
        #             month_list = month_list[:month_list.index(m)]
        # if month_now + 1 not in month_list:
        #     month_list.append(month_now + 1)
        # if month_now - 1 not in month_list:
        #     month_list.append(month_now - 1)
        # 获取要跑那块数据
        # data_0 = '2020-05-06'
        # date1 = time.strptime(data_0, '%Y-%m-%d')
        # now_d = time.strftime('%Y-%m-%d', time.localtime())
        # date2 = time.strptime(now_d, '%Y-%m-%d')
        # start_d = datetime(date1[0], date1[1], date1[2])
        # end_d = datetime(date2[0], date2[1], date2[2])
        # part_num = (end_d - start_d).days % 28

        #
        # # car_msg_df_new = car_msg_df[car_msg_df["part"] == part_num + 1]
        # # car_msg_df_new = car_msg_df_new.drop_duplicates('salesdescid')
        # # print(car_msg_df_new["salesdescid"].count())
