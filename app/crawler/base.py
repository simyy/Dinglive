#!/usr/bin/env python
# encoding: utf-8

import time
import random
import requests

from core.base import WithBackend
from models.tables import TV
from models.tables import TVCtg
from models.tables import TVSrc
from common.utils import save_pic


class CrawlerException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BaseCrawl(object):
    def __init__(self, method='get'):
        self.method = method

    def run(self, url, maxCount=300):
        result = list()
        page = 0
        size = 30
        while page * size < maxCount:
            page += 1
            tmp_url = url.format(page=page, size=size)
            res = self.load(tmp_url)
            print 'load\turl:%s' % tmp_url
            if res:
                result.extend(res)
            time.sleep(random.randrange(10))
        return result

    def load(self, url, kwargs=None):
        if self.method == 'get':
            r = self._get(url, kwargs=kwargs)
        else:
            r = self._post(url, kwargs=kwargs)
        if r:
            return self.parse(r)
        return None

    def parse(self, html):
        pass

    def _get(self, url, kwargs=None):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None

    def _post(self, url, kwargs=None):
        r = requests.post(url, kwargs)
        if r.status_code == 200:
            return r.text
        return None


class TVRoom(WithBackend):
    def __init__(self, **kwargs):
        if len(kwargs) != 11:
            raise CrawlerException('TVRoom初始化异常')
        self.tv = TV.new(kwargs)

    def _save_pic(self):
        pass

    def save(self):
        session = self.backend.get_session()
        new_tv = session.merge(self.tv)
        session.save(new_tv)
