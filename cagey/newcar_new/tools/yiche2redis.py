__author__ = 'cagey'

import pymongo
import redis
import pathlib
import os
import time
import json

with open('./yiche.json', 'r') as f:
    data = f.read()
brand_dic = json.loads(data)


settings = {
    # 'MONGODB_USER': 'admin',
    # 'MONGODB_PWD': 'ABCabc123',
    'MONGODB_PORT': 27017,
    'MONGODB_SERVER': '192.168.1.94',
    'MONGODB_DB': 'newcar_price',
    'MONGODB_COLLECTION': 'yiche_price',

}

local_time = time.strftime('%Y-%m-%d', time.localtime())
connection = pymongo.MongoClient(
    settings['MONGODB_SERVER'],
    settings['MONGODB_PORT']
)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]

count = collection.count()
name = settings['MONGODB_COLLECTION'] + '_' + str(local_time)
if count:
    print(count)
    collection.rename(name)

brand_list = []
for k, v in brand_dic.items():
    url = f"http://car.bitauto.com/{k}/baojia/c0/"
    brand_list.append(url)

pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
c = con.client()
c.lpush('yiche_price:start_urls', *brand_list)

# p = c.lpop('autohome_gz:start_urls')
# p = bytes.decode(p)
# print(p)
# con.close()




