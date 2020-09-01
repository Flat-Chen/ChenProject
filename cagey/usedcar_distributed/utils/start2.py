# -*- coding:utf-8 -*-
import os
import redis

redis_client = redis.Redis(host='192.168.84.129', port=6379, db=0)
websites =  [
    {'website': 'che58', 'start_url': 'http://www.58.com/ershouche/changecity/'},
]

def start(website):
    redis_client.lpush(website['website'], website['start_url'])
    os.system('nohup scrapy crawl {} > log/{}.log 2>&1 &'.format(website['website'], website['website']))

if __name__ == "__main__":
    for website in websites:
        start(website)