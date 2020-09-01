# -*- coding: utf-8 -*-
from copy import deepcopy

import scrapy
import re
from lxml import etree
import json
import demjson
import time
from koubei_new.items import YicheKoubeiItem
# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()

website ='yiche_koubei'


class YicheKoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['dianping.bitauto.com/']
    start_urls = ['http://dianping.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'public_opinion',
        'MYSQL_TABLE': 'yiche_koubei_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_COLLECTION': 'yiche_koubei_new',
        'MONGODB_DB': 'koubei',
        'CrawlCar_Num': 200000,
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 16,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, **kwargs):
        super(YicheKoubeiSpider, self).__init__(**kwargs)
        self.count = 0
        # self.font = settings["yiche_koubei_dic"]

    def start_requests(self):
        url = 'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=master'
        yield scrapy.Request(url=url)

    def parse(self, response):
        item = YicheKoubeiItem()
        data = demjson.decode(response.text)
        for i in data['DataList']:
            item["brand"] = i['name']
            # urlSpell = i['urlSpell']
            series_id = i['id']
            series_url = f'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=serial&pid={series_id}'
            # print(series_url)
            yield scrapy.Request(
                url=series_url,
                callback=self.parse_series_list,
                meta={"item": item}
            )

    def parse_series_list(self, response):
        item = response.meta["item"]
        data = demjson.decode(response.text)
        # print(data)
        for i in data:
            for c in i["child"]:
                # print(c["showName"])
                brand_id = c["id"]
                item['familyname'] = c["name"]
                # comment_list_url1 = f"http://dianping.bitauto.com/{urlSpell}/koubei/"
                item["usage"] = c["urlSpell"]
                # print(comment_list_url)
                page = 1
                pageSize = 1000
                comment_list_url = f'http://dianping.bitauto.com/web_app/api/v1/review/get_review_list?param=%7B%22cTagId%22%3A%22%22%2C%22tagId%22%3A%22-10%22%2C%22currentPage%22%3A{page}%2C%22serialId%22%3A%22{brand_id}%22%2C%22pageSize%22%3A{pageSize}%7D'
                # time.sleep(1)
                # print(comment_list_url)
                yield scrapy.Request(
                    url=comment_list_url,
                    callback=self.parse_comment_list,
                    meta={
                        "item": deepcopy(item),
                        "brand_id": brand_id,
                          }
                )

    def parse_comment_list(self, response):
        item = response.meta["item"]
        brand_id = response.meta["brand_id"]
        d = demjson.decode(response.text)

        if d["status"] == '1' and len(d["data"]) != 1:
            totle_num = len(d["data"]["list"])
            # print("*"*100)
            # print(totle_num)
            # print(response.url)
            pageSize = 10
            page_num = int(totle_num/pageSize) + 1
            # print(page_num)
            # print("*"*100)
            for page in range(1, page_num + 1):
                comment_list_url = f'http://dianping.bitauto.com/web_app/api/v1/review/get_review_list?param=%7B%22cTagId%22%3A%22%22%2C%22tagId%22%3A%22-10%22%2C%22currentPage%22%3A{page}%2C%22serialId%22%3A%22{brand_id}%22%2C%22pageSize%22%3A{pageSize}%7D'
                # print(comment_list_url)
                # print("*" * 100)
                self.count += 1
                yield scrapy.Request(
                    url=comment_list_url,
                    callback=self.parse_comment_next_page,
                    meta={"item": deepcopy(item)},
                    dont_filter=True
                )

    def parse_comment_next_page(self, response):
        item = response.meta["item"]
        d = demjson.decode(response.text)
        # print(response.url)
        print(self.count)
        if d["status"] == '1' and len(d["data"]) != 1:
            data = d["data"]["list"]
            for i in data:
                tiezi_id = i["id"]
                item["buyerid"] = i["userId"]
                item["buy_date"] = i["purchaseDate"]
                item["buy_pure_price"] = i["purchasePrice"]
                item["familynameid"] = i["serialId"]
                item["score"] = float(i["rating"]) / 2
                item["helpfulCount"] = i["postCount"]
                item["shortdesc"] = i["carName"]
                # item["comment_detail"] = i["content"].replace("\r", "").replace("\n", "")
                if i["user"]:
                    item["buyername"] = i["user"]["showname"]
                #     city_id = i["user"]["cityid"]
                # else:
                #     city_id = 0
                if i["fuelValue"]:
                    item["oil_consume"] = i["fuelValue"]+"L/100km"
                else:
                    item["oil_consume"] = '-'

                # detail_url = f'http://dianping.bitauto.com/sid_{item["familynameid"]}/koubei/{series_id}'
                detail_url = f"http://dianping.bitauto.com/{item['usage']}/koubei/{tiezi_id}"
                item["url"] = detail_url
                # print(detail_url)
                # city_url = f'http://cmsapi.bitauto.com/city/getcity.ashx?requesttype=json&bizCity=1&cityId={city_id}'
                # print(city_url)
                # print("*"*100)
                yield scrapy.Request(
                    url=item["url"],
                    callback=self.parse_detail_page,
                    meta={"item": deepcopy(item)},
                    dont_filter=True
                )

    def parse_detail_page(self, response):
        font_dic = self.settings.get("FONT_DIC")
        item = response.meta["item"]
        response_ = response.text
        # print(font_dic)
        # 替换字体
        for k, v in font_dic.items():
            # key_ = k.replace(';', '')
            if k in response_:
                response_ = response_.replace(k, str(v))
        html = etree.HTML(response_)
        content_list = html.xpath("//div[@class='tcid-info']//text()")
        content = ""
        for i in content_list:
            if '\r' in i:
                i = i.replace("\r", "")
            i = i.replace(" ", "").replace("\n", "")
            content += i
        # content = "".join(content_list)
        # print(content_list)
        # print(content)
        xjb = re.findall("#性价比(.*?)#", content)
        zmy = re.findall("#最满意(.*?)#", content)
        my = re.findall("#满意(.*?)#", content)
        zbmy = re.findall("#最不满意(.*?)#", content)
        bmy = re.findall("#不满意(.*?)#", content)
        kj = re.findall("#空间(.*?)#", content)
        wg = re.findall("#外观(.*?)#", content)
        ns = re.findall("#内饰(.*?)#", content)
        dl = re.findall("#动力(.*?)#", content)
        ck = re.findall("#操控(.*?)#", content)
        yh = re.findall("#油耗(.*?)#", content)
        ss = re.findall("#舒适性(.*?)#", content)

        if xjb:
            item["score_cost_compare"] = xjb[0]
            html.xpath("//div[@class='tcid-info']//text()")
        if zmy:
            item["satisfied"] = zmy[0]
        if my:
            item["satisfied"] = my[0]
        if zbmy:
            item["unsatisfied"] = zbmy[0]
        if bmy:
            item["unsatisfied"] = bmy[0]
        if kj:
            item["score_space_compare"] = kj[0]
            kj_star = html.xpath('//div[contains(text(),"空间")]//div[@class="start-icon active"]')
            item["score_space"] = len(kj_star) if len(kj_star) != 0 else None
        if wg:
            item["score_appearance_compare"] = wg[0]
            wg_star = html.xpath('//div[contains(text(),"外观")]//div[@class="start-icon active"]')
            item["score_appearance"] = len(wg_star) if len(wg_star) != 0 else None
        if ns:
            item["score_trim_compare"] = ns[0]
            ns_star = html.xpath('//div[contains(text(),"内饰")]//div[@class="start-icon active"]')
            item["score_trim"] = len(ns_star) if len(ns_star) != 0 else None
        if dl:
            item["score_power_compare"] = dl[0]
            dl_star = html.xpath('//div[contains(text(),"动力")]//div[@class="start-icon active"]')
            item["score_power"] = len(dl_star) if len(dl_star) != 0 else None
        if ck:
            item["score_control_compare"] = ck[0]
            ck_star = html.xpath('//div[contains(text(),"操控")]//div[@class="start-icon active"]')
            item["score_control"] = len(ck_star) if len(ck_star) != 0 else None
        if yh:
            item["score_fuel_compare"] = yh[0]
            yh_star = html.xpath('//div[contains(text(),"油耗")]//div[@class="start-icon active"]')
            item["score_fuel"] = len(yh_star) if len(yh_star) != 0 else None
        if ss:
            item["score_comfort_compare"] = ss[0]
            ss_star = html.xpath('//div[contains(text(),"舒适性")]//div[@class="start-icon active"]')
            item["score_comfort"] = len(ss_star) if len(ss_star) != 0 else None
        item["comment_detail"] = content.replace("\n", "")
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        buy_location = html.xpath("//div[@class='fd-bot']/div[@class='fd-txt']/text()")
        if len(buy_location) == 2:
            item["buy_location"] = buy_location[0]
        elif len(buy_location) == 1 and 'km' not in buy_location:
            item["buy_location"] = buy_location[0]
        else:
            item["buy_location"] = None
        item['spec_id'] = response.url[-6:]
        yield item

        # yield scrapy.Request(
        #     url=item["url"],
        #     callback=self.parse_city_page,
        #     meta={"item": deepcopy(item)},
        #     dont_filter=True
        # )
    #
    # def parse_city_page(self, response):
    #     item = response.meta["item"]
    #     # item["buy_location"] = response.xpath("/html/body/div[2]/div[1]/div[1]/div[5]/div[3]/div[2]/div/text()").get()
    #     if response.text:
    #         cityData = json.loads(response.text)
    #         item["buy_location"] = cityData[0]["cityName"]
    #     else:
    #         item["buy_location"] = None
    #
    #
    #     # yield item
    #     print(item)




