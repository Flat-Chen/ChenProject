#-*- coding: UTF-8 -*-
import re
import time
import scrapy
import pymysql
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

def parse_routine(item_list, item):
    caritemcontent = dict()
    for caritem in item_list:
        # parse解析
        caritemcontent[caritem['colname']] = parse(caritem, item)
        # print(caritem['colname'], caritemcontent[caritem['colname']])
    return caritemcontent

def parse_text(website, item):
    item_list = parse_conf(website)
    parsed_item=parse_routine(item_list, item)

    if key_cols_check(parsed_item):
        print('解析成功')
        return parsed_item

def key_cols_check(caritemcontent):
    keycols = ["shortdesc", "registerdate"]
    returncode = 1
    for keycol in keycols:
        if not (caritemcontent[keycol]):
            returncode = 0
            break
    return returncode


def parse(caritem, item):
    """解析方法"""
    col = caritem['colname']
    tag = caritem['tag']
    mainstring = caritem['mainstring']
    restring = caritem['restring']
    strip = caritem['strip']

    html = scrapy.selector.Selector(text=item["datasave"])
    caritemdata = None

    if tag == "time":
        caritemdata = time.strftime(mainstring, time.localtime())

    elif tag == "item":
        caritemdata = item[mainstring]

    elif tag == "value":
        caritemdata = mainstring

    elif tag == "xpath":
        mainstring = eval("u'%s'" % mainstring)

        try:
            caritemdata = html.xpath(mainstring).extract_first()
        except Exception as e:
            print(str(e))
            print(col, ' xpath: ', mainstring)

    # 正则提取及提取结果连接方式
    if restring and caritemdata:
        restring = eval("u'%s'" % restring)
        try:
            caritemdata = re.findall(restring, caritemdata)[0]
        except Exception as e:
            print(str(e))
            print(col, ' restring: ', restring, caritemdata)

    # strip
    if strip and caritemdata:
        caritemdata = caritemdata.strip()

    return caritemdata

def parse_conf(website):
    conn = pymysql.connect(settings['MYSQLDB_SERVER'],
                              settings['MYSQLDB_USER'],
                              settings['MYSQLDB_PASS'],
                              'usedcar_update',
                              port=settings['MYSQLDB_PORT'],
                              charset="utf8")

    cs = conn.cursor()
    sql = 'select colname, tag, mainstring, restring, strip from parse_conf_20190527 where website="{}"'.format(website)
    cs.execute(sql)
    results = cs.fetchall()

    item_list = []
    for row in results:
        caritem = dict()
        caritem['colname'] = row[0]
        caritem['tag'] = row[1]
        caritem['mainstring'] = row[2]
        caritem['restring'] = row[3]
        caritem['strip'] = row[4]
        item_list.append(caritem)

    cs.close()
    conn.close()
    return item_list