__author__ = 'cagey'
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
sql_jj = "select * from ouyeel_jj_new_tmp"
sql_gp = "select * from ouyeel_new_tmp"
pd.set_option('display.max_columns', None)
df_jj = pd.read_sql_query(sql_jj, conn)
df_gp = pd.read_sql_query(sql_gp, conn)

local_settings = {
        'MYSQL_USER': 'dataUser94',
        'MYSQL_PWD': 'Baogang@2019',
        'MYSQL_SERVER': '127.0.0.1',
        'MYSQL_PORT': 3306,
        'MYSQL_DB': 'baogang'
}

local_conn = create_engine(f'mysql+pymysql://{local_settings["MYSQL_USER"]}:{local_settings["MYSQL_PWD"]}@{local_settings["MYSQL_SERVER"]}:{local_settings["MYSQL_PORT"]}/{local_settings["MYSQL_DB"]}?')
df_jj.to_sql(name='ouyeel_jj', con=local_conn, if_exists="append", index=False)
df_gp.to_sql(name='ouyeel_gp', con=local_conn, if_exists="append", index=False)

sql1 = "truncate table ouyeel_jj"
sql2 = "truncate table ouyeel_gp"
conn.connect().execute(sql1)
conn.connect().execute(sql2)




