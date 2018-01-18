# -*- coding: utf-8 -*-
# Author: Morrow

from scrapy.cmdline import execute # scrapy断点测试
import  sys
import os

print os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','jobbole'])
