# -*- coding:utf-8 -*-
import redis
# redis_client = redis.Redis('192.168.84.129', port=6379, db=1)
redis_client = redis.Redis('192.168.1.247', port=6379, db=1)

with open("brand.txt") as f:
    brand = f.read()
    brand_list = brand.split("\n")

with open("city.txt") as f:
    city = f.read()
    city_list = city.split("\n")

# mileage
miles = ['sn_k0-8', 'sn_k8-']

# price
prices = ['p0-3', 'p3-5', 'p5-8', 'p8-10', 'p10-15', 'p15-20', 'p20-30', 'p30-50', 'p50-']

for brand in brand_list:
    if brand != "":
        for city in city_list:
            if city != "":
                for mile in miles:
                    for price in prices:
                        # 'https://www.xin.com/shenzhen/dazhong/sn_k8-p50-/
                        temp = mile + price
                        url = "https://www.xin.com/%s/%s/%s/" % (city, brand, temp)
                        redis_client.lpush('youxin', url)