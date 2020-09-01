import re

import numpy

import pytesseract
from PIL import ImageDraw, Image, ImageFont
from fontTools.ttLib import TTFont


def fontConvert(fontPath):  # 将web下载的字体文件解析，返回其编码和汉字的对应关系
    font = TTFont(fontPath)  # 打开字体文件
    # print(font)
    map_dict = font["cmap"].getBestCmap()
    # print(map_dict)
    # print(font.getGlyphOrder())  # 列举出所有字体的uni码
    # print(len(font.getGlyphOrder()) ) # 列举出所有字体的uni码
    codeList = font.getGlyphOrder()[1:]
    im = Image.new("RGB", (1800, 1000), (255, 255, 255))  # 创建一张画布   第二个参数为大小  第三个为颜色
    # im.show()
    dr = ImageDraw.Draw(im)  # 把im 上面的内容画上去
    # print(dr)
    font = ImageFont.truetype(fontPath, 50)  # 加载一个字体文件 并创建一个字体对象 并指定字体大小
    # print(font)
    count = 1
    arrayList = numpy.array_split(codeList, count)  # 将列表切分成15份，以便于在图片上分行显示
    # print(arrayList)

    for t in range(count):
        n = [i for i in arrayList[t]]
        newList = [i.replace("uni", "\\u") for i in arrayList[t]]
        # print(n)
        # print(newList)
        text = "".join(newList)
        # print(text)
        text = text.encode('utf-8').decode('unicode_escape')
        # print(text)
        # print(type(text))
        # text =list(text)

        # dr.text((5, 55 * t), text, font=font, fill="#000000")    # 用来画图的代码
    # im.save("sss.jpg")
    # im = Image.open("sss.jpg")  # 可以将图片保存到本地，以便于手动打开图片查看

    # result = pytesseract.image_to_string(im, lang="chi_sim")
    # result = result.replace(" ", "").replace("\n", "")  # OCR识别出来的字符串有空格换行符
    # print(result)
    # codeList = [i.replace("uni", "&#x") + ";" for i in codeList]
    # print(len(list(text)))
    # with open("a.txt","w",encoding="utf-8")as f:
    #     f.write(str(dict(zip(codeList, list(text)))))


    yingshe_dict = dict(zip(codeList, list(text)))
    # print(yingshe_dict)
    finally_dict = {}
    for va, ke in map_dict.items():
        # va, ke = i.items()
        va = (hex(va) + ";").strip("0")
        va = va[1:]
        finally_dict.update({'&#x'+va: yingshe_dict[ke]})
        # finally_dict.update({'\\u' + va: yingshe_dict[ke]})
    return finally_dict


fontDict = fontConvert("yc-ft.woff")
print(fontDict)
