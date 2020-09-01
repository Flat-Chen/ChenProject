# -*- coding: utf-8 -*-
import scrapy

from luntan.items import TouSuItem
from uuid import uuid4
# from scrapy.utils.project import get_project_settings

# settings = get_project_settings()

website = 'tousu'


class TousuSpider(scrapy.Spider):
    name = website
    allowed_domains = ['qctsw.com']
    # start_urls = ['http://qctsw.com/']
    count = 0
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_COLLECTION': 'tousu',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'luntan'
        # 'CONCURRENT_REQUESTS': 2
    }

    def start_requests(self):
        url = "http://www.qctsw.com/tousu/tsSearch/121_0_0_0_0_0,0,0,0,0,0_0.html"
        yield scrapy.Request(
            url=url
        )

    def parse(self, response):
        # item = TouSuItem()
        tr_list = response.xpath("//tr[@class='purple']")
        for tr in tr_list:
            item = TouSuItem()
            item["title"] = tr.xpath("./td[@class='tsTitle']/@title").get()
            # item["publish_time"] = tr.xpath("./td[4]/text()").get()
            item["url"] = "http://www.qctsw.com" + tr.xpath("./td[2]/a/@href").get()
            # item["issue"] = tr.xpath("./td[3]//a/text()").getall()
            issue = tr.xpath("./td[3]//a/text()").getall()
            item["issue"] = ",".join(issue)
            # item["brand"] = item["title"].split()[0].split("-")[0]
            # item["series"] = item["title"].split()[0].split("-")[1]
            # item["content"] = item["title"].split()[1]
            detail_url = tr.xpath("./td[@class='tsTitle']/a/@href").get()
            if detail_url:
                detail_url = "http://www.qctsw.com" + detail_url
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail_url,
                    meta={"item": item}
                )
            # print(item)
            # yield item

        next_url = response.xpath("//*[contains(text(),'下一页')]/@href").get()
        if next_url:
            next_url = "http://www.qctsw.com" + next_url
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_next_url
            )

    def parse_next_url(self, response):
        # item = TouSuItem()
        tr_list = response.xpath("//tr[@class='purple']")
        for tr in tr_list:
            item = TouSuItem()
            item["title"] = tr.xpath("./td[@class='tsTitle']/@title").get()
            # item["publish_time"] = tr.xpath("./td[4]/text()").get()
            item["url"] = "http://www.qctsw.com" + tr.xpath("./td[2]/a/@href").get()
            issue = tr.xpath("./td[3]//a/text()").getall()
            item["issue"] = ",".join(issue)
            detail_url = tr.xpath("./td[@class='tsTitle']/a/@href").get()
            if detail_url:
                detail_url = "http://www.qctsw.com" + detail_url
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail_url,
                    meta={"item": item}
                )
            # yield item

        next_url = response.xpath("//*[contains(text(),'下一页')]/@href").get()
        if next_url:
            next_url = "http://www.qctsw.com" + next_url
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_next_url
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//div[@class='articleContent']//p/text()").get().replace("\t", "").replace("\r","").replace("\n","")
        item["complainant"] = response.xpath("//div[@class='tableBox']/table//tr[2]/td[1]/text()").get().replace("\t", "").replace("\r","").replace("\n","")
        complaint_area = response.xpath("//div[@class='tableBox']/table//tr[4]/td[1]/a/text()").getall()
        item["complaint_area"] = ",".join(complaint_area)
        item["complaint_time"] = response.xpath("//div[@class='tableBox']/table//tr[3]/td[1]/text()").get().replace("\t", "").replace("\r","").replace("\n","")
        item["complaint_num"] = response.xpath("//div[@class='tableBox']/table//tr[1]/td[1]/b/text()").get()
        item["buy_time"] = response.xpath('//div[@class="tableBox"]/table//tr[7]/td[1]/text()').get()
        item["four_name"] = response.xpath('//div[@class="tableBox"]/table//tr[4]/td[2]/text()').get().replace("\t", "").replace("\r","").replace("\n","")
        item["four_phone"] = response.xpath('//div[@class="tableBox"]/table//tr[5]/td[2]/text()').get().replace("\t", "").replace("\r","").replace("\n","")
        appeal = response.xpath('//div[@class="tableBox"]/table//tr[6]/td[2]//a/text()').getall()
        item["appeal"] = ",".join(appeal)
        item["car_status"] = response.xpath("//div[@class='tableBox']/table//tr[5]/td[1]/a/text()").get()
        result = response.xpath("//div[@class='end']/p/text()").getall()
        item["result"] = "".join(result).replace("\t", "").replace("\r","").replace("\n","")
        item["result_publish_time"] = response.xpath("//div[@class='end']/span/i/text()").get()
        item["mileage"] = response.xpath("//div[@class='tableBox']/table//tr[6]/td[1]//text()").get()
        item["brand"] = response.xpath("//p[@class='fl']/a[1]//text()").get()
        item["series"] = response.xpath("//p[@class='fl']/a[2]//text()").get()
        item["_id"] = uuid4().__str__()
        # print(item)
        yield item



