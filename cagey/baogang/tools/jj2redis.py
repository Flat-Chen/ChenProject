__author__ = 'cagey'

import pymongo
import redis

settings = {
    'MONGODB_USER': 'admin',
    # 'MONGODB_PORT': 1206,
    'MONGODB_PORT': 27017,
    'MONGODB_DB': 'baogang',
    'MONGODB_COLLECTION': 'ouyeel_new',
    'MONGODB_PWD': 'ABCabc123',
    # 'MONGODB_SERVER': '180.167.80.118',
    'MONGODB_SERVER': '192.168.1.92',

}

# uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
# connection = pymongo.MongoClient(uri)
connection = pymongo.MongoClient(
    settings['MONGODB_SERVER'],
    settings['MONGODB_PORT']
)
db = connection[settings['MONGODB_DB']]
collection_tmp = db["ouyeel_data_num_bg_tmp"]
data_list = collection_tmp.find({"jj_status": True})
count = 0
url_list = []
for data in data_list:
    # print(data)
    if data["jj_status"]:
        for num in range(1, int(data["jj_page_num"])+1):
            jj_url = f"https://www.ouyeel.com/jk-mobile/search/main-search/?page={num}&shop={data['shop_code']}&salesMethod=20"
            url_list.append(jj_url)
            # print(jj_url)
            count += 1
print(count)
if count:
    # pool = redis.ConnectionPool(host='192.168.1.241', port=6379)
    pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=10)
    # pool = redis.ConnectionPool(host='192.168.1.92', port=6379)
    con = redis.Redis(connection_pool=pool)
    c = con.client()
    c.lpush('ouyeel_jj_bg:start_urls', *url_list)
    con.close()
else:
    print("无竞价资源!")




