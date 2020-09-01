__author__ = 'cagey'

import re
import pymysql
from redis import Redis

redis_url = 'redis://192.168.2.149:6379/15'
r = Redis.from_url(redis_url, decode_responses=True)

def structure_http(result):
    # "(2, 'price22.1863101943prov3city3mile0.1model11805year2006month6typedealer_price', 'D46B1542376EE8F1')"
    # "https://dingjia.che300.com/demo/evaluate/getPriceTrendSign?mile=3&sign=5061D26526E610B6&city=3&prov=3&year=2018&month=1&price=33.2503327331714&app_type=android_price&type=dealer_price&model=1146056"
    price = re.search(r"price(.*?)prov", result[1]).group(1)
    sign = result[2]
    mile = re.search(r'mile(.*?)mode', result[1]).group(1)
    city = re.search(r'city(.*?)mile', result[1]).group(1)
    prov = re.search(r'prov(.*?)city', result[1]).group(1)
    year = re.search(r'year(.*?)month', result[1]).group(1)
    month = re.search(r'month(.*?)type', result[1]).group(1)
    model = re.search(r'model(.*?)year', result[1]).group(1)
    # print(price, sign, mile, city, prov, year, month, model)

    meta = dict()
    meta['provid'] = prov
    meta['cityid'] = city
    meta['salesdescid'] = model
    meta['regDate'] = str(year) + "-" + str(month)
    meta['mile'] = mile

    http = "https://dingjia.che300.com/demo/evaluate/getPriceTrendSign?mile={}&sign={}&city={}&prov={}&year={}&month={}&price={}&app_type=android_price&type=dealer_price&model={}" \
        .format(mile, sign, city, prov, year, month, price, model)
    return (http, meta)

dbconn = pymysql.connect(host="192.168.1.94", database='for_android', user="dataUser94", password="94dataUser@2020", port=3306,
                         charset='utf8')
dbc = dbconn.cursor()
count = dbc.execute('select * from che300_trend')
print("一共%d条" % count)
result = dbc.fetchall()
for i in list(result):
    # i = (5, 'price95.1390656201prov3city3mile0.1model1129007year2017month6typedealer_price', '265BB6E86712C4BB')
    url, meta = structure_http(i)
    r.lpush('che300_futureprice:start_urls', url)
    # r.lpush('che300_futureprice:requests', url)
    print(url)
# r.llen('che300_futureprice:start_urls')