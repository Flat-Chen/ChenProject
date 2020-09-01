__author__ = 'cagey'
import pymysql
import pandas as pd
from sqlalchemy import create_engine
settings = {
        'MYSQL_USER': 'baogang',
        'MYSQL_PWD': 'Baogang@2019',
        'MYSQL_SERVER': '192.168.2.120',
        'MYSQL_PORT': 3306,
        'MYSQL_DB': 'baogang'
}


conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
sql_jj = "truncate table ouyeel_jj_new_tmp"
sql_gp = "truncate table ouyeel_new_tmp"
pd.set_option('display.max_columns', None)
conn.connect().execute(sql_jj)
conn.connect().execute(sql_gp)











