# -*- coding: utf-8 -*-
import scrapy
from ganji.items import HaicjItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random

website='haicj_a'

class CarSpider(scrapy.Spider):
    name=website

    def __init__(self,**kwargs):
        #args
        super(CarSpider,self).__init__(**kwargs)

        #problem report
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=160000
        #mongo
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','newcar',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        cars=[]
        for i in range(1,self.carnum):
            url='http://www.haicj.com/carinfo.jsp?lyid='+str(i)+'&typeid=1'
            car=scrapy.Request(url,callback=self.parse)
            cars.append(car)
        return cars

    def parse(self,response):
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        item=HaicjItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        # item['datasave'] = response.xpath('//html').extract_first()
        item['family_name']=response.xpath('//title/text()').re('(.*)\(')[0] \
            if response.xpath('//title/text()').re('(.*)\(') else "-"
        item['factoryname'] = response.xpath('//td[@id="cjmc"]/text()').extract_first() \
            if response.xpath('//td[@id="cjmc"]/text()').extract_first() else "-"
        item['salesdesc'] = response.xpath('//div[@class="header"]/i/text()').extract_first() \
            if response.xpath('//div[@class="header"]/i/text()').extract_first() else "-"
        item['makeyear'] = response.xpath('//td[@id="nk"]/text()').extract_first() \
            if response.xpath('//td[@id="nk"]/text()').extract_first() else "-"
        item['level'] = response.xpath('//td[@id="cljb"]/text()').extract_first() \
            if response.xpath('//td[@id="cljb"]/text()').extract_first() else "-"
        item['price'] = response.xpath('//td[@id="zdjg"]/text()').extract_first() \
            if response.xpath('//td[@id="zdjg"]/text()').extract_first() else "-"
        item['bodystyle'] = response.xpath('//td[@id="csxs"]/text()').extract_first() \
            if response.xpath('//td[@id="csxs"]/text()').extract_first() else "-"
        item['masspeed'] = response.xpath('//td[@id="zgsj"]/text()').extract_first() \
            if response.xpath('//td[@id="zgsj"]/text()').extract_first() else "-"
        item['accelerate'] = response.xpath('//td[@id="jss"]/text()').extract_first() \
            if response.xpath('//td[@id="jss"]/text()').extract_first() else "-"
        item['petrol'] = response.xpath('//td[@id="zhgkyh"]/text()').extract_first() \
            if response.xpath('//td[@id="zhgkyh"]/text()').extract_first() else "-"
        item['city_oil_consumption'] = response.xpath('//td[@id="sqgkyh"]/text()').extract_first() \
            if response.xpath('//td[@id="sqgkyh"]/text()').extract_first() else "-"
        item['suburb_oil_consumption'] = response.xpath('//td[@id="sjgkyh"]/text()').extract_first() \
            if response.xpath('//td[@id="sjgkyh"]/text()').extract_first() else "-"
        item['lenth_width_heigh'] = response.xpath('//td[@id="cd_kd_gd"]/text()').extract_first() \
            if response.xpath('//td[@id="cd_kd_gd"]/text()').extract_first() else "-"
        item['wheelbase'] = response.xpath('//td[@id="zj"]/text()').extract_first() \
            if response.xpath('//td[@id="zj"]/text()').extract_first() else "-"
        item['front_back_gauge'] = response.xpath('//td[@id="qlj_hlj"]/text()').extract_first() \
            if response.xpath('//td[@id="qlj_hlj"]/text()').extract_first() else "-"
        item['min_ground_distance'] = response.xpath('//td[@id="zxldjx"]/text()').extract_first() \
            if response.xpath('//td[@id="zxldjx"]/text()').extract_first() else "-"
        item['weigth_and_all_weight'] = response.xpath('//td[@id="zbzl_zzl"]/text()').extract_first() \
            if response.xpath('//td[@id="zbzl_zzl"]/text()').extract_first() else "-"
        item['doors'] = response.xpath('//td[@id="cms"]/text()').extract_first() \
            if response.xpath('//td[@id="cms"]/text()').extract_first() else "-"
        item['seats'] = response.xpath('//td[@id="zws"]/text()').extract_first() \
            if response.xpath('//td[@id="zws"]/text()').extract_first() else "-"
        item['fulevolumn'] = response.xpath('//td[@id="yxrj"]/text()').extract_first() \
            if response.xpath('//td[@id="yxrj"]/text()').extract_first() else "-"
        item['baggage'] = response.xpath('//td[@id="xlxrj"]/text()').extract_first() \
            if response.xpath('//td[@id="xlxrj"]/text()').extract_first() else "-"
        item['engine_type'] = response.xpath('//td[@id="fdjxh"]/text()').extract_first() \
            if response.xpath('//td[@id="fdjxh"]/text()').extract_first() else "-"
        item['output'] = response.xpath('//td[@id="pl"]/text()').extract_first() \
            if response.xpath('//td[@id="pl"]/text()').extract_first() else "-"
        item['cylinder_volume'] = response.xpath('//td[@id="qgrj"]/text()').extract_first() \
            if response.xpath('//td[@id="qgrj"]/text()').extract_first() else "-"
        item['method'] = response.xpath('//td[@id="jqxs"]/text()').extract_first() \
            if response.xpath('//td[@id="jqxs"]/text()').extract_first() else "-"
        item['lwv'] = response.xpath('//td[@id="qgxs"]/text()').extract_first() \
            if response.xpath('//td[@id="qgxs"]/text()').extract_first() else "-"
        item['lwvnumber'] = response.xpath('//td[@id="fdjgs"]/text()').extract_first() \
            if response.xpath('//td[@id="fdjgs"]/text()').extract_first() else "-"
        item['valve'] = response.xpath('//td[@id="qms"]/text()').extract_first() \
            if response.xpath('//td[@id="qms"]/text()').extract_first() else "-"
        item['compress'] = response.xpath('//td[@id="ysb"]/text()').extract_first() \
            if response.xpath('//td[@id="ysb"]/text()').extract_first() else "-"
        item['maxps'] = response.xpath('//td[@id="zdml"]/text()').extract_first() \
            if response.xpath('//td[@id="zdml"]/text()').extract_first() else "-"
        item['maxpower'] = response.xpath('//td[@id="gl"]/text()').extract_first() \
            if response.xpath('//td[@id="gl"]/text()').extract_first() else "-"
        item['maxrpm'] = response.xpath('//td[@id="glzs"]/text()').extract_first() \
            if response.xpath('//td[@id="glzs"]/text()').extract_first() else "-"
        item['maxnm'] = response.xpath('//td[@id="nj"]/text()').extract_first() \
            if response.xpath('//td[@id="nj"]/text()').extract_first() else "-"
        item['maxtorque'] = response.xpath('//td[@id="njzs"]/text()').extract_first() \
            if response.xpath('//td[@id="njzs"]/text()').extract_first() else "-"
        item['engine_technology'] = response.xpath('//td[@id="fdjtyjs"]/text()').extract_first() \
            if response.xpath('//td[@id="fdjtyjs"]/text()').extract_first() else "-"
        item['fueltype'] = response.xpath('//td[@id="rylx"]/text()').extract_first() \
            if response.xpath('//td[@id="rylx"]/text()').extract_first() else "-"
        item['fuelnumber'] = response.xpath('//td[@id="rybh"]/text()').extract_first() \
            if response.xpath('//td[@id="rybh"]/text()').extract_first() else "-"
        item['fuelmethod'] = response.xpath('//td[@id="gyfs"]/text()').extract_first() \
            if response.xpath('//td[@id="gyfs"]/text()').extract_first() else "-"
        item['engine_position'] = response.xpath('//td[@id="fdjwz"]/text()').extract_first() \
            if response.xpath('//td[@id="fdjwz"]/text()').extract_first() else "-"
        item['emission'] = response.xpath('//td[@id="pfbz"]/text()').extract_first() \
            if response.xpath('//td[@id="pfbz"]/text()').extract_first() else "-"
        item['gearnumber'] = response.xpath('//td[@id="dws"]/text()').extract_first() \
            if response.xpath('//td[@id="dws"]/text()').extract_first() else "-"
        item['geartype'] = response.xpath('//td[@id="bsqlx"]/text()').extract_first() \
            if response.xpath('//td[@id="bsqlx"]/text()').extract_first() else "-"
        item['geardesc'] = response.xpath('//td[@id="bsqms"]/text()').extract_first() \
            if response.xpath('//td[@id="bsqms"]/text()').extract_first() else "-"
        item['steering_resistance_type'] = response.xpath('//td[@id="zszllx"]/text()').extract_first() \
            if response.xpath('//td[@id="zszllx"]/text()').extract_first() else "-"
        item['driveway'] = response.xpath('//td[@id="qdfs"]/text()').extract_first() \
            if response.xpath('//td[@id="qdfs"]/text()').extract_first() else "-"
        item['fronthang'] = response.xpath('//td[@id="qxgxt"]/text()').extract_first() \
            if response.xpath('//td[@id="qxgxt"]/text()').extract_first() else "-"
        item['backhang'] = response.xpath('//td[@id="hxgxt"]/text()').extract_first() \
            if response.xpath('//td[@id="hxgxt"]/text()').extract_first() else "-"
        item['frontbrake'] = response.xpath('//td[@id="qzdlx"]/text()').extract_first() \
            if response.xpath('//td[@id="qzdlx"]/text()').extract_first() else "-"
        item['backbrake'] = response.xpath('//td[@id="hzdlx"]/text()').extract_first() \
            if response.xpath('//td[@id="hzdlx"]/text()').extract_first() else "-"
        item['frontwheel'] = response.xpath('//td[@id="qltgg"]/text()').extract_first() \
            if response.xpath('//td[@id="qltgg"]/text()').extract_first() else "-"
        item['backwheel'] = response.xpath('//td[@id="hltgg"]/text()').extract_first() \
            if response.xpath('//td[@id="hltgg"]/text()').extract_first() else "-"
        item['driver_codrive_airbag_major'] = response.xpath('//td[@id="cb"]/text()').extract_first() \
            if response.xpath('//td[@id="cb"]/text()').extract_first() else "-"
        item['driver_codrive_airbag_minor'] = response.xpath('//td[@id="cc"]/text()').extract_first() \
            if response.xpath('//td[@id="cc"]/text()').extract_first() else "-"
        item['front_side_airbag'] = response.xpath('//td[@id="cd"]/text()').extract_first() \
            if response.xpath('//td[@id="cd"]/text()').extract_first() else "-"
        item['back_side_airbag'] = response.xpath('//td[@id="ce"]/text()').extract_first() \
            if response.xpath('//td[@id="ce"]/text()').extract_first() else "-"
        item['front_head_airbag'] = response.xpath('//td[@id="cf"]/text()').extract_first() \
            if response.xpath('//td[@id="cf"]/text()').extract_first() else "-"
        item['back_head_airbag'] = response.xpath('//td[@id="cg"]/text()').extract_first() \
            if response.xpath('//td[@id="cg"]/text()').extract_first() else "-"
        item['knee_airbag'] = response.xpath('//td[@id="ch"]/text()').extract_first() \
            if response.xpath('//td[@id="ch"]/text()').extract_first() else "-"
        item['tire_pressure_monitoring'] = response.xpath('//td[@id="ci"]/text()').extract_first() \
            if response.xpath('//td[@id="ci"]/text()').extract_first() else "-"
        item['zero_tire_pressure'] = response.xpath('//td[@id="ck"]/../td/text()').extract_first() \
            if response.xpath('//td[@id="ck"]/../td/text()').extract_first() else "-"
        item['safety_belt_is_not_prompt'] = response.xpath('//td[@id="ck"]/text()').extract_first() \
            if response.xpath('//td[@id="ck"]/text()').extract_first() else "-"
        item['isofix_child_seat_interface'] = response.xpath('//td[@id="cl"]/text()').extract_first() \
            if response.xpath('//td[@id="cl"]/text()').extract_first() else "-"
        item['latch_seat_interface'] = response.xpath('//td[@id="cm"]/text()').extract_first() \
            if response.xpath('//td[@id="cm"]/text()').extract_first() else "-"
        item['engine_electronic_control_unit'] = response.xpath('//td[@id="cn"]/text()').extract_first() \
            if response.xpath('//td[@id="cn"]/text()').extract_first() else "-"
        item['central_lock'] = response.xpath('//td[@id="co"]/text()').extract_first() \
            if response.xpath('//td[@id="co"]/text()').extract_first() else "-"
        item['remote_control_key'] = response.xpath('//td[@id="cp"]/text()').extract_first() \
            if response.xpath('//td[@id="cp"]/text()').extract_first() else "-"
        item['keyless_start_system'] = response.xpath('//td[@id="cq"]/text()').extract_first() \
            if response.xpath('//td[@id="cq"]/text()').extract_first() else "-"
        item['abs_antilock'] = response.xpath('//td[@id="cr"]/text()').extract_first() \
            if response.xpath('//td[@id="cr"]/text()').extract_first() else "-"
        item['braking_force_distribution_ebd_cbc'] = response.xpath('//td[@id="cs"]/text()').extract_first() \
            if response.xpath('//td[@id="cs"]/text()').extract_first() else "-"
        item['brake_assist_eba_bas_ba'] = response.xpath('//td[@id="ct"]/text()').extract_first() \
            if response.xpath('//td[@id="ct"]/text()').extract_first() else "-"
        item['traction_control_system_asr_tcs_trc'] = response.xpath('//td[@id="cu"]/text()').extract_first() \
            if response.xpath('//td[@id="cu"]/text()').extract_first() else "-"
        item['vehicle_stability_control_esp_dsc_vsc'] = response.xpath('//td[@id="cv"]/text()').extract_first() \
            if response.xpath('//td[@id="cv"]/text()').extract_first() else "-"
        item['hill_start_assist_and_auto_parking'] = response.xpath('//td[@id="cw"]/text()').extract_first() \
            if response.xpath('//td[@id="cw"]/text()').extract_first() else "-"
        item['hill_descent_control'] = response.xpath('//td[@id="cx"]/text()').extract_first() \
            if response.xpath('//td[@id="cx"]/text()').extract_first() else "-"
        item['variable_suspension'] = response.xpath('//td[@id="cy"]/text()').extract_first() \
            if response.xpath('//td[@id="cy"]/text()').extract_first() else "-"
        item['aimatic'] = response.xpath('//td[@id="cz"]/text()').extract_first() \
            if response.xpath('//td[@id="cz"]/text()').extract_first() else "-"
        item['variable_gear_steering_ratio'] = response.xpath('//td[@id="da"]/text()').extract_first() \
            if response.xpath('//td[@id="da"]/text()').extract_first() else "-"
        item['active_steering_system'] = response.xpath('//td[@id="dd"]/text()').extract_first() \
            if response.xpath('//td[@id="dd"]/text()').extract_first() else "-"
        item['electric_sunroof'] = response.xpath('//td[@id="em"]/text()').extract_first() \
            if response.xpath('//td[@id="em"]/text()').extract_first() else "-"
        item['panoramic_sunroof'] = response.xpath('//td[@id="en"]/text()').extract_first() \
            if response.xpath('//td[@id="en"]/text()').extract_first() else "-"
        item['sport_appearance_suite'] = response.xpath('//td[@id="ek"]/text()').extract_first() \
            if response.xpath('//td[@id="ek"]/text()').extract_first() else "-"
        item['electric_door'] = response.xpath('//td[@id="el"]/text()').extract_first() \
            if response.xpath('//td[@id="el"]/text()').extract_first() else "-"
        item['electric_trunk'] = response.xpath('//td[@id="ej"]/text()').extract_first() \
            if response.xpath('//td[@id="ej"]/text()').extract_first() else "-"
        item['leather_steering_wheel'] = response.xpath('//td[@id="de"]/text()').extract_first() \
            if response.xpath('//td[@id="de"]/text()').extract_first() else "-"
        item['steering_up_and_down'] = response.xpath('//td[@id="df"]/text()').extract_first() \
            if response.xpath('//td[@id="df"]/text()').extract_first() else "-"
        item['steering_front_and_back'] = response.xpath('//td[@id="dg"]/text()').extract_first() \
            if response.xpath('//td[@id="dg"]/text()').extract_first() else "-"
        item['steering_wheel_electric_adjustment'] = response.xpath('//td[@id="dh"]/text()').extract_first() \
            if response.xpath('//td[@id="dh"]/text()').extract_first() else "-"
        item['multi_function_steering_wheel'] = response.xpath('//td[@id="di"]/text()').extract_first() \
            if response.xpath('//td[@id="di"]/text()').extract_first() else "-"
        item['steering_wheel_shift'] = response.xpath('//td[@id="dj"]/text()').extract_first() \
            if response.xpath('//td[@id="dj"]/text()').extract_first() else "-"
        item['cruise_control'] = response.xpath('//td[@id="fh"]/text()').extract_first() \
            if response.xpath('//td[@id="fh"]/text()').extract_first() else "-"
        item['parking_assistance'] = response.xpath('//td[@id="fl"]/text()').extract_first() \
            if response.xpath('//td[@id="fl"]/text()').extract_first() else "-"
        item['rear_video_monitor'] = response.xpath('//td[@id="fj"]/text()').extract_first() \
            if response.xpath('//td[@id="fj"]/text()').extract_first() else "-"
        item['computer_screen_of_driving'] = response.xpath('//td[@id="fk"]/text()').extract_first() \
            if response.xpath('//td[@id="fk"]/text()').extract_first() else "-"
        item['heads_up_display'] = response.xpath('//td[@id="fl"]/text()').extract_first() \
            if response.xpath('//td[@id="fl"]/text()').extract_first() else "-"
        item['abls'] = response.xpath('//td[@id="dc"]/text()').extract_first() \
            if response.xpath('//td[@id="dc"]/text()').extract_first() else "-"
        item['doubling_asisst'] = response.xpath('//td[@id="db"]/text()').extract_first() \
            if response.xpath('//td[@id="db"]/text()').extract_first() else "-"
        item['leather_seat'] = response.xpath('//td[@id="dk"]/text()').extract_first() \
            if response.xpath('//td[@id="dk"]/text()').extract_first() else "-"
        item['sports_seats'] = response.xpath('//td[@id="dl"]/text()').extract_first() \
            if response.xpath('//td[@id="dl"]/text()').extract_first() else "-"
        item['adjustable_seat_height'] = response.xpath('//td[@id="dm"]/text()').extract_first() \
            if response.xpath('//td[@id="dm"]/text()').extract_first() else "-"
        item['adjustable_lumbar_support'] = response.xpath('//td[@id="dn"]/text()').extract_first() \
            if response.xpath('//td[@id="dn"]/text()').extract_first() else "-"
        item['adjustable_shoulder_support'] = response.xpath('//td[@id="do"]/text()').extract_first() \
            if response.xpath('//td[@id="do"]/text()').extract_first() else "-"
        item['seat_electric_adjustment_major'] = response.xpath('//td[@id="dp"]/text()').extract_first() \
            if response.xpath('//td[@id="dp"]/text()').extract_first() else "-"
        item['seat_electric_adjustment_minor'] = response.xpath('//td[@id="dq"]/text()').extract_first() \
            if response.xpath('//td[@id="dq"]/text()').extract_first() else "-"
        item['adjustable_rear_row_backrest_angle_'] = response.xpath('//td[@id="dr"]/text()').extract_first() \
            if response.xpath('//td[@id="dr"]/text()').extract_first() else "-"
        item['rear_row_seat_movement'] = response.xpath('//td[@id="ds"]/text()').extract_first() \
            if response.xpath('//td[@id="ds"]/text()').extract_first() else "-"
        item['rear_seat_electric_adjustment'] = response.xpath('//td[@id="dt"]/text()').extract_first() \
            if response.xpath('//td[@id="dt"]/text()').extract_first() else "-"
        item['electric_chair_memory'] = response.xpath('//td[@id="du"]/text()').extract_first() \
            if response.xpath('//td[@id="du"]/text()').extract_first() else "-"
        item['front_seat_heating'] = response.xpath('//td[@id="dv"]/text()').extract_first() \
            if response.xpath('//td[@id="dv"]/text()').extract_first() else "-"
        item['back_seat_heating'] = response.xpath('//td[@id="dw"]/text()').extract_first() \
            if response.xpath('//td[@id="dw"]/text()').extract_first() else "-"
        item['seat_ventilation'] = response.xpath('//td[@id="dx"]/text()').extract_first() \
            if response.xpath('//td[@id="dx"]/text()').extract_first() else "-"
        item['massage_seat'] = response.xpath('//td[@id="dy"]/text()').extract_first() \
            if response.xpath('//td[@id="dy"]/text()').extract_first() else "-"
        item['third_row_seats'] = response.xpath('//td[@id="eb"]/text()').extract_first() \
            if response.xpath('//td[@id="eb"]/text()').extract_first() else "-"
        item['rear_seat_down'] = response.xpath('//td[@id="dz"]/text()').extract_first() \
            if response.xpath('//td[@id="dz"]/text()').extract_first() else "-"
        item['rear_seat_proportion_down'] = response.xpath('//td[@id="ea"]/text()').extract_first() \
            if response.xpath('//td[@id="ea"]/text()').extract_first() else "-"
        item['front_seat_armrest'] = response.xpath('//td[@id="ec"]/text()').extract_first() \
            if response.xpath('//td[@id="ec"]/text()').extract_first() else "-"
        item['back_seat_armrest'] = response.xpath('//td[@id="ed"]/text()').extract_first() \
            if response.xpath('//td[@id="ed"]/text()').extract_first() else "-"
        item['rear_row_hang_cup'] = response.xpath('//td[@id="ee"]/text()').extract_first() \
            if response.xpath('//td[@id="ee"]/text()').extract_first() else "-"
        item['gps_navigation'] = response.xpath('//td[@id="fm"]/text()').extract_first() \
            if response.xpath('//td[@id="fm"]/text()').extract_first() else "-"
        item['interactive_location_services'] = response.xpath('//td[@id="fn"]/text()').extract_first() \
            if response.xpath('//td[@id="fn"]/text()').extract_first() else "-"
        item['color_screen_display_control'] = response.xpath('//td[@id="fo"]/text()').extract_first() \
            if response.xpath('//td[@id="fo"]/text()').extract_first() else "-"
        item['human_computer_interaction_system'] = response.xpath('//td[@id="fp"]/text()').extract_first() \
            if response.xpath('//td[@id="fp"]/text()').extract_first() else "-"
        item['built_in_hard_disk'] = response.xpath('//td[@id="fq"]/text()').extract_first() \
            if response.xpath('//td[@id="fq"]/text()').extract_first() else "-"
        item['bluetooth_car_phone'] = response.xpath('//td[@id="fr"]/text()').extract_first() \
            if response.xpath('//td[@id="fr"]/text()').extract_first() else "-"
        item['onboard_tv'] = response.xpath('//td[@id="fs"]/text()').extract_first() \
            if response.xpath('//td[@id="fs"]/text()').extract_first() else "-"
        item['rear_lcd_screen'] = response.xpath('//td[@id="ft"]/text()').extract_first() \
            if response.xpath('//td[@id="ft"]/text()').extract_first() else "-"
        item['external_audio_source_connectors'] = response.xpath('//td[@id="fu"]/text()').extract_first() \
            if response.xpath('//td[@id="fu"]/text()').extract_first() else "-"
        item['mp3_audio_support'] = response.xpath('//td[@id="fv"]/text()').extract_first() \
            if response.xpath('//td[@id="fv"]/text()').extract_first() else "-"
        item['single_cd_player'] = response.xpath('//td[@id="fw"]/text()').extract_first() \
            if response.xpath('//td[@id="fw"]/text()').extract_first() else "-"
        item['multi_cd_player'] = response.xpath('//td[@id="fx"]/text()').extract_first() \
            if response.xpath('//td[@id="fx"]/text()').extract_first() else "-"
        item['virtual_multi_cd_player'] = response.xpath('//td[@id="fy"]/text()').extract_first() \
            if response.xpath('//td[@id="fy"]/text()').extract_first() else "-"
        item['single_dvd_player'] = response.xpath('//td[@id="fz"]/text()').extract_first() \
            if response.xpath('//td[@id="fz"]/text()').extract_first() else "-"
        item['multi_dvd_player'] = response.xpath('//td[@id="ga"]/text()').extract_first() \
            if response.xpath('//td[@id="ga"]/text()').extract_first() else "-"
        item['speakers_number'] = response.xpath('//td[@id="gb"]/text()').extract_first() \
            if response.xpath('//td[@id="gb"]/text()').extract_first() else "-"
        item['xenon_headlight'] = response.xpath('//td[@id="eo"]/text()').extract_first() \
            if response.xpath('//td[@id="eo"]/text()').extract_first() else "-"
        item['led_headlight'] = response.xpath('//td[@id="ep"]/text()').extract_first() \
            if response.xpath('//td[@id="ep"]/text()').extract_first() else "-"
        item['daytime__lights'] = response.xpath('//td[@id="eq"]/text()').extract_first() \
            if response.xpath('//td[@id="eq"]/text()').extract_first() else "-"
        item['automatic_headlights'] = response.xpath('//td[@id="er"]/text()').extract_first() \
            if response.xpath('//td[@id="er"]/text()').extract_first() else "-"
        item['steering_headlights_or_auxiliary'] = response.xpath('//td[@id="es"]/text()').extract_first() \
            if response.xpath('//td[@id="es"]/text()').extract_first() else "-"
        item['antifog_ligths'] = response.xpath('//td[@id="et"]/text()').extract_first() \
            if response.xpath('//td[@id="et"]/text()').extract_first() else "-"
        item['adjustable_headlight_height'] = response.xpath('//td[@id="eu"]/text()').extract_first() \
            if response.xpath('//td[@id="eu"]/text()').extract_first() else "-"
        item['headlight_cleaning_device'] = response.xpath('//td[@id="ev"]/text()').extract_first() \
            if response.xpath('//td[@id="ev"]/text()').extract_first() else "-"
        item['inside_atmosphere_lights'] = response.xpath('//td[@id="ef"]/text()').extract_first() \
            if response.xpath('//td[@id="ef"]/text()').extract_first() else "-"
        item['front_lectric_windows'] = response.xpath('//td[@id="ew"]/text()').extract_first() \
            if response.xpath('//td[@id="ew"]/text()').extract_first() else "-"
        item['rear_lectric_windows'] = response.xpath('//td[@id="ex"]/text()').extract_first() \
            if response.xpath('//td[@id="ex"]/text()').extract_first() else "-"
        item['window_clip_hand_safety'] = response.xpath('//td[@id="ey"]/text()').extract_first() \
            if response.xpath('//td[@id="ey"]/text()').extract_first() else "-"
        item['insulating_glass'] = response.xpath('//td[@id="ez"]/text()').extract_first() \
            if response.xpath('//td[@id="ez"]/text()').extract_first() else "-"
        item['rearview_mirror_electric_adjustment'] = response.xpath('//td[@id="fa"]/text()').extract_first() \
            if response.xpath('//td[@id="fa"]/text()').extract_first() else "-"
        item['rearview_mirror_heating'] = response.xpath('//td[@id="fb"]/text()').extract_first() \
            if response.xpath('//td[@id="fb"]/text()').extract_first() else "-"
        item['rearview_mirror_auto_anti_glare'] = response.xpath('//td[@id="fc"]/text()').extract_first() \
            if response.xpath('//td[@id="fc"]/text()').extract_first() else "-"
        item['rearview_mirror_electric_folding'] = response.xpath('//td[@id="fd"]/text()').extract_first() \
            if response.xpath('//td[@id="fd"]/text()').extract_first() else "-"
        item['rearview_mirror_memory'] = response.xpath('//td[@id="fe"]/text()').extract_first() \
            if response.xpath('//td[@id="fe"]/text()').extract_first() else "-"
        item['backglass_sunshade'] = response.xpath('//td[@id="eg"]/text()').extract_first() \
            if response.xpath('//td[@id="eg"]/text()').extract_first() else "-"
        item['backsideglass_sunshade'] = response.xpath('//td[@id="eh"]/text()').extract_first() \
            if response.xpath('//td[@id="eh"]/text()').extract_first() else "-"
        item['visor__mirror'] = response.xpath('//td[@id="ei"]/text()').extract_first() \
            if response.xpath('//td[@id="ei"]/text()').extract_first() else "-"
        item['rear_windshield_wiper'] = response.xpath('//td[@id="ff"]/text()').extract_first() \
            if response.xpath('//td[@id="ff"]/text()').extract_first() else "-"
        item['windshield_wiper_sensor'] = response.xpath('//td[@id="fg"]/text()').extract_first() \
            if response.xpath('//td[@id="fg"]/text()').extract_first() else "-"
        item['air_conditioner'] = response.xpath('//td[@id="gc"]/text()').extract_first() \
            if response.xpath('//td[@id="gc"]/text()').extract_first() else "-"
        item['auto_air_conditioner'] = response.xpath('//td[@id="gd"]/text()').extract_first() \
            if response.xpath('//td[@id="gd"]/text()').extract_first() else "-"
        item['rear_independent_ac'] = response.xpath('//td[@id="ge"]/text()').extract_first() \
            if response.xpath('//td[@id="ge"]/text()').extract_first() else "-"
        item['rear_ac'] = response.xpath('//td[@id="gf"]/text()').extract_first() \
            if response.xpath('//td[@id="gf"]/text()').extract_first() else "-"
        item['zone_temperature_control'] = response.xpath('//td[@id="gg"]/text()').extract_first() \
            if response.xpath('//td[@id="gg"]/text()').extract_first() else "-"
        item['ac_pollen_filter'] = response.xpath('//td[@id="gh"]/text()').extract_first() \
            if response.xpath('//td[@id="gh"]/text()').extract_first() else "-"
        item['car_refrigerator'] = response.xpath('//td[@id="gi"]/text()').extract_first() \
            if response.xpath('//td[@id="gi"]/text()').extract_first() else "-"
        yield item
