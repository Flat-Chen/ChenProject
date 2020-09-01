import re

import numpy

import pytesseract
from PIL import ImageDraw, Image, ImageFont
from fontTools.ttLib import TTFont
from functools import reduce
from lxml import etree
import requests
import os

# font = TTFont('./font/base.woff')
# font.saveXML('./font/base.xml')

import tempfile

def string_to_file(string):
    file_like_obj = tempfile.NamedTemporaryFile()
    file_like_obj.write(string)
    # 确保string立即写入文件
    file_like_obj.flush()
    # 将文件读取指针返回到文件开头位置
    file_like_obj.seek(0)
    return file_like_obj


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
# url = 'http://www.che300.com/partner/result.php?prov=11&city=11&brand=35&series=419&model=29947&registerDate=2008-12&mileAge=6&intention=0&partnerId=escsh&unit=1&sn=5d621b6dd35246eab6f104de6ae4cd88&sld=nj'
url = "https://www.che300.com/partner/result.php?prov=10&city=10&brand=14&series=221&model=2940&registerDate=2011-12&mileAge=17&intention=0&partnerId=douyin&unit=1&sn=3a0b24fad548603ae422daf5590609a8&sld=heb"
r = requests.get(url=url, headers=headers)
res = r.text

font1_url = re.findall('url\("(.*?)"\) format\("woff"\);', r.text, re.M)[0]
print(font1_url)

font1 = requests.get(font1_url, headers=headers)
# print(font1.content)
print(type(font1.content))
tmpe_file = string_to_file(font1.content)
print(tmpe_file)
print(type(tmpe_file))
# font = TTFont(tmpe_file)#读取woff文件
# with open("./font/new_base.woff", "wb")as f:
#     f.write(font1.content)

print(font1)
font = TTFont('./font/base.woff')#读取woff文件
num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '.']
list = font.getGlyphOrder()[2:]
print(list)
num_dict = dict(zip(list, num))
print(num_dict)
new_font_dict = dict()

font1 = TTFont(tmpe_file)
# font1 = TTFont('./font/new_base.woff')  # 读取新的woff文件
ff_list = font1.getGlyphNames()#返回一个对象
ff_news = font1.getGlyphOrder()
for fo in ff_news:
    fo2 = font1['glyf'][fo]
    for fff1 in list:
        fo3 = font['glyf'][fff1]
        if fo2 == fo3:
            new_font_dict[fo.replace("uni", "&#x").lower()] = num_dict[fff1]
k = [k for k in new_font_dict.keys()]
v = [v for v in new_font_dict.values()]


# r = reduce(lambda x, y: res.replace(x, y), new_font_dict)
# r = map(lambda x, y: print(x, y), new_font_dict)
print(new_font_dict)
for k, v in new_font_dict.items():
    res = res.replace(k, str(v))
#
print(list(r))
# print(res)



# # 创建font目录保存基准字体
# if not os.path.exists("font"):
#     font1 = requests.get(font1_url, headers=headers)
#     os.mkdir("font")
#     with open("./font/base.woff", "wb")as f:
#         f.write(font1.content)
# #
# base_font = TTFont('./font/base.woff')
# base_dict = []
# for i in range(len(base_font.getGlyphOrder()[2:])):
#     print(f"对应的数字{i + 1}:")
#     w = input()
#     base_dict.append({"code": base_font.getGlyphOrder()[2:][i], "num": w})
# print(base_dict)
# #
# # new_font_url = re.findall('url\("(.*?)"\) format\("woff"\);', r.text, re.M)[0]
# # font = requests.get(new_font_url, headers=headers)
# # with open("new_font.woff", "wb")as f:
# #     f.write(font.content)
# #
# # new_font = TTFont('new_font.woff')
# # new_font_code_list = new_font.getGlyphOrder()[2:]
# #
# # replace_dic=[]
# # for i in range(10):
# #     news = new_font['glyf'][new_font_code_list[i]]
# #     for j in range(10):
# #         bases = base_font['glyf'][base_dict[j]["code"]]
# #         if news == bases:
# #             unicode=new_font_code_list[i].lower().replace("uni", "&#x")+";"
# #             num = base_dict[j]["num"]
# #             replace_dic.append({"code":unicode, "num":num})
# #
# # org_data = r.text
# # for i in range(len(replace_dic)):
# #     new_data = org_data.replace(replace_dic[i]["code"],replace_dic[i]["num"])
# #
# # tree = etree.HTML(org_data)
# # dds = tree.xpath('//dl[@class="board-wrapper"]/dd')

