import scrapy


class BiyeSpider(scrapy.Spider):
    name = 'biye'
    allowed_domains = ['edu.cn']
    # start_urls = ['http://edu.cn/']

    def start_requests(self):
        for ji in range(14, 17):
            for yuan in range(1, 10):
                for zhuanye in range(1, 10):
                    for ban in range(1, 9):
                        for xuehao in range(1, 60):
                            xuehao = '0'+str(xuehao) if xuehao < 10 else xuehao
                            # xh = str(ji) + '0' + str(yuan) + '0' + str(zhuanye)+'0' + str(ban) + str(xuehao)
                            # print(xh)
                            xh = '1608040102'
                            url = 'http://211.70.176.123/jwyy/zdzm/1.asp'
                            data = {
                                'xh': xh,
                                'b1': '%B2%E9%D1%AF'
                            }
                            yield scrapy.FormRequest(url=url,formdata=data,meta={'xh': xh})


    def parse(self, response):
        if '学号不正确，或者你不是当年毕业生！' in response.text:
            pass
        else:
            p = response.xpath('//tr//text()').getall()
            srt1 = str()
            for i in p:
                print(i)
                str1 = srt1 + i.strip()
            print(srt1)
            # print(p)
            data = ' '.join(response.xpath('//tr//text()').getall()).replace(' ', '').replace('\n', '').replace('\r', '').replace(' ','')
            # print(data)
