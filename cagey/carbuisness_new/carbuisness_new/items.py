# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarbuisnessNewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AllLocationItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    province_name = scrapy.Field()
    province_id = scrapy.Field()
    city_name = scrapy.Field()
    city_id = scrapy.Field()
    district_name = scrapy.Field()
    district_id = scrapy.Field()
    street_name = scrapy.Field()
    street_id = scrapy.Field()
    citycode = scrapy.Field()
    center = scrapy.Field()
    level = scrapy.Field()
    polyline = scrapy.Field()


class JzgPriceItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    brandid = scrapy.Field()
    familyid = scrapy.Field()
    modelid = scrapy.Field()
    brandname = scrapy.Field()
    familyname = scrapy.Field()
    model_full_name = scrapy.Field()
    HBBZ = scrapy.Field()
    RegDateTime = scrapy.Field()
    RegDate = scrapy.Field()
    MarketMonthNum = scrapy.Field()
    Mileage = scrapy.Field()
    ProvId = scrapy.Field()
    ProvName = scrapy.Field()
    CityId = scrapy.Field()
    CityName = scrapy.Field()
    NowMsrp = scrapy.Field()
    C2BLowPrice_sell_img = scrapy.Field()
    C2BMidPrice_sell = scrapy.Field()
    C2BUpPrice_sell_img = scrapy.Field()
    B2CLowPrice_buy_img = scrapy.Field()
    B2CMidPrice_buy_img = scrapy.Field()
    B2CUpPrice_buy_img = scrapy.Field()
    # C2BBLowPrice = scrapy.Field()
    # C2BBMidPrice = scrapy.Field()
    # C2BBUpPrice = scrapy.Field()
    # C2BCLowPrice = scrapy.Field()
    # C2BCMidPrice = scrapy.Field()
    # C2BCUpPrice = scrapy.Field()
    C2CLowPrice_sell_img = scrapy.Field()
    C2CMidPrice_sell_img = scrapy.Field()
    C2CUpPrice_sell_img = scrapy.Field()
    C2CLowPrice_buy_img = scrapy.Field()
    C2CMidPrice_buy_img = scrapy.Field()
    C2CUpPrice_buy_img = scrapy.Field()
    # C2CLowPrice = scrapy.Field()
    # C2CMidPrice = scrapy.Field()
    # C2CUpPrice = scrapy.Field()
    PriceLevel = scrapy.Field()
    BaoZhilvRank = scrapy.Field()
    BaoZhilvCityId = scrapy.Field()
    BaoZhilvCityName = scrapy.Field()
    BaoZhilvLevel = scrapy.Field()
    BaoZhilvLevelName = scrapy.Field()
    BaoZhilvPercentage = scrapy.Field()
    maxPrice = scrapy.Field()
    minLoanRate = scrapy.Field()
    ShareUrl = scrapy.Field()
    PlatNumber = scrapy.Field()
    type = scrapy.Field()


class JzgModelListItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    fastest_speed = scrapy.Field()
    factory = scrapy.Field()
    body_structure = scrapy.Field()
    l_w_h = scrapy.Field()
    gear = scrapy.Field()
    offical_oil_consumption = scrapy.Field()
    national_oil_consumption = scrapy.Field()
    engine = scrapy.Field()
    acceleration = scrapy.Field()
    level = scrapy.Field()
    roof_style = scrapy.Field()
    trim_color = scrapy.Field()
    roof_rack = scrapy.Field()
    hood = scrapy.Field()
    number_gears = scrapy.Field()
    shift_dial = scrapy.Field()
    geartype = scrapy.Field()
    front_seat_heating = scrapy.Field()
    back_seat_heating = scrapy.Field()
    elec_seat_memery = scrapy.Field()
    shoulder_support_adjusting = scrapy.Field()
    front_seat_center_handler = scrapy.Field()
    auxiliary_driving_seat_adjusting = scrapy.Field()
    seats_height_adjusting = scrapy.Field()
    back_seat_ventilation = scrapy.Field()
    second_seat_angle_adjusting = scrapy.Field()
    back_seat_center_handler = scrapy.Field()
    driving_seat_adjusting = scrapy.Field()
    back_cup_frame = scrapy.Field()
    front_seat_ventilation = scrapy.Field()
    second_seat_moving = scrapy.Field()
    back_seat_massage = scrapy.Field()
    third_seat = scrapy.Field()
    sport_style_seat = scrapy.Field()
    back_seat_lay_down_type = scrapy.Field()
    front_seat_massage = scrapy.Field()
    genuine_imitation_leather_seat = scrapy.Field()
    waist_support_adjusting = scrapy.Field()
    front_seat_heating = scrapy.Field()
    night_vision_system = scrapy.Field()
    ldws = scrapy.Field()
    engine_start_stop_tech = scrapy.Field()
    adaptive_cruise_control = scrapy.Field()
    panoramic_camera = scrapy.Field()
    automatic_parking = scrapy.Field()
    brake_and_safty_system = scrapy.Field()
    integrated_active_steering_system = scrapy.Field()
    central_control_panel_display = scrapy.Field()
    parallel_auxiliary = scrapy.Field()
    front_seat_heating = scrapy.Field()
    sun_visor = scrapy.Field()
    anti_glare_inner_rearview_mirror = scrapy.Field()
    window_clamping_function = scrapy.Field()
    electric_folding_rearview_mirror = scrapy.Field()
    induction_wiper = scrapy.Field()
    rearview_mirror_heating = scrapy.Field()
    rear_windshield_sunshade_curtain = scrapy.Field()
    rear_electric_window = scrapy.Field()
    rearview_mirror_side_signal = scrapy.Field()
    rear_side_privacy_glass = scrapy.Field()
    rear_wiper = scrapy.Field()
    front_electric_window = scrapy.Field()
    uv_thermal_insulation_glass = scrapy.Field()
    rear_side_sunshade_curtain = scrapy.Field()
    rearview_mirror_memory = scrapy.Field()
    anti_glare_external_rearview_mirror = scrapy.Field()
    engine_position = scrapy.Field()
    fuel_supply_mode = scrapy.Field()
    environmental_protection_standard = scrapy.Field()
    displacement = scrapy.Field()
    intake_mode = scrapy.Field()
    maximum_horsepower = scrapy.Field()
    fuel_labeling = scrapy.Field()
    trip = scrapy.Field()
    maximum_torque_speed = scrapy.Field()
    fuel_form = scrapy.Field()
    engine_specific_tech = scrapy.Field()
    cylinder_head_material = scrapy.Field()
    maximum_torque = scrapy.Field()
    number_cylinders = scrapy.Field()
    engine_type = scrapy.Field()
    cylinder_diameter = scrapy.Field()
    maximum_power_speed = scrapy.Field()
    cylinder_arrangement = scrapy.Field()
    valve_structure = scrapy.Field()
    compression_ratio = scrapy.Field()
    cylinder_material = scrapy.Field()
    maximum_power = scrapy.Field()
    valve_per_cylinder = scrapy.Field()
    number_seats = scrapy.Field()
    luggage_compartment_volume = scrapy.Field()
    height = scrapy.Field()
    width = scrapy.Field()
    length = scrapy.Field()
    tank_volume = scrapy.Field()
    rear_wheelbase = scrapy.Field()
    minimum_ground_clearance = scrapy.Field()
    wheelbase = scrapy.Field()
    maximum_load_weight = scrapy.Field()
    number_doors = scrapy.Field()
    front_wheelbase = scrapy.Field()
    preparation_quality = scrapy.Field()
    electrically_operated_suction_door = scrapy.Field()
    motor_type = scrapy.Field()
    mic_milestone = scrapy.Field()
    motor_total_power = scrapy.Field()
    battery_capacity = scrapy.Field()
    front_motor_maximum_torque = scrapy.Field()
    rear_motor_maximum_torque = scrapy.Field()
    front_motor_maximum_power = scrapy.Field()
    rear_motor_maximum_power = scrapy.Field()
    parking_brake_type = scrapy.Field()
    spare_tire_specification = scrapy.Field()
    rear_tire_specification = scrapy.Field()
    rear_brake_type = scrapy.Field()
    front_tire_specification = scrapy.Field()
    front_brake_type = scrapy.Field()
    sports_appearance_kit = scrapy.Field()
    electric_skylight = scrapy.Field()
    electrically_operated_suction_door = scrapy.Field()
    electric_reserve_compartment = scrapy.Field()
    induction_reserve_compartment = scrapy.Field()
    panoramic_sunroof = scrapy.Field()
    sideslip_door = scrapy.Field()
    loudspeaker_quantity = scrapy.Field()
    speaker_brand = scrapy.Field()
    central_console_color_screen = scrapy.Field()
    location_interaction_service = scrapy.Field()
    gps_navigation_system = scrapy.Field()
    multimedia_system = scrapy.Field()
    car_tv = scrapy.Field()
    mp3_wma_support = scrapy.Field()
    external_audio_interface = scrapy.Field()
    blueteeth_and_car_phone = scrapy.Field()
    rear_lcd_screen = scrapy.Field()
    front_seat_belt_adjustmentw = scrapy.Field()
    front_side_airbag = scrapy.Field()
    keyless_entry_system = scrapy.Field()
    rear_head_airbag = scrapy.Field()
    zero_tire_pressure_driving = scrapy.Field()
    seat_belt_pre_tightening = scrapy.Field()
    keyless_starting_system = scrapy.Field()
    front_head_airbag = scrapy.Field()
    remote_key = scrapy.Field()
    seat_belt_limitation = scrapy.Field()
    children_lock = scrapy.Field()
    seat_belt_warning = scrapy.Field()
    auxiliary_seat_safety_airbag = scrapy.Field()
    vehicle_central_control_lock = scrapy.Field()
    rear_center_seat_belt = scrapy.Field()
    engine_electronic_anti_theft = scrapy.Field()
    driving_seat_safety_airbag = scrapy.Field()
    knee_airbag = scrapy.Field()
    rear_seat_belt = scrapy.Field()
    isofix_children_seat_interface = scrapy.Field()
    rear_side_airbag = scrapy.Field()
    tire_pressure_monitoring_device = scrapy.Field()
    multifunctional_steering_wheel = scrapy.Field()
    full_lcd_dashboard = scrapy.Field()
    steering_wheel_adjusting = scrapy.Field()
    reversing_video = scrapy.Field()
    steering_wheel_memory_settings = scrapy.Field()
    hud_rising_number_display = scrapy.Field()
    steering_wheel_heating = scrapy.Field()
    driving_computer_display_screen = scrapy.Field()
    rear_parking_radar = scrapy.Field()
    cruise_control = scrapy.Field()
    leather_steering_wheel = scrapy.Field()
    front_parking_radar = scrapy.Field()
    steering_auxiliary_lamp = scrapy.Field()
    led_taillights = scrapy.Field()
    drl = scrapy.Field()
    turning_headlights = scrapy.Field()
    front_reading_lamp = scrapy.Field()
    headlamp_height_adjustable = scrapy.Field()
    front_headlamp_automatic_steering = scrapy.Field()
    headlight_cleaning_device = scrapy.Field()
    interior_atmosphere_lamp = scrapy.Field()
    front_fog_lamp = scrapy.Field()
    side_turn_lamp = scrapy.Field()
    automatic_headlamp = scrapy.Field()
    led_headlights = scrapy.Field()
    high_brake_lights = scrapy.Field()
    air_conditioning = scrapy.Field()
    air_conditioning_control_mode = scrapy.Field()
    temperature_zoning_control = scrapy.Field()
    rear_seat_outlet = scrapy.Field()
    vehicle_air_purification_equipment = scrapy.Field()
    rear_independent_air_conditioning = scrapy.Field()
    vehicle_refrigerator = scrapy.Field()
    steering_power = scrapy.Field()
    front_suspension_type = scrapy.Field()
    rear_suspension_type = scrapy.Field()
    driving_mode = scrapy.Field()
    central_differential_structure = scrapy.Field()
    chassis_structure = scrapy.Field()
    minimum_turning_radius = scrapy.Field()
    approach_angle = scrapy.Field()
    departure_angle = scrapy.Field()
    braking_force_distribution = scrapy.Field()
    rear_limited_slip_differential = scrapy.Field()
    hdc = scrapy.Field()
    central_differential_locking = scrapy.Field()
    variable_steering_ratio = scrapy.Field()
    blind_spot_detection = scrapy.Field()
    vehicle_stability_control = scrapy.Field()
    hill_start_assist = scrapy.Field()
    variable_suspension = scrapy.Field()
    automatic_steering_adjusting = scrapy.Field()
    auto_parking = scrapy.Field()
    abs_anti_lock = scrapy.Field()
    front_limited_slip_differential = scrapy.Field()
    air_suspension = scrapy.Field()
    adjustable_suspension = scrapy.Field()
    brake_assist = scrapy.Field()
    traction_control = scrapy.Field()
    instrument_panel_brightness_adjusting = scrapy.Field()
    brandid = scrapy.Field()
    brandname = scrapy.Field()
    familyname = scrapy.Field()
    familyid = scrapy.Field()
    model_full_name = scrapy.Field()
    modelname = scrapy.Field()
    modelid = scrapy.Field()
    make_year = scrapy.Field()
    next_year = scrapy.Field()


class AutohomeErrorItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    waiguan1 = scrapy.Field()
    xingshi1 = scrapy.Field()
    caozuo1 = scrapy.Field()
    dianzi1 = scrapy.Field()
    zuoyi1 = scrapy.Field()
    kongtiao1 = scrapy.Field()
    neishi1 = scrapy.Field()
    fadongji1 = scrapy.Field()
    waiguan2 = scrapy.Field()
    xingshi2 = scrapy.Field()
    caozuo2 = scrapy.Field()
    dianzi2 = scrapy.Field()
    zuoyi2 = scrapy.Field()
    kongtiao2 = scrapy.Field()
    neishi2 = scrapy.Field()
    fadongji2 = scrapy.Field()
    familyid = scrapy.Field()
    category_id = scrapy.Field()
    json = scrapy.Field()
    biansuxitong1 = scrapy.Field()
    sum = scrapy.Field()

    brand = scrapy.Field()
    series = scrapy.Field()
    series_id = scrapy.Field()
    newcar_quality = scrapy.Field()
    newcar_bug_num = scrapy.Field()
    newcar_bug_type = scrapy.Field()
    newcar_people_num = scrapy.Field()
    newcar_bug_ratio = scrapy.Field()
    oldcar_quality = scrapy.Field()
    oldcar_bug_num = scrapy.Field()
    oldcar_people_num = scrapy.Field()
    oldcar_bug_type = scrapy.Field()
    oldcar_bug_ratio = scrapy.Field()


class XiaoZhuItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    brand_id = scrapy.Field()
    factoryId = scrapy.Field()
    factoryName = scrapy.Field()
    series_id = scrapy.Field()
    maxFactoryPrice = scrapy.Field()
    minFactoryPrice = scrapy.Field()
    referencePrice = scrapy.Field()
    series = scrapy.Field()
    model_category = scrapy.Field()
    model_id = scrapy.Field()
    price = scrapy.Field()
    output = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    saleStatus = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    # xiaozhu_gz
    prices = scrapy.Field()
    city = scrapy.Field()
    registerdate = scrapy.Field()
    mile = scrapy.Field()
    desc = scrapy.Field()
    url = scrapy.Field()


class AutohomeGzItem(scrapy.Item):
    autohomeid = scrapy.Field()

    price_data_info = scrapy.Field()
    good_guarantee_buy = scrapy.Field()
    good_merchant_buy = scrapy.Field()
    good_personage_buy = scrapy.Field()
    good_personage_sell = scrapy.Field()
    good_4Sreplacement = scrapy.Field()
    good_merchant_sell = scrapy.Field()

    middle_guarantee_buy = scrapy.Field()
    middle_merchant_buy = scrapy.Field()
    middle_personage_buy = scrapy.Field()
    middle_personage_sell = scrapy.Field()
    middle_4Sreplacement = scrapy.Field()
    middle_merchant_sell = scrapy.Field()

    bad_guarantee_buy = scrapy.Field()
    bad_merchant_buy = scrapy.Field()
    bad_personage_buy = scrapy.Field()
    bad_personage_sell = scrapy.Field()
    bad_4Sreplacement = scrapy.Field()
    bad_merchant_sell = scrapy.Field()

    url_list = scrapy.Field()
    city = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    registerdate = scrapy.Field()
    mile = scrapy.Field()
    url = scrapy.Field()











