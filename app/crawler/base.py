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
    '魔兽 DOTA1': 'DOTA',
    'Dota2': 'DOTA',
    # DNF
    'DNF': '地下城与勇士',
    # 单机
    '主机游戏': '单机游戏',
    '单机游戏（综合）': '单机游戏',
    '主机游戏（综合）': '单机游戏',
    # 户外
    '户外': '户外直播',
    # 暗黑
    '暗黑破坏神Ⅲ': '暗黑破坏神',
    '暗黑破坏神3': '暗黑破坏神',
    # cs
    'CSGO': 'CS:GO',
    '冒险岛2': '冒险岛',
    # 魔兽
    '魔兽争霸3': '魔兽争霸',
    # 怀旧
    '怀旧回忆': '怀旧经典',
    '怀旧游戏': '怀旧经典',
    '经典怀旧': '怀旧经典',
    # cs
    '反恐精英：全球攻势': '反恐精英',
    '反恐精英Online': '反恐精英',
    # music
    '音乐': '音乐专区',
    # 星际争霸
    '星际争霸2': '星际争霸',
    # 梦幻
    '梦幻西游2': '梦幻西游',
    'CF枪战王者': '穿越火线',
    # 网游
    '热门网游': '网络游戏',
    '网游综合': '网络游戏',
    # 三国杀
    '三国杀英雄传': '三国杀',
    '三国杀移动版': '三国杀',
    # 棋牌
    '棋牌游戏': '棋牌娱乐',
    '棋牌竞技': '棋牌娱乐',
    # NBA2K
    'NBA2K ONLINE': 'NBA2K',
    'NBA篮球竞技': 'NBA2K',
    'NBA2KOL': 'NBA2K',
    # 星秀
    '龙珠星秀': '星秀',
    '全民星秀': '星秀',
    # 拳皇
    '拳皇98OL': '拳皇',
    '拳皇97': '拳皇',
    # 传奇
    '热血传奇': '传奇',
    '传奇永恒': '传奇',
    # 怪物猎人
    '怪物猎人ol': '怪物猎人',
    '怪物猎人online': '怪物猎人',
    '怪物猎人OL': '怪物猎人',
    # 足球
    'FIFA Online3': 'FIFA',
    'FIFA Online': 'FIFA',
    'FIFA足球': 'FIFA',
    # 战地
    '战地之王': '战地',
    #
    '一起看': '游戏放映厅',
    '视听点评': '游戏放映厅',
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
                if not tv.avatar and r[0].avatar:
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

