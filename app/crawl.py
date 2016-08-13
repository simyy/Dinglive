#!/usr/bin/env python
# encoding: utf-8

from crawler.tv import PandaCrawl
from crawler.tv import ZhanqiCrawl
from crawler.tv import DouyuCrawl
from crawler.tv import LongzhuCrawl
from crawler.tv import HuyaCrawl


def main():
    ZhanqiCrawl().run(count=1000)
    PandaCrawl().run(count=1000)
    DouyuCrawl().run(count=1000)
    LongzhuCrawl().run(count=1000)
    HuyaCrawl().run(count=1000)


if __name__ == '__main__':

    from datetime import datetime
    print 'Crawl start:', datetime.now()
    main()
    print 'Crawl end:', datetime.now()
