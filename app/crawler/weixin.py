#!/usr/bin/env python
# encoding: utf-8

from base import BaseCrawl
from bs4 import BeautifulSoup


class ChildCrawl(BaseCrawl):
    def __init__(self, url):
        super(ChildCrawl, self).__init__(url, method='get')

    def parse(self, html):
        soup = BeautifulSoup(html, 'lxml')
        #print soup.prettify()
        for item in soup.findAll('div', class_='wx-rb wx-rb3'):
            print 'href', item.select('a[data-z="art"]')[0].attrs['href']
            print 'title', item.
            print 'pic', 



if __name__ == '__main__':
    ChildCrawl('http://weixin.sogou.com/weixin?type=2&query=\
                %E5%B9%BC%E5%84%BF&ie=utf8&_sug_=n&_sug_type_=').run(None)
