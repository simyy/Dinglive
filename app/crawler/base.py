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
            if len(res) == 0:
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

    def save(self, items):
        ctg_dict = self._get_ctgs()
        session = self.backend.get_session()
        for item in items:
            ctg_id = ctg_dict.get(item['category_id'], None)
            if ctg_id:
                item['category_id'] = ctg_id
            else:
                tvctg = TVCtg(name=item['category_id'])
                session.add(tvctg)
                session.commit()
                ctg_dict[item['category_id']] = tvctg.id
                item['category_id'] = tvctg.id
            print item
            tv = TV(**item)
            r = session.query(TV).filter(
                TV.room_id==item['room_id'],
                TV.source_id==item['source_id']).all()[:1]
            if r:
                tv.id = r[0].id
                if not tv.avatar and r[0].avatar:
                    tv.avatar = r[0].avatar
                else:
                    tv.avatar = self._get_avatar_url(item['room_site'])
                #print '重复tvroom id=%d' % int(tv.id)
                #print r[0].room_name, r[0].room_id, r[0].source_id
                #print tv.room_name, tv.room_id, tv.source_id
            else:
                tv.avatar = self._get_avatar_url(item['room_site'])
            new_tv = session.merge(tv)
            session.add(new_tv)
            session.commit()

    def _get_avatar_url(self, room_site):
        return '/static/img/avatar/default.jpg'

    def _get_ctgs(self):
        session = self.backend.get_session()
        rows = session.query(TVCtg).all()
        ctg_dict = dict()
        for row in rows:
            ctg_dict[row.name] = row.id
        return ctg_dict

