# -*- coding:utf-8 -*-
import redis

provinces = ['/ah/buycar/', '/bj/buycar/', '/cq/buycar/', '/fj/buycar/', '/gd/buycar/', '/gx/buycar/',
                     '/guizhou/buycar/', '/gs/buycar/', '/hb/buycar/', '/hlj/buycar/', '/hn/buycar/', '/hubei/buycar/',
                     '/hunan/buycar/', '/hainan/buycar/', '/jl/buycar/', '/js/buycar/', '/jx/buycar/', '/ln/buycar/',
                     '/nmg/buycar/', '/nx/buycar/', '/qh/buycar/', '/shanxi/buycar/', '/sh/buycar/', '/sd/buycar/',
                     '/sc/buycar/', '/sx/buycar/', '/tj/buycar/', '/xz/buycar/', '/xj/buycar/', '/yn/buycar/', '/zj/buycar/']

# redis_client = redis.Redis('192.168.84.129', port=6379, db=1)
redis_client = redis.Redis('192.168.1.247', port=6379, db=1)
for province in provinces:
    url = 'http://2sc.sohu.com' + province
    redis_client.lpush('souhu', url)