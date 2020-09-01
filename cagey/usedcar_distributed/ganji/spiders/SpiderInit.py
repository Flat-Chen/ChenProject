#-*- coding: UTF-8 -*-
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


# original
def spider_original_Init(dbname, website, carnum):
    # Mongo setting
    settings.set('CrawlCar_Num', carnum, priority='cmdline')
    settings.set('MONGODB_DB', dbname, priority='cmdline')
    settings.set('MONGODB_COLLECTION', website, priority='cmdline')
