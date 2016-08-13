#!/usr/bin/env python
# encoding: utf-8

from crawler.tv import PandaCrawl
from crawler.tv import ZhanqiCrawl
from crawler.tv import DouyuCrawl
from crawler.tv import LongzhuCrawl
from crawler.tv import HuyaCrawl

import sys


def main(_type):
    if _type == 'zhanqi':
        ZhanqiCrawl().run(count=1000)
    elif _type == 'panda':
        PandaCrawl().run(count=1000)
    elif _type == 'douyu':
        DouyuCrawl().run(count=1000)
    elif _type == 'longzhu':
        LongzhuCrawl().run(count=1000)
    elif _type == 'huya':
        HuyaCrawl().run(count=1000)
    else:
        ZhanqiCrawl().run(count=200)
        PandaCrawl().run(count=200)
        DouyuCrawl().run(count=200)
        LongzhuCrawl().run(count=200)
        HuyaCrawl().run(count=200)


if __name__ == '__main__':

    from datetime import datetime
    if len(sys.argv) == 1:
        print 'Crawl all start:', datetime.now()
        main('all')
        print 'Crawl all end:', datetime.now()
    else:
        print 'Crawl %s start:' % sys.argv[1] ,datetime.now()
        main(sys.argv[1])
        print 'Crawl %s end:' % sys.argc[1], datetime.now()
