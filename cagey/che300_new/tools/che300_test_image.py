__author__ = 'cagey'
import io
import base64
import re
import requests
import pytesseract
from PIL import Image

url = 'https://www.che300.com/estimate/result/3/3/5/61/22053/2015-3/2/1/null/2017/2014?'
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Cookie": "pcim=8b7c7256db284e01a54442e53d1cb896d0ca6d7b",
}

res = requests.get(url=url, headers=headers)
print(res.text)

def decode_image(src):
    """
    解码图片
    :param src: 图片编码
        eg:
            src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    :return: str 保存到本地的文件名
    """
    # 1、信息提取
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")

    else:
        raise Exception("Do not parse!")

    # 2、base64解码
    img = base64.urlsafe_b64decode(data)
    image = Image.open(io.BytesIO(img))
    img_str = pytesseract.image_to_string(image)
    return img_str

if __name__ == '__main__':
    src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAASBAMAAAAUH7VWAAAAElBMVEX///8AAAAAAAAAAAAAAAAAAABknMCaAAAAgUlEQVQokc2Quw3AIAxEjwR6vAFigkgsQMEANOy/SjAhHwLUyQkhLE7PZwMfiEgD1tYqBCCl2FqEBmExiymV9NKriNSRhM6UAxTKgYpvD/HVeDoO58HdiwN1mMK5Mvshh2NXTG03yJM9J0YOPXV2frrp7LxDm4XVbZMdPuSmPz/RDvkADrGDaTi/AAAAAElFTkSuQmCC'
    # 解码测试
    price = decode_image(src)
    print(price)



