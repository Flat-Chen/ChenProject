# -*- coding:utf-8 -*-
import redis

# REDIS_SERVER = '192.168.84.129'
# REDIS_DB = 0

REDIS_SERVER = '192.168.1.247'
REDIS_DB = 0

redis_client = redis.Redis(REDIS_SERVER, port=6379, db=REDIS_DB)
redis_client2 = redis.Redis(REDIS_SERVER, port=6379, db=1)


# redis_client.lpush('che58', "http://www.58.com/ershouche/changecity/")
# redis_client.lpush('che273', "http://www.273.cn/car/city.html")
# redis_client.lpush('aokangda', "http://www.akd.cn/carlist/o9/")
# redis_client.lpush('auto51', "http://m.51auto.com/quanguo/pabmdcigf")
# redis_client.lpush('che101', "http://www.che101.com/buycar/")
# redis_client.lpush('che168', "http://m.che168.com/carlist/FilterBrand.aspx")
# chemao_start_urls = redis_client2.lrange('chemao', 0, -1)
# print(chemao_start_urls)
# redis_client.lpush('chemao', *chemao_start_urls)
# redis_client.lpush('carsupai', "https://www.chesupai.cn/list/sh/")
# redis_client.lpush('chewang', "http://www.carking001.com/ershouche")
# redis_client.lpush('chezhibao', "https://search.chezhibao.com/auctionHistory/list.htm?page=1&brand=0&mode=0&year=0&mileage=0")
# redis_client.lpush('cn2che', "http://www.cn2che.com/serial.html")
# redis_client.lpush('ganji', "http://www.ganji.com/index.htm")
# redis_client.lpush('haoche51', "http://www.haoche51.com/cn/ershouche/p1.html")
# redis_client.lpush('haoche99', "http://www.99haoche.com/quanguo/all/")
# redis_client.lpush('hx2car', "http://www.hx2car.com/quanguo/soa1")
# redis_client.lpush('iautos', "https://so.iautos.cn/quanguo/pasds9vepcatcpbnscac/")
# redis_client.lpush('renrenche', "https://www.renrenche.com/sh/ershouche")
# souhu_start_urls = redis_client2.lrange('souhu', 0, -1)
# print(souhu_start_urls)
# redis_client.lpush('souhu', *souhu_start_urls)
# redis_client.lpush('taoche', "http://quanguo.taoche.com/all/?orderid=5&direction=2&onsale=0#pagetag")
# redis_client.lpush('ttpai', "http://www.ttpai.cn/quanguo/list-p1")
# redis_client.lpush('xcar', "http://used.xcar.com.cn/search/100-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0/?page=0")
# redis_client.lpush('ygche', "http://www.ygche.com.cn/list/0_0_0_0_0_0_0_0_0_1.html")
# redis_client.lpush('youche', "https://www.youche.com/ershouche")
# youxin_start_urls = redis_client2.lrange('youxin', 0, 500000)
# # print(youxin_start_urls)
# redis_client.lpush('youxin', *youxin_start_urls)
#
# youxin_start_urls2 = redis_client2.lrange('youxin', 500001, 1000000)
# redis_client.lpush('youxin', *youxin_start_urls2)
#
# youxin_start_urls3 = redis_client2.lrange('youxin', 1000001, -1)
# redis_client.lpush('youxin', *youxin_start_urls3)
# redis_client.lpush('youxinpai', "http://i.youxinpai.com/LoginFromPCClient.aspx?key=5LFu9AuZj+n4mmgHy5M3iIGhoASQzWKXOTwV5YWeY0F+plxiJKChFWOt+MvUVPAx&Redirect=http://i.youxinpai.com/Default.aspx")
# redis_client.lpush('zg2sc', "http://www.zg2sc.cn/usedcar/search_result.do")
redis_client.lpush('anxinpai', "http://www.haicj.com/bidcar")




# s = redis_client.brpop('zg2sc')
# print(s)

# redis_client.lpush('requests', *['a', 'b', 'c'])