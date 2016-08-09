#!/usr/bin/env python
# encoding: utf-8

from crawler.tv import PandaCrawl
from crawler.tv import ZhanqiCrawl


def main():
    ZhanqiCrawl().run(count=500)
    PandaCrawl().run(count=500)


if __name__ == '__main__':
    main()
