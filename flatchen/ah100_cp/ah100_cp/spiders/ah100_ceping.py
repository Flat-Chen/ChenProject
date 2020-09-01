# -*- coding: utf-8 -*-
import json
import re
import time
import scrapy


class Ah100CepingSpider(scrapy.Spider):
    name = 'ah100_ceping'
    allowed_domains = ['https://www.autohome.com.cn/']
    start_urls = ['https://www.autohome.com.cn/bestauto/1']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Ah100CepingSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'ah100_cp',
        'MONGODB_COLLECTION': 'ah100_ceping',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        divs = response.xpath('//div[@class="row"]')
        next = response.xpath('//a[@class="page-item-next"]/@href').get()
        next_url = 'https://' + next

        for div in divs:
            # print(div)
            try:
                cp_url = div.xpath('.//span[@class="gray66 fn-fontsize14"]/a/@href').extract()[0]
                # print(cp_url)
                cp_url = re.sub(r'https:|//', '', cp_url)
                # print(cp_url)
                if 'ah100' in cp_url:
                    cp_url = 'https://' + cp_url
                    yield scrapy.Request(url=cp_url, callback=self.parse_modle, meta={"info": cp_url}, dont_filter=True)
                else:
                    # 排除非ah100测评
                    pass
            except:
                # 过滤空列表
                pass
        if next:
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_modle(self, response):
        cp_url = response.meta.get('info')
        vehicle = response.xpath('//a[@class="car-spec-name"]/text()').get()
        vehicle_url = response.xpath('//a[@class="car-spec-name"]/@href').get()
        vehicle_id = re.split(r'/', vehicle_url)[2]
        all_star = response.xpath('//span[@class="score-star star-orange"]/em/@style').extract()[0]
        all_star = re.split(r':', all_star)[1].lstrip()
        # print(vehicle, vehicle_id)

        view_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=1'
        yield scrapy.Request(url=view_url, callback=self.parse_view,
                             meta={"info": (cp_url, vehicle, vehicle_id, all_star)},
                             dont_filter=True)

    def parse_view(self, response):
        cp_url, vehicle, vehicle_id, all_star = response.meta.get('info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        view_rank = json_data['SpecScore']['Score'] / 10
        try:
            view_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            view_star = 0
        space_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=2'
        yield scrapy.Request(url=space_url, callback=self.parse_space,
                             meta={"info": (cp_url, vehicle, vehicle_id, all_star, view_rank, view_star)},
                             dont_filter=True)

    def parse_space(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star = response.meta.get('info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        space_rank = json_data['SpecScore']['Score'] / 10
        try:
            space_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            space_star = 0
        power_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=3'
        yield scrapy.Request(url=power_url, callback=self.parse_power,
                             meta={
                                 "info": (
                                     cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank,
                                     space_star)},
                             dont_filter=True)

    def parse_power(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star = response.meta.get('info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        power_rank = json_data['SpecScore']['Score'] / 10
        try:
            power_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            power_star = 0
        speed_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=4'
        yield scrapy.Request(url=speed_url, callback=self.parse_speed, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star)},
                             dont_filter=True)

    def parse_speed(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        speed_rank = json_data['SpecScore']['Score'] / 10
        try:
            speed_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            speed_star = 0
        oil_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=5'
        yield scrapy.Request(url=oil_url, callback=self.parse_oil, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star,
                speed_rank, speed_star)},
                             dont_filter=True)

    def parse_oil(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star, speed_rank, speed_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        oil_rank = json_data['SpecScore']['Score'] / 10
        try:
            oil_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            oil_star = 0
        brake_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=6'
        yield scrapy.Request(url=brake_url, callback=self.parse_brake, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star,
                speed_rank, speed_star, oil_rank, oil_star)}, dont_filter=True)

    def parse_brake(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star, speed_rank, speed_star, oil_rank, oil_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        brake_rank = json_data['SpecScore']['Score'] / 10
        try:
            brake_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            brake_star = 0
        feel_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=7'
        yield scrapy.Request(url=feel_url, callback=self.parse_feel, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star,
                speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star)}, dont_filter=True)

    def parse_feel(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star, speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        feel_rank = json_data['SpecScore']['Score'] / 10
        try:
            feel_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            feel_star = 0
        noise_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=8'
        yield scrapy.Request(url=noise_url, callback=self.parse_noise, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star,
                speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star)},
                             dont_filter=True)

    def parse_noise(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star, speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        noise_rank = json_data['SpecScore']['Score'] / 10
        try:
            noise_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            noise_star = 0
        cross_country_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=9'
        yield scrapy.Request(url=cross_country_url, callback=self.parse_cross_country, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star,
                speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star, noise_rank,
                noise_star)}, dont_filter=True)

    def parse_cross_country(self, response):
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star, speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star, noise_rank, noise_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        cross_country_rank = json_data['SpecScore']['Score'] / 10
        try:
            cross_country_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            cross_country_star = 0
        price_url = f'https://www.autohome.com.cn/ashx/article/AutoModelSpecScore.ashx?id={vehicle_id}&version=2&classid=10'
        yield scrapy.Request(url=price_url, callback=self.parse_price, meta={
            "info": (
                cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
                power_star, speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star,
                noise_rank,
                noise_star, cross_country_rank, cross_country_star)}, dont_filter=True)

    def parse_price(self, response):
        item = dict()
        cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank, power_star, speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star, noise_rank, noise_star, cross_country_rank, cross_country_star = response.meta.get(
            'info')
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        price_rank = json_data['SpecScore']['Score'] / 10
        try:
            price_star = str(json_data['SpecScore']['Score'] / json_data['SpecScore']['TotalScore'] * 100) + '%'
        except:
            price_star = 0
        # print(cp_url, vehicle, vehicle_id, all_star, view_rank, view_star, space_rank, space_star, power_rank,
        #       power_star,
        #       speed_rank, speed_star, oil_rank, oil_star, brake_rank, brake_star, feel_rank, feel_star, noise_rank,
        #       noise_star, cross_country_rank, cross_country_star, price_rank, price_star)
        item['vehicle'] = vehicle
        item['vehicle_id'] = vehicle_id
        item['all_star'] = all_star
        item['view_rank'] = view_rank
        item['view_star'] = view_star
        item['space_rank'] = space_rank
        item['space_star'] = space_star
        item['power_rank'] = power_rank
        item['power_star'] = power_star
        item['speed_rank'] = space_rank
        item['speed_star'] = space_star
        item['oil_rank'] = oil_rank
        item['oil_star'] = oil_star
        item['brake_rank'] = brake_rank
        item['brake_star'] = brake_star
        item['feel_rank'] = feel_rank
        item['feel_star'] = feel_star
        item['noise_rank'] = noise_rank
        item['noise_star'] = noise_star
        item['cross_country_rank'] = cross_country_rank
        item['cross_country_star'] = cross_country_star
        item['price_rank'] = price_rank
        item['price_star'] = price_star
        item['url'] = cp_url
        item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['status'] = cp_url + all_star
        yield item
