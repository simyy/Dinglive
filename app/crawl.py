#!/usr/bin/env python
# encoding: utf-8

from crawler.tv import PandaCrawl
from crawler.tv import ZhanqiCrawl
from crawler.tv import DouyuCrawl
from crawler.tv import LongzhuCrawl
from crawler.tv import HuyaCrawl
from crawler.tv import QuanminCrawl
from crawler.tv import HuomaoCrawl

import sys


def main(_type):
    if _type == 'zhanqi':
        ZhanqiCrawl().run(count=500)
    elif _type == 'panda':
        PandaCrawl().run(count=500)
    elif _type == 'douyu':
        DouyuCrawl().run(count=500)
    elif _type == 'longzhu':
        LongzhuCrawl().run(count=500)
    elif _type == 'huya':
        HuyaCrawl().run(count=500)
    elif _type == 'quanmin':
        QuanminCrawl().run(count=500)
    elif _type == 'huomao':
        HuomaoCrawl().run(count=500)
    else:
        DouyuCrawl().run(count=20)
        ZhanqiCrawl().run(count=50)
        PandaCrawl().run(count=50)
        LongzhuCrawl().run(count=50)
        HuyaCrawl().run(count=50)
        QuanminCrawl().run(count=50)


if __name__ == '__main__':

    from datetime import datetime
    if len(sys.argv) == 1:
        print 'Crawl all start:', datetime.now()
        main('all')
        print 'Crawl all end:', datetime.now()
    else:
        print 'Crawl %s start:' % sys.argv[1] ,datetime.now()
        main(sys.argv[1])
        print 'Crawl %s end:' % sys.argv[1], datetime.now()
