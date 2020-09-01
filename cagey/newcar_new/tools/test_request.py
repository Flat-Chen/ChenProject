__author__ = 'cagey'
import requests
# url = "https://bbs.pcauto.com.cn/topic-13756756.html"
url = "http://bbs.pcauto.com.cn/intf/topic/counter.ajax?tid=17875295"


res = requests.get(url=url)
print(res.text)
print(res.status_code)










