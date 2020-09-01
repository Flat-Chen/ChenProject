__author__ = 'cagey'
import requests

headers = {
    'Referer': 'https://bbs.pcauto.com.cn',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    # "Cookie": "visitedfid=17957D20685D22418D20697D23985D23585D17913D17608D17504D17329",
}

url = "https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/bbs/forums.xsp?forumId=15281&pageNo=786&pageSize=20"

res = requests.get(url=url, headers=headers)

print(res.text)


