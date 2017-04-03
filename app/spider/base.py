#!/usr/bin/env python
# encoding: utf-8

import os
import time
import random
import requests

from core.base import WithBackend
from models.tables import TV
from models.tables import TVCtg


def loadCtgDict():
    d = dict()
    if os.path.exists('/opt/dinglive/app'):
        fileName = '/opt/dinglive/app/spider/ctg.txt'
    else:
        fileName = 'spider/ctg.txt'
    with open(fileName) as f:
        lines = f.readlines()
        lines = filter(
            lambda x: x.startswith('#') is False and len(x.strip()) > 0, lines)
        lines = map(lambda x: x.strip().decode('utf8'), lines)
        for line in lines:
            items = line.split('=')
            cate = items[0]
            sort = int(items[1])
            mapping = items[2].split("|")
            if len(mapping) == 2:
                d[mapping[0]] = [mapping[1], cate, sort]
            else:
                d[mapping[0]] = [mapping[0], cate, sort]
        return d


CTG_DICT = loadCtgDict()


class CrawlerException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BaseCrawl(WithBackend):
    def __init__(self, method='get'):
        self.method = method

    def run(self, url, count=300, size=100):
        result = list()
        page = 0
        size = size
        num = 0
        while num < count:
            page += 1
            tmp_url = url.format(page=page, size=size)
            res = self.load(tmp_url)
            if not res or len(res) == 0:
                break
            num += len(res)
            print 'load\turl:%s' % tmp_url
            print 'num:', num
            if res:
                result.extend(res)
            time.sleep(random.randrange(10))
        self.save(result)

    def load(self, url, kwargs=None):
        if self.method == 'get':
            r = self._get(url, kwargs=kwargs)
        else:
            r = self._post(url, kwargs=kwargs)
        if r:
            try:
                return self.parse(r)
            except Exception as e:
                print e
        return None

    def parse(self, html):
        pass

    def getRandomHeader(self):
        header = [
            "Mozilla/5.0 (compatible, MSIE 10.0, Windows NT, DigExt)",
            "Mozilla/4.0 (compatible, MSIE 7.0, Windows NT 5.1, 360SE)",
            "Mozilla/4.0 (compatible, MSIE 8.0, Windows NT 6.0, Trident/4.0)",
            "Mozilla/5.0 (compatible, MSIE 9.0, Windows NT 6.1, Trident/5.0,",
            "Opera/9.80 (Windows NT 6.1, U, en) Presto/2.8.131 Version/11.11",
            "Mozilla/4.0 (compatible, MSIE 7.0, Windows NT 5.1, TencentTraveler 4.0)",
            "Mozilla/5.0 (Windows, U, Windows NT 6.1, en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Macintosh, Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh, U, Intel Mac OS X 10_6_8, en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Linux, U, Android 3.0, en-us, Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (iPad, U, CPU OS 4_3_3 like Mac OS X, en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/4.0 (compatible, MSIE 7.0, Windows NT 5.1, Trident/4.0, SE 2.X MetaSr 1.0, SE 2.X MetaSr 1.0, .NET CLR 2.0.50727, SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (iPhone, U, CPU iPhone OS 4_3_3 like Mac OS X, en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "MQQBrowser/26 Mozilla/5.0 (Linux, U, Android 2.3.7, zh-cn, MB200 Build/GRJ22, CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        ]
        return {"User-Agent": header[random.randrange(0, len(header))]}

    def _get(self, url, kwargs=None):
        r = requests.get(url, headers=self.getRandomHeader(), verify=False)
        if r.status_code == 200:
            return r.text
        return None

    def _post(self, url, kwargs=None):
        r = requests.post(url, kwargs, headers=self.getRandomHeader())
        if r.status_code == 200:
            return r.text
        return None

    def save(self, items):
        ctg_dict = self._get_ctgs()
        session = self.backend.get_session()
        for item in items:
            try:
                item['category_id'] = CTG_DICT.get(
                        item['category_id'],
                        [u'大杂烩', 0, 0])[0]
                ctg_id = ctg_dict.get(item['category_id'], None)
                if ctg_id:
                    item['category_id'] = ctg_id
                else:
                    cate = CTG_DICT.get(item['category_id'])[1]
                    sort = CTG_DICT.get(item['category_id'])[2]
                    tvctg = TVCtg(name=item['category_id'], cate=cate, sort=sort)
                    session.add(tvctg)
                    session.commit()
                    ctg_dict[item['category_id']] = tvctg.id
                    item['category_id'] = tvctg.id
                tv = TV(**item)
                r = session.query(TV).filter(
                    TV.room_id == item['room_id'],
                    TV.source_id == item['source_id']).all()[:1]
                if r:
                    tv.id = r[0].id
                    if not tv.avatar:
                        tv.avatar = r[0].avatar
                    # print '重复tvroom id=%d' % int(tv.id)
                    # print r[0].room_name, r[0].room_id, r[0].source_id
                    # print tv.room_name, tv.room_id, tv.source_id
                if not tv.avatar:
                    tv.avatar = self._get_avatar_url(item['room_site'])
                new_tv = session.merge(tv)
                session.add(new_tv)
                session.commit()
            except Exception as e:
                print e

    def _get_avatar_url(self, room_site):
        return '/static/img/avatar/default.jpg'

    def _get_ctgs(self):
        session = self.backend.get_session()
        rows = session.query(TVCtg).all()
        ctg_dict = dict()
        for row in rows:
            ctg_dict[row.name] = row.id
        return ctg_dict

