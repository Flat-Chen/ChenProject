__author__ = 'cagey'
import time
import random
import logging
import pandas as pd
from pymysql import connect

from redis import Redis
import redis
from sqlalchemy import create_engine

pool = redis.ConnectionPool(host='192.168.1.249', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
c = con.client()
website = 'che300_big_car_evaluate'
engine = create_engine(f'mysql+pymysql://{"root"}:{"Datauser@2017"}@{"192.168.1.94"}:{3306}/{"truck"}?charset=utf8')


def get_city_prive():
    engine_city = create_engine('mysql+pymysql://baogang:Baogang@2019@192.168.2.120:3306/peoplez?charset=utf8')
    city = pd.read_sql("select cityid,provid from che300_city where provincial_capital=1 ", con=engine_city)
    return city.values.tolist()

def change_table_name():
    # alter table 旧表名 rename 新表名
    # 先判断 新表是否存在 然后在修改
    con = connect(host='192.168.1.94', port=3306, user='root', password='Datauser@2017', database='truck',
                  charset='utf8')
    table_time = time.strftime("%Y_%m", time.localtime())
    cs1 = con.cursor()
    index = cs1.execute("show tables like 'che300_big_car_evaluate_all_city_online_{}'".format(table_time))
    if int(index) == 1:
        logging.log(msg='表名已经存在 不需要修改-----------------------------------------------------', level=logging.INFO)
        cs1.close()
        con.close()
    else:
        sql = "alter table che300_big_car_evaluate_all_city_online rename  to che300_big_car_evaluate_all_city_online_{}".format(
            table_time)
        try:
            cs1.execute(sql)
        except:
            logging.log(msg='表名不存在-----------------------------------------------------', level=logging.INFO)
        else:
            logging.log(msg='修改表名成功----------------------------------------------------------------',
                        level=logging.INFO)
        cs1.close()
        con.close()


def push_url(city_list):
    car_data = pd.read_sql("SELECT brand_id,series_id,model_id ,min_year,max_year,type from che300_big_car_online LIMIT 0,1000", con=engine)
    max_year = int(time.strftime("%Y", time.localtime()))
    car_list = car_data.drop_duplicates('model_id').values.tolist()
    # random.shuffle(car_list)
    for i in car_list:
        for city in city_list:
            for year in range(int(max_year) + 1)[int(i[3]):]:
                mile = (max_year - year) * 2
                if year == max_year:
                    mile = 0.1
                reg_date = str(year) + time.strftime("-%m", time.localtime())
                meta = {
                    "brand_id": i[0],
                    "series_id": i[1],
                    "model_id": i[2],
                    "prov_id": city[1],
                    "city_id": int(city[0]),
                    "mile": mile,
                    "reg_date": reg_date
                }
                url = "https://open.che300.com/api/cv/evaluate?brand_id={}&series_id={}&model_id={}&prov_id={}&city_id={}&reg_date={}&mile={}".format(
                        meta["brand_id"], meta["series_id"], meta["model_id"], meta["prov_id"], meta["city_id"],
                        meta["reg_date"], meta["mile"])
                c.lpush('che300_big_car_evaluate_all_city:start_urls', url)
                print(url)


if __name__ == '__main__':
    city_list = get_city_prive()
    change_table_name()
    push_url(city_list)
