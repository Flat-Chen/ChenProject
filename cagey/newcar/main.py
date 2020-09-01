from scrapy.cmdline import execute

import sys
import os


website = "new_autohome_newcar_v3_20190719"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


