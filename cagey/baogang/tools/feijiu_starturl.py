import pandas as pd
import pymysql

__author__ = 'cagey'

import redis
import time


def readMysql127(db, tablename):
    dbconn = pymysql.connect(
        host="127.0.0.1",
        database=db,
        user="dataUser94",
        password="yangkaiqi",
        port=3306,
        charset='utf8')
    # 查询
    sqlcmd = "select * from " + tablename
    df = pd.read_sql(sqlcmd, dbconn)
    return df


# df = readMysql127('baogang', 'feijiu_url3')
# start_url_list = df["url"].tolist()
start_url_list = ['http://www.feijiu.net/QiTaMuZhiPin/', 'http://www.feijiu.net/YuanPianBoLi/', 'http://www.feijiu.net/FeiMuTou/', 'http://www.feijiu.net/JiaJuLei/', 'http://www.feijiu.net/BanCaiLei/', 'http://www.feijiu.net/YuanMuLei/', 'http://www.feijiu.net/XiangJiaoFeiLiao/', 'http://www.feijiu.net/SuJiaoBianJiaoL/', 'http://www.feijiu.net/JiuDianYongPinCDBZ/', 'http://www.feijiu.net/ErShouYiQiYB/', 'http://www.feijiu.net/ZaiShengXiangJiao/', 'http://www.feijiu.net/MoJuGang/', 'http://www.feijiu.net/HeJinGang/', 'http://www.feijiu.net/HeJin/', 'http://www.feijiu.net/BuXiuTie/', 'http://www.feijiu.net/GuanBan/', 'http://www.feijiu.net/BaoFei/', 'http://www.feijiu.net/ChongYaJian/', 'http://www.feijiu.net/GangSiSheng_/', 'http://www.feijiu.net/FeiTong_1/', 'http://www.feijiu.net/NaiCaiNaiHCLNHZ/', 'http://www.feijiu.net/HanSiHanTiao/', 'http://www.feijiu.net/ErShouTongXunSB/', 'http://www.feijiu.net/XiGuiJinShu/', 'http://www.feijiu.net/KuangYeSheBei/', 'http://www.feijiu.net/ErShouChuFangSB/', 'http://www.feijiu.net/JiuDianBinGuanSB_/', 'http://www.feijiu.net/zhiyaosb/', 'http://www.feijiu.net/BaoFeiHunHeJS/', 'http://www.feijiu.net/KongFenSheBei_/', 'http://www.feijiu.net/YinRanSheBei/', 'http://www.feijiu.net/LouYuSheShi_/', 'http://www.feijiu.net/GangJieGouSheB/', 'http://www.feijiu.net/ErShouLiuShuiX/', 'http://www.feijiu.net/YingYuanSheBei/', 'http://www.feijiu.net/GangTie/', 'http://www.feijiu.net/ReChuLiSheBei/', 'http://www.feijiu.net/ZhiLengSheBei_/', 'http://www.feijiu.net/ChaiQianChaiChu/', 'http://www.feijiu.net/DianZiSheBei_/', 'http://www.feijiu.net/ShuiBeng_/', 'http://www.feijiu.net/YouSeJinShu/', 'http://www.feijiu.net/FaMenSheBei/', 'http://www.feijiu.net/JianCaiSheBei/', 'http://www.feijiu.net/PeiJianSheBei/', 'http://www.feijiu.net/HuanBaoSheBei_/', 'http://www.feijiu.net/BeiPinBeiJian/', 'http://www.feijiu.net/ZhouChengSheBei_/', 'http://www.feijiu.net/ShuiNiJiXie/', 'http://www.feijiu.net/FuZhuangChangSheB/', 'http://www.feijiu.net/FengJiSheBei/', 'http://www.feijiu.net/MuGongJiXie/', 'http://www.feijiu.net/JiaoTongYunShu/', 'http://www.feijiu.net/BianSuSheBei_/', 'http://www.feijiu.net/BaoZhuangSheBei/', 'http://www.feijiu.net/YaSuJi_/', 'http://www.feijiu.net/YinShuaSheBei_/', 'http://www.feijiu.net/ZaoZhiSheBei_/', 'http://www.feijiu.net/YiQiYiBiao/', 'http://www.feijiu.net/ShiPinJiXie/', 'http://www.feijiu.net/KuangShanSheBei_/', 'http://www.feijiu.net/YiLiaoSheBei_/', 'http://www.feijiu.net/KTVSheB/', 'http://www.feijiu.net/NongYongJiXie/', 'http://www.feijiu.net/GuoLuSheBei_/', 'http://www.feijiu.net/BianYaQi_/', 'http://www.feijiu.net/SuLiaoJiXie_/', 'http://www.feijiu.net/YeJinSheBei/', 'http://www.feijiu.net/DunDai/', 'http://www.feijiu.net/FangZhiSheBei/', 'http://www.feijiu.net/BianZhiDai/', 'http://www.feijiu.net/TuLiao_/', 'http://www.feijiu.net/RanLiao_/', 'http://www.feijiu.net/YouQi_/', 'http://www.feijiu.net/LiQing_/', 'http://www.feijiu.net/BaoZhuangYinSZJFL/', 'http://www.feijiu.net/BanGongJiaoYTSJSB/', 'http://www.feijiu.net/LiPinGongYPZBWJ/', 'http://www.feijiu.net/ZhaoMingDianGDQ/', 'http://www.feijiu.net/NongYeShiPYL/', 'http://www.feijiu.net/AnQuanFangHQJ/', 'http://www.feijiu.net/ShuMaDianNJPJ/', 'http://www.feijiu.net/TongXinChanPinJPJ/', 'http://www.feijiu.net/YunDongXiuXYP/', 'http://www.feijiu.net/ChuanMeiGuangD/', 'http://www.feijiu.net/JiaJuYongPinJYDQ/', 'http://www.feijiu.net/YiYaoBaoY/', 'http://www.feijiu.net/YiQiYiBiao_/', 'http://www.feijiu.net/HuanBaoNengY/', 'http://www.feijiu.net/YeJinKuangChan/', 'http://www.feijiu.net/QiCheMoTuoCJPJ/', 'http://www.feijiu.net/EShouJiChuang/', 'http://www.feijiu.net/HeChengXiangJiao_/', 'http://www.feijiu.net/GongChengJiXie/', 'http://www.feijiu.net/WuJinGongJuJQPJ/', 'http://www.feijiu.net/TianRanXiangJiao_/', 'http://www.feijiu.net/XiangJiaoZhiPin/', 'http://www.feijiu.net/FeiJiuLunTai/', 'http://www.feijiu.net/XianLuBan/', 'http://www.feijiu.net/FeiJiuJiaDian/', 'http://www.feijiu.net/DianZiChanPin/', 'http://www.feijiu.net/EShouDianNao/', 'http://www.feijiu.net/HuaGongJingXHXP/', 'http://www.feijiu.net/GuangDianDianXinSB/', 'http://www.feijiu.net/DianNaoShuMCP/', 'http://www.feijiu.net/GongKongXiTongJZ/', 'http://www.feijiu.net/DianZiYuanQiJJZJ/', 'http://www.feijiu.net/DianLiSheBei_/', 'http://www.feijiu.net/YiQiYiB/', 'http://www.feijiu.net/JiaYongDianQi/', 'http://www.feijiu.net/XianShiSheBei/', 'http://www.feijiu.net/GaoYaDianQi_/', 'http://www.feijiu.net/DianYuanDianQi/', 'http://www.feijiu.net/JiChengDianLu_/', 'http://www.feijiu.net/DianZiCaiLiao/', 'http://www.feijiu.net/KaiGuan_/', 'http://www.feijiu.net/DianRongQi_/', 'http://www.feijiu.net/DuanLuQi_/', 'http://www.feijiu.net/TongXunChanPin_/', 'http://www.feijiu.net/DianChi_/', 'http://www.feijiu.net/KouJian/', 'http://www.feijiu.net/JiaZiGuan/', 'http://www.feijiu.net/JiaoShouJia/', 'http://www.feijiu.net/LuoWenGang/', 'http://www.feijiu.net/CaoGang/', 'http://www.feijiu.net/GangJin/', 'http://www.feijiu.net/GangMoBan/', 'http://www.feijiu.net/HXingGang/', 'http://www.feijiu.net/GuanCai/', 'http://www.feijiu.net/GangJieGou/', 'http://www.feijiu.net/CaiGangFangHDF/', 'http://www.feijiu.net/HuaGongSheBei/', 'http://www.feijiu.net/JieGouGang/', 'http://www.feijiu.net/MuFangFangM/', 'http://www.feijiu.net/JiuFuZhuangXieM/', 'http://www.feijiu.net/FeiJiuFuLiao/', 'http://www.feijiu.net/ShaXianS/', 'http://www.feijiu.net/ShengChanBianJiaoL/', 'http://www.feijiu.net/CanCiFuZhuangXM/', 'http://www.feijiu.net/FeiLiaoYuKuC/', 'http://www.feijiu.net/FuZhuang/', 'http://www.feijiu.net/FeiKaZhi/', 'http://www.feijiu.net/FuHeFeiZhi/', 'http://www.feijiu.net/FeiZhiBian/', 'http://www.feijiu.net/ZhiJiang_/', 'http://www.feijiu.net/FeiZhiXiang/', 'http://www.feijiu.net/BaoZhuangYongZhi_/', 'http://www.feijiu.net/MuZhiPinLei/', 'http://www.feijiu.net/ShengHuoYongZhi_/', 'http://www.feijiu.net/JinKouFeiZhi_/', 'http://www.feijiu.net/QiMinBoLi/', 'http://www.feijiu.net/YinShuaYongZhi/', 'http://www.feijiu.net/BanGongWenHYZ/']
time.sleep(1)
# print(start_url_list)

# pool = redis.ConnectionPool(host='192.168.1.241', port=6379)
pool = redis.ConnectionPool(host='192.168.1.249', port=6379)
# pool = redis.ConnectionPool(host='192.168.1.92', port=6379)
con = redis.Redis(connection_pool=pool)
c = con.client()
values = ["http://www.feijiu.net/FeiJinShu/", "http://www.feijiu.net/ErShouSheBei/",
          "http://www.feijiu.net/FeiDianZiDianQ/", "http://www.feijiu.net/FeiZhi/", "http://www.feijiu.net/KuCunWuZi/",
          "http://www.feijiu.net/FeiFangZhiPinYFPG/", "http://www.feijiu.net/JiuLunTaiYuXJ/",
          "http://www.feijiu.net/FeiBoLiYuMZP/", "http://www.feijiu.net/ErShouJianCai/"]
# c.lpush('feijiu:start_urls', *values)
c.lpush('crawl_feijiu:start_urls', *start_url_list)
con.close()
