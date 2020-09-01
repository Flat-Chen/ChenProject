#-*- coding: UTF-8 -*-
import re
import time
import pymysql
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


def parse_routine(caritemlist, item, domtext):

    caritemcontent = dict()
    for caritem in caritemlist:
        # parse解析
        caritemcontent[caritem['colname']] = parse(
            tag=caritem['tag'],
            mainstring=caritem['mainstring'],
            restring=caritem['restring'],
            redeal=caritem['redeal'],
            strip=caritem['strip'],
            formatstring=caritem['format'],
            formula=caritem['formula'],
            extractstring=caritem['extract'],
            lenstring=caritem['lenstring'],
            addstring=caritem['addstring'],
            formatbeforestring=caritem['format_before'],
            itemdata=item,
            domcontent=domtext,
        )
        # print(caritem['colname'], caritemcontent[caritem['colname']])
    return caritemcontent

def ILikeParse(caritemlist, item, domtext):
    length = len(caritemlist)
    versionnumber = length/103
    currentversion = 1
    i = (currentversion - 1) * 103
    j = currentversion * 103

    parsed_item=parse_routine(caritemlist[i:j],item,domtext)

    while(currentversion<=versionnumber):
        if keycolscheck(parsed_item):
            print('解析成功')
            print('xpath解析版本为：'+ str(currentversion))
            return parsed_item
        currentversion = currentversion + 1
        i = (currentversion - 1) * 103
        j = currentversion * 103
        print(str(currentversion) + ":version")
        parsed_item = parse_routine(caritemlist[i:j], item, domtext)

def keycolscheck(caritemcontent):
    keycols = ["shortdesc", "registerdate", "price1"]
    returncode = 1
    for keycol in keycols:
        if not (caritemcontent[keycol]):
            returncode = 0
            break
    return returncode


def parse(tag, mainstring, restring, redeal, strip, formatstring, formula, extractstring, lenstring, addstring,
          formatbeforestring, itemdata, domcontent):
    """解析方法"""

    # main parse
    if tag == "time":
        caritemdata = time.strftime(mainstring, time.localtime())

    elif tag == "item":
        caritemdata = itemdata[mainstring]

    elif tag == "value":
        caritemdata = mainstring

    elif tag == "text":
        caritemdata = domcontent.response.body

    elif tag == "xpath":
        xpathcontent = ""
        mainstring = eval("u'%s'" % mainstring)

        try:
            xpathcontent = domcontent.xpath(mainstring)
        except Exception as e:
            print(str(e) + mainstring)

        if xpathcontent:
            if extractstring == "alljoin":
                caritemdata = "/".join(xpathcontent.extract())
            else:
                caritemdata = xpathcontent.extract_first()
        else:
            caritemdata = None
    else:
        caritemdata = None

    # 正则提取及提取结果连接方式
    if restring and caritemdata:
        restring = eval("u'%s'" % restring)
        revalue = re.compile(restring).findall(caritemdata)
        if revalue:
            if not (redeal):
                caritemdata = revalue[0]
            elif redeal == ".join":
                caritemdata = ".".join(revalue)
            elif redeal == "-join":
                caritemdata = "-".join(revalue)
        else:
            caritemdata = None

    # strip
    if strip and caritemdata:
        caritemdata = caritemdata.strip()

    #　formula
    # format
    if caritemdata and formatstring and formatbeforestring:
        try:
            formatstring = eval("u'%s'" % formatstring)
            formatbeforestring = eval("u'%s'" % formatbeforestring)
            caritemdata = time.strftime(formatstring, time.strptime(caritemdata, formatbeforestring))
        except:
            caritemdata = caritemdata

    # addstring
    if caritemdata and addstring:
        addstring = eval("u'%s'" % addstring)
        caritemdata = caritemdata + addstring
    elif not (caritemdata) and addstring:
        addstring = eval("u'%s'" % addstring)
        caritemdata = addstring

    # len
    if caritemdata and len(caritemdata) >= int(lenstring):
        caritemdata = caritemdata[:int(lenstring)]

    return caritemdata


def Parse_conf(website):
    # mysql
    mysqldb = pymysql.connect(settings['MYSQLDB_SERVER'],
                              settings['MYSQLDB_USER'],
                              settings['MYSQLDB_PASS'],
                              settings['MYSQLDB_DB'],
                              port=settings['MYSQLDB_PORT'],
                              charset="utf8")

    mysqldbc = mysqldb.cursor()
    sql = "SELECT * FROM parse_conf where website='" + website + "'"
    caritemlist = []
    try:
        mysqldbc.execute(sql)
        results = mysqldbc.fetchall()
        # print(results)
        caritemlist = []
        for row in results:
            caritem = dict()
            caritem['ID'] = row[0]
            caritem['itemid'] = row[2]
            caritem['version'] = row[3]
            caritem['colname'] = row[4]
            caritem['tag'] = row[5]
            caritem['status'] = row[6]
            caritem['mainstring'] = row[7]
            caritem['restring'] = row[8]
            caritem['redeal'] = row[9]
            caritem['strip'] = row[10]
            caritem['format'] = row[11]
            caritem['formula'] = row[12]
            caritem['extract'] = row[13]
            caritem['lenstring'] = row[14]
            caritem['addstring'] = row[15]
            caritem['format_before'] = row[16]
            caritemlist.append(caritem)
    except:
        print("parse col error")
    mysqldb.close()
    return caritemlist
