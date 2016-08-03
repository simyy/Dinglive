#!/usr/bin/env python
# encoding: utf-8

import time
import random
import requests

from core.base import WithBackend


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
    def __init__(self, roomId, title, name, avatar, gender,
            url, pic, count, ctg_id, src_id):
        self.roomId = roomId
        self.title = title
        self.name = name
        self.avatar = avatar
        self.gender = gender
        self.url = url
        self.pic = pic
        self.count = count
        self.ctg_id = ctg_id
        self.src_id = src_id

    def _save_pic(self):
        if self.avatar is not None:
            pass
        if self.pic is not None:
            pass

    def save(self):
        pass
