# -*- coding:utf-8 -*-
import redis

brands = ['/s/audi', '/s/aerfa', '/s/astonmartin', '/s/brd536', '/s/baofeili', '/s/porsche', '/s/buick', '/s/bj',
                  '/s/beiqi', '/s/weiwang', '/s/huansu', '/s/shenbaop', '/s/benteng', '/s/benz', '/s/bmw', '/s/baojun',
                  '/s/baolong', '/s/bentley', '/s/brabus', '/s/bugatti', '/s/honda', '/s/peugeot', '/s/byd', '/s/brd167',
                  '/s/baowo', '/s/bisu', '/s/changhe', '/s/changcheng', '/s/changanshy', '/s/changan', '/s/brd497', '/s/ds',
                  '/s/dongnan', '/s/dongfeng', '/s/xiaokang', '/s/dongfengfengdu', '/s/fengshen', '/s/fengxing', '/s/brd170',
                  '/s/vw', '/s/dadi', '/s/datong', '/s/dodge', '/s/toyota', '/s/ferrari', '/s/ford', '/s/futian', '/s/fudi',
                  '/s/fiat', '/s/brd41', '/s/qiteng', '/s/brd543', '/s/brd545', '/s/gmc', '/s/guanggang', '/s/chuanqi', '/s/jiao',
                  '/s/guanzhi', '/s/huapu', '/s/huatai', '/s/fuqip', '/s/huasong', '/s/haval', '/s/hafei', '/s/hengtian',
                  '/s/hummer', '/s/huizhong', '/s/haige', '/s/haima', '/s/brd54', '/s/hongqi', '/s/huanghai', '/s/brd173',
                  '/s/hanteng', '/s/jeep', '/s/jiulongp', '/s/geely', '/s/quanqiuying', '/s/dihao', '/s/yinglun', '/s/jaguar',
                  '/s/jiangnan', '/s/jianghuai', '/s/jiangling', '/s/brd71', '/s/jinbei', '/s/brd69', '/s/brd542', '/s/chrysler',
                  '/s/kaiyi', '/s/cadillac', '/s/kawei', '/s/kaersen', '/s/kairui', '/s/brd76', '/s/brd546', '/s/lamborghini',
                  '/s/lifan', '/s/laosilaisi', '/s/lincoln', '/s/liebao', '/s/linian', '/s/lianhua', '/s/lotus', '/s/landrover',
                  '/s/suzuki', '/s/lufeng', '/s/lexus', '/s/renault', '/s/mg', '/s/mini', '/s/brd98', '/s/maserati', '/s/meiya',
                  '/s/mclaren', '/s/maybach', '/s/mazda', '/s/nazhijie', '/s/oubao', '/s/oulangp', '/s/acura', '/s/pagani',
                  '/s/qichen', '/s/chery', '/s/qingling', '/s/kia', '/s/nissan', '/s/ruiqip', '/s/roewe', '/s/smart',
                  '/s/mitsubishi', '/s/shijue', '/s/shuanghuan', '/s/shuanglong', '/s/subaru', '/s/skoda', '/s/sabo',
                  '/s/simingp', '/s/siwei', '/s/brd120', '/s/tianma', '/s/tengship', '/s/wuling', '/s/weiziman', '/s/weilin',
                  '/s/volvo', '/s/isuzu', '/s/brd544', '/s/xiali', '/s/xinkai', '/s/brd151', '/s/xinyatup', '/s/hyundai',
                  '/s/xiyate', '/s/chevrolet', '/s/citroen', '/s/faw', '/s/naveco', '/s/brd136', '/s/yongyuanp', '/s/yingzhi',
                  '/s/infiniti', '/s/yema', '/s/zhongxing', '/s/zhonghuap', '/s/huabei', '/s/zhongou', '/s/zhongshun',
                  '/s/zhongtai', '/s/zhidou']

cities = ['/hz', '/bjs', '/shs', '/gz', '/sc', '/zqs', '/cd', '/sz', '/nb', '/wz', '/tz', '/xa', '/sy', '/sjz', '/zz', '/nj',
          '/jn', '/wh', '/wx', '/wf', '/fs', '/hf', '/dl', '/xm', '/shx', '/cs', '/dg', '/km', '/liny', '/chz', '/jh', '/heb',
          '/km', '/cc', '/tzh']

ages = ['/00ag1', '/00ag2', '/00ag3', '/00ag4', '/00ag5', '/00ag6']


# redis_client = redis.Redis('192.168.84.129', port=6379, db=1)
redis_client = redis.Redis('192.168.1.247', port=6379, db=1)
for city in cities:
    for brand in brands:
        for age in ages:
            url = 'https://www.chemao.com' + city + brand + age
            redis_client.lpush('chemao', url)

# print(len(urls))

# redis_client.lrem('chemao', 'https://www.chemao.com/tzh/s/zhidou/00ag6')