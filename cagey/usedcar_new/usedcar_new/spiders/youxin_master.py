# -*- coding: utf-8 -*-
import redis
import scrapy
import re
from scrapy_redis.spiders import RedisSpider
from usedcar_new.items import GuaziItem
import time
import execjs
import os
import json
# from usedcar_new.middlewares import ProxyMiddleware

# from .items import YouinMasterSpider Item
now_date = time.strftime('%Y-%m-%d %X', time.localtime())

pool = redis.ConnectionPool(host='192.168.1.92', port=6379, db=14)
con = redis.Redis(connection_pool=pool)
c = con.client()


class YouxinMasterSpider(scrapy.Spider):
    name = 'youxin_master'
    allowed_domains = ['xin.com']

    # start_urls = ['http://xin.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YouxinMasterSpider, self).__init__(**kwargs)
        self.counts = 0
        self.city_list = ['https://www.xin.com/hefei/s/', 'https://www.xin.com/anqing/s/',
                          'https://www.xin.com/bengbu/s/', 'https://www.xin.com/fuyang/s/',
                          'https://www.xin.com/huaibei/s/', 'https://www.xin.com/huainan/s/',
                          'https://www.xin.com/luan/s/', 'https://www.xin.com/maanshan/s/',
                          'https://www.xin.com/tongling/s/', 'https://www.xin.com/wuhu/s/',
                          'https://www.xin.com/xuancheng/s/', 'https://www.xin.com/chuzhou/s/',
                          'https://www.xin.com/bozhou/s/', 'https://www.xin.com/huangshan/s/',
                          'https://www.xin.com/suzhouah/s/', 'https://www.xin.com/beijing/s/',
                          'https://www.xin.com/fuzhou/s/', 'https://www.xin.com/xiamen/s/',
                          'https://www.xin.com/longyan/s/', 'https://www.xin.com/zhangzhou/s/',
                          'https://www.xin.com/putian/s/', 'https://www.xin.com/quanzhou/s/',
                          'https://www.xin.com/nanping/s/', 'https://www.xin.com/ningde/s/',
                          'https://www.xin.com/sanming/s/', 'https://www.xin.com/lanzhou/s/',
                          'https://www.xin.com/dingxi/s/', 'https://www.xin.com/pingliang/s/',
                          'https://www.xin.com/jiuquan/s/', 'https://www.xin.com/qingyang/s/',
                          'https://www.xin.com/wuwei/s/', 'https://www.xin.com/tianshui/s/',
                          'https://www.xin.com/baiyin/s/', 'https://www.xin.com/longnan/s/',
                          'https://www.xin.com/guangzhou/s/', 'https://www.xin.com/shenzhen/s/',
                          'https://www.xin.com/zhuhai/s/', 'https://www.xin.com/dongguan/s/',
                          'https://www.xin.com/zhongshan/s/', 'https://www.xin.com/shantou/s/',
                          'https://www.xin.com/chaozhou/s/', 'https://www.xin.com/shaoguan/s/',
                          'https://www.xin.com/zhanjiang/s/', 'https://www.xin.com/zhaoqing/s/',
                          'https://www.xin.com/maoming/s/', 'https://www.xin.com/meizhou/s/',
                          'https://www.xin.com/foshan/s/', 'https://www.xin.com/huizhou/s/',
                          'https://www.xin.com/jiangmen/s/', 'https://www.xin.com/jieyang/s/',
                          'https://www.xin.com/qingyuan/s/', 'https://www.xin.com/yangjiang/s/',
                          'https://www.xin.com/heyuan/s/', 'https://www.xin.com/shanwei/s/',
                          'https://www.xin.com/nanning/s/', 'https://www.xin.com/liuzhou/s/',
                          'https://www.xin.com/guilin/s/', 'https://www.xin.com/beihai/s/',
                          'https://www.xin.com/baise/s/', 'https://www.xin.com/hezhou/s/',
                          'https://www.xin.com/hechi/s/', 'https://www.xin.com/guigang/s/',
                          'https://www.xin.com/yulin/s/', 'https://www.xin.com/qinzhou/s/',
                          'https://www.xin.com/wuzhou/s/', 'https://www.xin.com/fangchenggang/s/',
                          'https://www.xin.com/guiyang/s/', 'https://www.xin.com/zunyi/s/',
                          'https://www.xin.com/bijie/s/', 'https://www.xin.com/liupanshui/s/',
                          'https://www.xin.com/tongren/s/', 'https://www.xin.com/haikou/s/',
                          'https://www.xin.com/sanya/s/', 'https://www.xin.com/shijiazhuang/s/',
                          'https://www.xin.com/tangshan/s/', 'https://www.xin.com/xingtai/s/',
                          'https://www.xin.com/qinhuangdao/s/', 'https://www.xin.com/langfang/s/',
                          'https://www.xin.com/handan/s/', 'https://www.xin.com/hengshui/s/',
                          'https://www.xin.com/cangzhou/s/', 'https://www.xin.com/baoding/s/',
                          'https://www.xin.com/zhangjiakou/s/', 'https://www.xin.com/chengde/s/',
                          'https://www.xin.com/zhengzhou/s/', 'https://www.xin.com/luoyang/s/',
                          'https://www.xin.com/zhoukou/s/', 'https://www.xin.com/xinyang/s/',
                          'https://www.xin.com/xinxiang/s/', 'https://www.xin.com/shangqiu/s/',
                          'https://www.xin.com/sanmenxia/s/', 'https://www.xin.com/puyang/s/',
                          'https://www.xin.com/nanyang/s/', 'https://www.xin.com/luohe/s/',
                          'https://www.xin.com/jiaozuo/s/', 'https://www.xin.com/kaifeng/s/',
                          'https://www.xin.com/anyang/s/', 'https://www.xin.com/dezhou/s/',
                          'https://www.xin.com/hebi/s/', 'https://www.xin.com/pingdingshan/s/',
                          'https://www.xin.com/zhumadian/s/', 'https://www.xin.com/xuchang/s/',
                          'https://www.xin.com/haerbin/s/', 'https://www.xin.com/daqing/s/',
                          'https://www.xin.com/qiqihaer/s/', 'https://www.xin.com/jiamusi/s/',
                          'https://www.xin.com/jixi/s/', 'https://www.xin.com/mudanjiang/s/',
                          'https://www.xin.com/qitaihe/s/', 'https://www.xin.com/yichun/s/',
                          'https://www.xin.com/heihe/s/', 'https://www.xin.com/suihua/s/',
                          'https://www.xin.com/shuangyashan/s/', 'https://www.xin.com/wuhan/s/',
                          'https://www.xin.com/shiyan/s/', 'https://www.xin.com/xiangyang/s/',
                          'https://www.xin.com/suizhou/s/', 'https://www.xin.com/xiantao/s/',
                          'https://www.xin.com/tianmenshi/s/', 'https://www.xin.com/yichang/s/',
                          'https://www.xin.com/huangshi/s/', 'https://www.xin.com/jingmen/s/',
                          'https://www.xin.com/jingzhou/s/', 'https://www.xin.com/huanggang/s/',
                          'https://www.xin.com/ezhou/s/', 'https://www.xin.com/xianning/s/',
                          'https://www.xin.com/xiaogan/s/', 'https://www.xin.com/qianjiang/s/',
                          'https://www.xin.com/changsha/s/', 'https://www.xin.com/chenzhou/s/',
                          'https://www.xin.com/changde/s/', 'https://www.xin.com/hengyang/s/',
                          'https://www.xin.com/huaihua/s/', 'https://www.xin.com/loudi/s/',
                          'https://www.xin.com/zhuzhou/s/', 'https://www.xin.com/yueyang/s/',
                          'https://www.xin.com/xiangtan/s/', 'https://www.xin.com/shaoyang/s/',
                          'https://www.xin.com/yiyang/s/', 'https://www.xin.com/zhangjiajie/s/',
                          'https://www.xin.com/changchun/s/', 'https://www.xin.com/jilin/s/',
                          'https://www.xin.com/tonghua/s/', 'https://www.xin.com/liaoyuan/s/',
                          'https://www.xin.com/baishan/s/', 'https://www.xin.com/baicheng/s/',
                          'https://www.xin.com/songyuan/s/', 'https://www.xin.com/nanjing/s/',
                          'https://www.xin.com/suzhou/s/', 'https://www.xin.com/wuxi/s/',
                          'https://www.xin.com/changzhou/s/', 'https://www.xin.com/huaian/s/',
                          'https://www.xin.com/lianyungang/s/', 'https://www.xin.com/nantong/s/',
                          'https://www.xin.com/yancheng/s/', 'https://www.xin.com/yangzhou/s/',
                          'https://www.xin.com/zhenjiang/s/', 'https://www.xin.com/taizhou/s/',
                          'https://www.xin.com/xuzhou/s/', 'https://www.xin.com/suqian/s/',
                          'https://www.xin.com/nanchang/s/', 'https://www.xin.com/shangrao/s/',
                          'https://www.xin.com/pingxiang/s/', 'https://www.xin.com/xinyu/s/',
                          'https://www.xin.com/yichunjx/s/', 'https://www.xin.com/jiujiang/s/',
                          'https://www.xin.com/ganzhou/s/', 'https://www.xin.com/jian/s/',
                          'https://www.xin.com/jingdezhen/s/', 'https://www.xin.com/fuzhoujx/s/',
                          'https://www.xin.com/siping/s/', 'https://www.xin.com/shenyang/s/',
                          'https://www.xin.com/dandong/s/', 'https://www.xin.com/fushun/s/',
                          'https://www.xin.com/fuxin/s/', 'https://www.xin.com/huludao/s/',
                          'https://www.xin.com/chaoyang/s/', 'https://www.xin.com/dalian/s/',
                          'https://www.xin.com/benxi/s/', 'https://www.xin.com/anshan/s/',
                          'https://www.xin.com/jinzhou/s/', 'https://www.xin.com/liaoyang/s/',
                          'https://www.xin.com/yingkou/s/', 'https://www.xin.com/panjin/s/',
                          'https://www.xin.com/tieling/s/', 'https://www.xin.com/huhehaote/s/',
                          'https://www.xin.com/baotou/s/', 'https://www.xin.com/chifeng/s/',
                          'https://www.xin.com/tongliao/s/', 'https://www.xin.com/wuhai/s/',
                          'https://www.xin.com/eerduosi/s/', 'https://www.xin.com/hulunbeier/s/',
                          'https://www.xin.com/xilinguolemeng/s/', 'https://www.xin.com/wulanchabu/s/',
                          'https://www.xin.com/alashanmeng/s/', 'https://www.xin.com/yinchuan/s/',
                          'https://www.xin.com/wuzhong/s/', 'https://www.xin.com/guyuan/s/',
                          'https://www.xin.com/shizuishan/s/', 'https://www.xin.com/xining/s/',
                          'https://www.xin.com/haidong/s/', 'https://www.xin.com/jinan/s/',
                          'https://www.xin.com/qingdao/s/', 'https://www.xin.com/yantai/s/',
                          'https://www.xin.com/weihai/s/', 'https://www.xin.com/weifang/s/',
                          'https://www.xin.com/taian/s/', 'https://www.xin.com/zaozhuang/s/',
                          'https://www.xin.com/zibo/s/', 'https://www.xin.com/dongying/s/',
                          'https://www.xin.com/heze/s/', 'https://www.xin.com/binzhou/s/',
                          'https://www.xin.com/liaocheng/s/', 'https://www.xin.com/linyi/s/',
                          'https://www.xin.com/jiningsd/s/', 'https://www.xin.com/rizhao/s/',
                          'https://www.xin.com/laiwu/s/', 'https://www.xin.com/taiyuan/s/',
                          'https://www.xin.com/datong/s/', 'https://www.xin.com/jincheng/s/',
                          'https://www.xin.com/jinzhong/s/', 'https://www.xin.com/linfen/s/',
                          'https://www.xin.com/changzhi/s/', 'https://www.xin.com/yuncheng/s/',
                          'https://www.xin.com/xinzhou/s/', 'https://www.xin.com/yangquan/s/',
                          'https://www.xin.com/shuozhou/s/', 'https://www.xin.com/lvliang/s/',
                          'https://www.xin.com/xian/s/', 'https://www.xin.com/xianyang/s/',
                          'https://www.xin.com/weinan/s/', 'https://www.xin.com/yulinsx/s/',
                          'https://www.xin.com/baoji/s/', 'https://www.xin.com/ankang/s/',
                          'https://www.xin.com/hanzhong/s/', 'https://www.xin.com/yanan/s/',
                          'https://www.xin.com/tongchuan/s/', 'https://www.xin.com/shangluo/s/',
                          'https://www.xin.com/shanghai/s/', 'https://www.xin.com/chengdu/s/',
                          'https://www.xin.com/mianyang/s/', 'https://www.xin.com/suining/s/',
                          'https://www.xin.com/panzhihua/s/', 'https://www.xin.com/yibin/s/',
                          'https://www.xin.com/zigong/s/', 'https://www.xin.com/guangyuan/s/',
                          'https://www.xin.com/deyang/s/', 'https://www.xin.com/leshan/s/',
                          'https://www.xin.com/nanchong/s/', 'https://www.xin.com/meishan/s/',
                          'https://www.xin.com/luzhou/s/', 'https://www.xin.com/neijiang/s/',
                          'https://www.xin.com/dazhou/s/', 'https://www.xin.com/guangan/s/',
                          'https://www.xin.com/tianjin/s/', 'https://www.xin.com/shannanshi/s/',
                          'https://www.xin.com/wulumuqi/s/', 'https://www.xin.com/hami/s/',
                          'https://www.xin.com/tulufan/s/', 'https://www.xin.com/shihezishi/s/',
                          'https://www.xin.com/kunming/s/', 'https://www.xin.com/yuxi/s/',
                          'https://www.xin.com/qujing/s/', 'https://www.xin.com/baoshanshi/s/',
                          'https://www.xin.com/zhaotong/s/', 'https://www.xin.com/lijiang/s/',
                          'https://www.xin.com/hangzhou/s/', 'https://www.xin.com/ningbo/s/',
                          'https://www.xin.com/wenzhou/s/', 'https://www.xin.com/jiaxing/s/',
                          'https://www.xin.com/jinhua/s/', 'https://www.xin.com/lishui/s/',
                          'https://www.xin.com/huzhou/s/', 'https://www.xin.com/quzhou/s/',
                          'https://www.xin.com/taizhouzj/s/', 'https://www.xin.com/shaoxing/s/',
                          'https://www.xin.com/zhoushan/s/', 'https://www.xin.com/chongqing/s/',
                          'https://www.xin.com/bayannaoer/s/', 'https://www.xin.com/zhongwei/s/',
                          'https://www.xin.com/yanbianchaoxianzuzizhizhou/s/',
                          'https://www.xin.com/enshitujiazuzizhizhou/s/', 'https://www.xin.com/chongzuo/s/',
                          'https://www.xin.com/liangshanyizuzizhizhou/s/', 'https://www.xin.com/qianxinan/s/',
                          'https://www.xin.com/qiandongnan/s/', 'https://www.xin.com/qiannanbuyizu/s/',
                          'https://www.xin.com/chuxiong/s/', 'https://www.xin.com/honghehanizu/s/',
                          'https://www.xin.com/wenshanzhuangzuzizhizhou/s/',
                          'https://www.xin.com/xishuangbannadaizuzizhizhou/s/',
                          'https://www.xin.com/dalibaizuzizhizhou/s/',
                          'https://www.xin.com/dehongdaizujingpozuzizhizhou/s/',
                          'https://www.xin.com/linxiahuizuzizhizhou/s/', 'https://www.xin.com/huangnan/s/',
                          'https://www.xin.com/changjihuizuzizhizhou/s/', 'https://www.xin.com/bayinguoleng/s/',
                          'https://www.xin.com/akesudiqu/s/', 'https://www.xin.com/yilihasakezizhizhou/s/']
        self.brand_list = ['https://www.xin.com/shanghai/yaxing/', 'https://www.xin.com/shanghai/ruichixinnenyuan/',
                           'https://www.xin.com/shanghai/localmotors/', 'https://www.xin.com/shanghai/biaozhi/',
                           'https://www.xin.com/shanghai/jianglingjituanxinnenyuan/',
                           'https://www.xin.com/shanghai/saibao/', 'https://www.xin.com/shanghai/zhongshun/',
                           'https://www.xin.com/shanghai/dongfengfengxing/',
                           'https://www.xin.com/shanghai/oushangqiche/', 'https://www.xin.com/shanghai/alpina/',
                           'https://www.xin.com/shanghai/kaibaihe/', 'https://www.xin.com/shanghai/guanzhi/',
                           'https://www.xin.com/shanghai/maibahe/', 'https://www.xin.com/shanghai/liebaoqiche/',
                           'https://www.xin.com/shanghai/juntianqiche/', 'https://www.xin.com/shanghai/luofuhate/',
                           'https://www.xin.com/shanghai/lite/', 'https://www.xin.com/shanghai/beiqixinnenyuan/',
                           'https://www.xin.com/shanghai/zhonghua/', 'https://www.xin.com/shanghai/aerfaluomiou/',
                           'https://www.xin.com/shanghai/xiaopengqiche/',
                           'https://www.xin.com/shanghai/polestarjixing/', 'https://www.xin.com/shanghai/qiantu/',
                           'https://www.xin.com/shanghai/leikesasi/', 'https://www.xin.com/shanghai/yingfeinidi/',
                           'https://www.xin.com/shanghai/dazhong/', 'https://www.xin.com/shanghai/kelaisile/',
                           'https://www.xin.com/shanghai/sabo/', 'https://www.xin.com/shanghai/beiqizhizao/',
                           'https://www.xin.com/shanghai/jeep/', 'https://www.xin.com/shanghai/yutongkeche/',
                           'https://www.xin.com/shanghai/kaimaqiche/', 'https://www.xin.com/shanghai/lifan/',
                           'https://www.xin.com/shanghai/siweiqiche/', 'https://www.xin.com/shanghai/lutesi/',
                           'https://www.xin.com/shanghai/woerwo/', 'https://www.xin.com/shanghai/shuanglong/',
                           'https://www.xin.com/shanghai/xingtu/', 'https://www.xin.com/shanghai/sitech/',
                           'https://www.xin.com/shanghai/kenisaike/', 'https://www.xin.com/shanghai/weiziman/',
                           'https://www.xin.com/shanghai/hanma/', 'https://www.xin.com/shanghai/hanlongqiche/',
                           'https://www.xin.com/shanghai/huakai/', 'https://www.xin.com/shanghai/guangqixinnenyuan/',
                           'https://www.xin.com/shanghai/ktm/', 'https://www.xin.com/shanghai/yujie/',
                           'https://www.xin.com/shanghai/xiyate/', 'https://www.xin.com/shanghai/yongyuan/',
                           'https://www.xin.com/shanghai/tongtian/', 'https://www.xin.com/shanghai/beijing/',
                           'https://www.xin.com/shanghai/asidunmading/', 'https://www.xin.com/shanghai/lianhua/',
                           'https://www.xin.com/shanghai/chenggong/', 'https://www.xin.com/shanghai/jinbei/',
                           'https://www.xin.com/shanghai/futianchengyongche/', 'https://www.xin.com/shanghai/fengtian/',
                           'https://www.xin.com/shanghai/jieda/', 'https://www.xin.com/shanghai/hafei/',
                           'https://www.xin.com/shanghai/richan/', 'https://www.xin.com/shanghai/beiqidaoda/',
                           'https://www.xin.com/shanghai/oula/', 'https://www.xin.com/shanghai/sanling/',
                           'https://www.xin.com/shanghai/tesila/', 'https://www.xin.com/shanghai/wey/',
                           'https://www.xin.com/shanghai/changhe/', 'https://www.xin.com/shanghai/guojizhijun/',
                           'https://www.xin.com/shanghai/spirra/', 'https://www.xin.com/shanghai/weilin/',
                           'https://www.xin.com/shanghai/yusheng/', 'https://www.xin.com/shanghai/yulu/',
                           'https://www.xin.com/shanghai/jiulong/', 'https://www.xin.com/shanghai/haima/',
                           'https://www.xin.com/shanghai/meiya/', 'https://www.xin.com/shanghai/dianka/',
                           'https://www.xin.com/shanghai/guangqichuanqi/', 'https://www.xin.com/shanghai/jinlong/',
                           'https://www.xin.com/shanghai/lufeng/', 'https://www.xin.com/shanghai/anchi/',
                           'https://www.xin.com/shanghai/linken/', 'https://www.xin.com/shanghai/huapu/',
                           'https://www.xin.com/shanghai/qirui/', 'https://www.xin.com/shanghai/tangjunqiche/',
                           'https://www.xin.com/shanghai/dongfeng/', 'https://www.xin.com/shanghai/tongbao/',
                           'https://www.xin.com/shanghai/shangqidatong/', 'https://www.xin.com/shanghai/qichen/',
                           'https://www.xin.com/shanghai/jinlv/', 'https://www.xin.com/shanghai/yiqi/',
                           'https://www.xin.com/shanghai/changan/', 'https://www.xin.com/shanghai/dachengqiche/',
                           'https://www.xin.com/shanghai/guanggang/', 'https://www.xin.com/shanghai/baoshijie/',
                           'https://www.xin.com/shanghai/baowo/', 'https://www.xin.com/shanghai/huaqi/',
                           'https://www.xin.com/shanghai/dafa/', 'https://www.xin.com/shanghai/beijingqiche/',
                           'https://www.xin.com/shanghai/nanjingjinlong/', 'https://www.xin.com/shanghai/lingtuqiche/',
                           'https://www.xin.com/shanghai/shanqitongjia/', 'https://www.xin.com/shanghai/tengshi/',
                           'https://www.xin.com/shanghai/mashaladi/', 'https://www.xin.com/shanghai/tianjiqiche/',
                           'https://www.xin.com/shanghai/bisuqiche/', 'https://www.xin.com/shanghai/dongfengruitaite/',
                           'https://www.xin.com/shanghai/huaxiang/', 'https://www.xin.com/shanghai/fuqiqiteng/',
                           'https://www.xin.com/shanghai/changcheng/', 'https://www.xin.com/shanghai/guangqijiao/',
                           'https://www.xin.com/shanghai/xiandai/', 'https://www.xin.com/shanghai/jiliqiche/',
                           'https://www.xin.com/shanghai/kangdiquanqiuying/', 'https://www.xin.com/shanghai/lingke/',
                           'https://www.xin.com/shanghai/mazida/', 'https://www.xin.com/shanghai/yundu/',
                           'https://www.xin.com/shanghai/zhongou/', 'https://www.xin.com/shanghai/hafu/',
                           'https://www.xin.com/shanghai/leinuo/', 'https://www.xin.com/shanghai/dayu/',
                           'https://www.xin.com/shanghai/bieke/', 'https://www.xin.com/shanghai/aichi/',
                           'https://www.xin.com/shanghai/beiqiweiwang/', 'https://www.xin.com/shanghai/huasong/',
                           'https://www.xin.com/shanghai/oubao/', 'https://www.xin.com/shanghai/ruiqi/',
                           'https://www.xin.com/shanghai/weimaqiche/', 'https://www.xin.com/shanghai/bujiadi/',
                           'https://www.xin.com/shanghai/huanghai/', 'https://www.xin.com/shanghai/dongfengfengdu/',
                           'https://www.xin.com/shanghai/jianghuai/', 'https://www.xin.com/shanghai/jiebao/',
                           'https://www.xin.com/shanghai/wuling/', 'https://www.xin.com/shanghai/jiangling/',
                           'https://www.xin.com/shanghai/mogen/', 'https://www.xin.com/shanghai/daoqi/',
                           'https://www.xin.com/shanghai/gmc/', 'https://www.xin.com/shanghai/benteng/',
                           'https://www.xin.com/shanghai/huatai/', 'https://www.xin.com/shanghai/luofu/',
                           'https://www.xin.com/shanghai/zhongtai/', 'https://www.xin.com/shanghai/qingnianqiche/',
                           'https://www.xin.com/shanghai/zhongxing/', 'https://www.xin.com/shanghai/nazhaqiche/',
                           'https://www.xin.com/shanghai/kawei/', 'https://www.xin.com/shanghai/yemaqiche/',
                           'https://www.xin.com/shanghai/zhinuo/', 'https://www.xin.com/shanghai/ludifangzhou/',
                           'https://www.xin.com/shanghai/aodi/', 'https://www.xin.com/shanghai/hongxingqiche/',
                           'https://www.xin.com/shanghai/kaiyi/', 'https://www.xin.com/shanghai/huataixinnenyuan/',
                           'https://www.xin.com/shanghai/xinyuan/', 'https://www.xin.com/shanghai/jinchengqiche/',
                           'https://www.xin.com/shanghai/kairui/', 'https://www.xin.com/shanghai/huabei/',
                           'https://www.xin.com/shanghai/mini/', 'https://www.xin.com/shanghai/sihao/',
                           'https://www.xin.com/shanghai/guangqijituan/', 'https://www.xin.com/shanghai/mingjue/',
                           'https://www.xin.com/shanghai/hanteng/', 'https://www.xin.com/shanghai/nanqi/',
                           'https://www.xin.com/shanghai/taikate/', 'https://www.xin.com/shanghai/linian/',
                           'https://www.xin.com/shanghai/kasheng/', 'https://www.xin.com/shanghai/binli/',
                           'https://www.xin.com/shanghai/lada/', 'https://www.xin.com/shanghai/dongnan/',
                           'https://www.xin.com/shanghai/kaersen/', 'https://www.xin.com/shanghai/leiding/',
                           'https://www.xin.com/shanghai/shuixing/', 'https://www.xin.com/shanghai/xinkai/',
                           'https://www.xin.com/shanghai/beiqihuansu/', 'https://www.xin.com/shanghai/sailin/',
                           'https://www.xin.com/shanghai/benchi/', 'https://www.xin.com/shanghai/xuefulan/',
                           'https://www.xin.com/shanghai/wanfeng/', 'https://www.xin.com/shanghai/luhu/',
                           'https://www.xin.com/shanghai/yiqilinghe/', 'https://www.xin.com/shanghai/sikeda/',
                           'https://www.xin.com/shanghai/rongdazhizao/', 'https://www.xin.com/shanghai/futian/',
                           'https://www.xin.com/shanghai/jietu/', 'https://www.xin.com/shanghai/acschnitzer/',
                           'https://www.xin.com/shanghai/xindadi/', 'https://www.xin.com/shanghai/dongfengfengshen/',
                           'https://www.xin.com/shanghai/fudi/', 'https://www.xin.com/shanghai/sibalu/',
                           'https://www.xin.com/shanghai/laosilaisi/', 'https://www.xin.com/shanghai/babosi/',
                           'https://www.xin.com/shanghai/qiya/', 'https://www.xin.com/shanghai/falali/',
                           'https://www.xin.com/shanghai/zhidou/', 'https://www.xin.com/shanghai/feiyate/',
                           'https://www.xin.com/shanghai/sidataike/', 'https://www.xin.com/shanghai/lingmu/',
                           'https://www.xin.com/shanghai/weichaiyingzhi/', 'https://www.xin.com/shanghai/lingpaoqiche/',
                           'https://www.xin.com/shanghai/baolong/', 'https://www.xin.com/shanghai/laolunshi/',
                           'https://www.xin.com/shanghai/nazhijie/', 'https://www.xin.com/shanghai/yunque/',
                           'https://www.xin.com/shanghai/dongfengxiaokang/', 'https://www.xin.com/shanghai/huayang/',
                           'https://www.xin.com/shanghai/lixiang/', 'https://www.xin.com/shanghai/hangtian/',
                           'https://www.xin.com/shanghai/haige/', 'https://www.xin.com/shanghai/xuetielong/',
                           'https://www.xin.com/shanghai/shuanghuan/',
                           'https://www.xin.com/shanghai/dongfengfengguang/', 'https://www.xin.com/shanghai/fute/',
                           'https://www.xin.com/shanghai/biyadi/', 'https://www.xin.com/shanghai/weilai/',
                           'https://www.xin.com/shanghai/dadi/', 'https://www.xin.com/shanghai/nanjunqiche/',
                           'https://www.xin.com/shanghai/hengtian/', 'https://www.xin.com/shanghai/zhongyu/',
                           'https://www.xin.com/shanghai/guojinqiche/', 'https://www.xin.com/shanghai/shijue/',
                           'https://www.xin.com/shanghai/tianma/', 'https://www.xin.com/shanghai/yiweike/',
                           'https://www.xin.com/shanghai/weichaiqiche/', 'https://www.xin.com/shanghai/baoqiqiche/',
                           'https://www.xin.com/shanghai/hongqi/',
                           'https://www.xin.com/shanghai/jianglingjituanqingqi/',
                           'https://www.xin.com/shanghai/yunbao/', 'https://www.xin.com/shanghai/changanqingxingche/',
                           'https://www.xin.com/shanghai/heibao/', 'https://www.xin.com/shanghai/beijingqingxing/',
                           'https://www.xin.com/shanghai/jiangnan/', 'https://www.xin.com/shanghai/qiaozhibadun/',
                           'https://www.xin.com/shanghai/siming/', 'https://www.xin.com/shanghai/smart/',
                           'https://www.xin.com/shanghai/baoma/', 'https://www.xin.com/shanghai/ruhu/',
                           'https://www.xin.com/shanghai/fisker/', 'https://www.xin.com/shanghai/huizhong/',
                           'https://www.xin.com/shanghai/ds/', 'https://www.xin.com/shanghai/wushiling/',
                           'https://www.xin.com/shanghai/kaidilake/', 'https://www.xin.com/shanghai/lanbojini/',
                           'https://www.xin.com/shanghai/ouge/', 'https://www.xin.com/shanghai/maikailun/',
                           'https://www.xin.com/shanghai/ankai/', 'https://www.xin.com/shanghai/changanoushang/',
                           'https://www.xin.com/shanghai/xinbaojun/', 'https://www.xin.com/shanghai/baojun/',
                           'https://www.xin.com/shanghai/junmaqiche/', 'https://www.xin.com/shanghai/rongwei/',
                           'https://www.xin.com/shanghai/pajiani/', 'https://www.xin.com/shanghai/duoshixing/',
                           'https://www.xin.com/shanghai/bentian/', 'https://www.xin.com/shanghai/xinte/']

        self.c = con.client()
        self.drop_num = 0
        self.all_num = 0
        self.fail_url = []

        self.headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
          # 'cookie': f'acw_sc__v2={Cookie}',
        }


    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'youxin_sid_test',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'youxin_sid_test',
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'COOKIES_ENABLED': False,
        'REDIS_URL': 'redis://192.168.1.92:6379/14',
        'DOWNLOADER_MIDDLEWARES': {
            'usedcar_new.middlewares.ProxyMiddleware': 700,
            # 'usedcar_new.middlewares.MoGuProxyMiddleware': 700,
            # 'usedcar_new.middlewares.SeleniumIPMiddleware': 701,
            # 'usedcar_new.middlewares.UsedcarNewDownloaderMiddleware': 701,
            'usedcar_new.middlewares.MyproxiesSpiderMiddleware': 701,
        },
        'ITEM_PIPELINES': {
            'usedcar_new.pipelines.GanjiPipeline': 300,
        },
    }


    def get_cookie(self, code):
        Cookie = execjs.compile(open("./tools/youxin.js").read()).call('getpwd', code)
        headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
          'cookie': f'acw_sc__v2={Cookie}',
        }
        return headers

    def start_requests(self):
        city_url_list = ["https://www.xin.com/shanghai/s/"]
        for city_url in city_url_list:
            yield scrapy.Request(
                url=city_url,
                callback=self.parse_brand,
                dont_filter=True,
                headers=self.headers
            )

    def parse_brand(self, response):
        brand_list = response.xpath("//li[contains(@class,'li_spell li_spell_')]//dd/a/@href").getall()
        for brand_url in brand_list:
            brand_url = response.urljoin(brand_url)
            # print(brand_url)
            yield scrapy.Request(
                url=brand_url,
                dont_filter=True,
                callback=self.parse,
                headers=self.headers
            )

    def parse(self, response):
        if 'arg1' in response.text:
            arg_code = re.findall("var arg1='(.*?)';", response.text)[0]
            headers = self.get_cookie(arg_code)
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                headers=headers,
                dont_filter=True
            )
        else:
            counts = response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+')[0] \
                if response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+') else 0
            counts = int(counts)
            if counts != 0:
                if counts <= 2000:
                    print(counts)
                    print("1" * 100)
                    page_num = int(counts/40)
                    for i in range(1, page_num+2):
                        url = response.url+f'i{i}/'
                        yield scrapy.Request(
                                url=url,
                                callback=self.parse_data,
                                dont_filter=True,
                                headers=self.headers
                            )
                else:
                    for href in response.xpath('//div[@class="select-con"][2]/dl/dd/a'):
                        urlbase = href.xpath('@href').get()
                        if urlbase and 'javascript' not in urlbase:
                            url = response.urljoin(urlbase)
                            yield scrapy.Request(url, self.select2_parse, dont_filter=True, headers=self.headers)

    def select2_parse(self, response):
        if 'arg1' in response.text:
            arg_code = re.findall("var arg1='(.*?)';", response.text)[0]
            headers = self.get_cookie(arg_code)
            yield scrapy.Request(
                url=response.url,
                callback=self.select2_parse,
                headers=headers,
                dont_filter=True
            )
        else:
            counts = response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+')[0] \
                if response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+') else 0
            counts = int(counts)
            if counts != 0:
                if counts <= 2000:
                    print(counts)
                    print("2" * 100)
                    page_num = int(counts / 40)
                    for i in range(1, page_num + 2):
                        url = response.url + f'i{i}/'
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse_data,
                            dont_filter=True,
                            headers=self.headers
                        )
                else:
                    print("*"*100)
                    print(counts)
                    for href in response.xpath("//dl[@id='select3']//dd/a"):
                        urlbase = href.xpath('@href').get()
                        if urlbase and 'javascript' not in urlbase:
                            url = response.urljoin(urlbase)
                            yield scrapy.Request(url, self.select3_parse, dont_filter=True, headers=self.headers)

    def select3_parse(self, response):
        if 'arg1' in response.text:
            arg_code = re.findall("var arg1='(.*?)';", response.text)[0]
            headers = self.get_cookie(arg_code)
            yield scrapy.Request(
                url=response.url,
                callback=self.select3_parse,
                headers=headers,
                dont_filter=True
            )
        else:
            counts = response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+')[0] \
                if response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+') else 0
            counts = int(counts)
            if counts != 0:
                print(counts)
                print("3" * 100)
                page_num = int(counts / 40)
                for i in range(1, page_num + 2):
                    url = response.url + f'i{i}/'
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_data,
                        dont_filter=True,
                        headers=self.headers
                    )

    def parse_data(self, response):
        # print(response.url)
        # counts = response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+')[0] \
        #     if response.xpath("//h4[contains(text(),'全部车源')]/text()").re('\d+') else 0
        # counts = float(counts)
        node_list = response.xpath('//li[@class="con caritem conHeight"]')
        for node in node_list:
            urlbase = node.xpath('.//a[@class="aimg"]/@href').get()
            url = response.urljoin(urlbase)
            self.c.lpush('youxin:start_urls', url)
            print(url)
            # item = GuaziItem()
            # item["page_num"] = counts
            # item["price"] = node.xpath('.//em[contains(text(),"万")]/text()').get().replace(' ', '').replace(
            #     '\n', '').replace('\r', '').replace('万', '')
            # item["city_id"] = url.split("=")[1]
            # item["store"] = node.xpath('.//span[contains(text(),"仓")]/text()').get()
            # item["car_id"] = re.findall("che(.*?)\.html", url)[0]
            # item["sid"] = re.findall("com/(.*?)/che", url)[0]
            # item["url"] = url
            # item["page_url"] = response.url
            # item["statusplus"] = url + '-' + item["store"] + '-' + item["price"] + '-' + item["page_url"]
            # yield item
            # print(item)
        # next_page = response.xpath('//a[contains(text(),"下一页")]')
        # if next_page:
        #     urlbase = response.xpath('./@href').get()
        #     next_url = response.urljoin(urlbase)
        #     print(next_url)
        #     print('9'*100)
        #     yield scrapy.Request(
        #             url=next_url,
        #             callback=self.parse_data,
        #             dont_filter=True,
        #             headers=self.headers
        #         )
