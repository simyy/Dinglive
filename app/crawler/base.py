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


CTG_DICT = {
    # dota
    'DOTA2': 'DOTA', 
    u'魔兽 DOTA1': 'DOTA',
    'Dota2': 'DOTA',
    # DNF
    'DNF': u'地下城与勇士',
    # 单机
    u'主机游戏': u'单机游戏',
    u'单机游戏（综合）': u'单机游戏',
    u'主机游戏（综合）': u'单机游戏',
    # 户外
    u'户外': u'户外直播',
    # 暗黑
    u'暗黑破坏神Ⅲ': u'暗黑破坏神',
    u'暗黑破坏神3': u'暗黑破坏神',
    # cs
    'CSGO': 'CS:GO',
    u'冒险岛2': u'冒险岛',
    # 魔兽
    u'魔兽争霸3': u'魔兽争霸',
    # 怀旧
    u'怀旧回忆': u'怀旧经典',
    u'怀旧游戏': u'怀旧经典',
    u'经典怀旧': u'怀旧经典',
    # cs
    u'反恐精英：全球攻势': u'反恐精英',
    u'反恐精英Online': u'反恐精英',
    # music
    u'音乐': u'音乐专区',
    # 星际争霸
    u'星际争霸2': u'星际争霸',
    # 梦幻
    u'梦幻西游2': u'梦幻西游',
    u'CF枪战王者': u'穿越火线',
    # 网游
    u'热门网游': u'网络游戏',
    u'网游综合': u'网络游戏',
    # 三国杀
    u'三国杀英雄传': u'三国杀',
    u'三国杀移动版': u'三国杀',
    # 棋牌
    u'棋牌游戏': u'棋牌娱乐',
    u'棋牌竞技': u'棋牌娱乐',
    # NBA2K
    'NBA2K ONLINE': 'NBA2K',
    u'NBA篮球竞技': 'NBA2K',
    'NBA2KOL': 'NBA2K',
    # 星秀
    u'龙珠星秀': u'星秀',
    u'全民星秀': u'星秀',
    # 拳皇
    u'拳皇98OL': u'拳皇',
    u'拳皇97': u'拳皇',
    # 传奇
    u'热血传奇': u'传奇',
    u'传奇永恒': u'传奇',
    # 怪物猎人
    u'怪物猎人ol': u'怪物猎人',
    u'怪物猎人online': u'怪物猎人',
    u'怪物猎人OL': u'怪物猎人',
    # 足球
    'FIFA Online3': 'FIFA',
    'FIFA Online': 'FIFA',
    u'FIFA足球': 'FIFA',
    # 战地
    u'战地之王': u'战地',
    #
    u'一起看': u'游戏放映室',
    u'视听点评': u'游戏放映室',
    u'龙珠拼盘': u'游戏放映室',
}


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
            if item['category_id'] in CTG_DICT:
                item['category_id'] = CTG_DICT.get(item['category_id'])
            ctg_id = ctg_dict.get(item['category_id'], None)
            if ctg_id:
                item['category_id'] = ctg_id
            else:
                tvctg = TVCtg(name=item['category_id'])
                session.add(tvctg)
                session.commit()
                ctg_dict[item['category_id']] = tvctg.id
                item['category_id'] = tvctg.id
            tv = TV(**item)
            r = session.query(TV).filter(
                TV.room_id==item['room_id'],
                TV.source_id==item['source_id']).all()[:1]
            if r:
                tv.id = r[0].id
                if not tv.avatar:
                    tv.avatar = r[0].avatar
                #print '重复tvroom id=%d' % int(tv.id)
                #print r[0].room_name, r[0].room_id, r[0].source_id
                #print tv.room_name, tv.room_id, tv.source_id
            if not tv.avatar:
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

