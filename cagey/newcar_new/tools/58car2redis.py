__author__ = 'cagey'

import pymongo
import redis
import time

settings = {
    'MONGODB_PORT': 27017,
    'MONGODB_SERVER': '192.168.1.94',
    'MONGODB_DB': 'newcar_price',
    'MONGODB_COLLECTION': '58car_price',

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


pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
c = con.client()

c.delete('autohome_price_new:dupefilter')
# c.lpush('autohome_price:start_urls', *city_list)


# p = c.lpop('autohome_gz:start_urls')
# p = bytes.decode(p)
# print(p)
# con.close()




