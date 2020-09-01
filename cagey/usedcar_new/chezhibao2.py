__author__ = 'cagey'
from scrapy.cmdline import execute

import sys
import os


website = "chezhibao2"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])
