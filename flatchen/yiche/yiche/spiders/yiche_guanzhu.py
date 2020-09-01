import scrapy


class YicheGuanzhuSpider(scrapy.Spider):
    name = 'yiche_guanzhu'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://bitauto.com/']

    def parse(self, response):
        pass
